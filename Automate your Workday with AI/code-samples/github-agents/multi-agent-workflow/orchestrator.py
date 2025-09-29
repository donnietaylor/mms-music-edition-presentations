#!/usr/bin/env python3
"""
Multi-Agent Workflow Orchestrator
Demonstrates coordination of multiple GitHub Agents for enhanced performance
"""

import asyncio
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import redis
import aioredis
from github import Github

class AgentType(Enum):
    CODE_REVIEW = "code_review"
    SECURITY_SCAN = "security_scan"
    TEST_GENERATION = "test_generation"
    DOCUMENTATION = "documentation"
    DEPLOYMENT = "deployment"
    MONITORING = "monitoring"

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class Task:
    id: str
    type: AgentType
    priority: int
    data: Dict[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    assigned_agent: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    result: Optional[Dict] = None
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

@dataclass
class WorkflowResult:
    workflow_id: str
    total_time: float
    tasks_completed: int
    tasks_failed: int
    parallel_efficiency: float
    agent_utilization: Dict[str, float]

class AgentOrchestrator:
    def __init__(self):
        self.github = Github(os.getenv('GITHUB_TOKEN'))
        self.redis_client = None
        self.agents = {}  # Available agents by type
        self.active_workflows = {}
        self.task_queue = asyncio.Queue()
        
        # Performance tracking
        self.metrics = {
            'workflows_processed': 0,
            'total_tasks_executed': 0,
            'parallel_tasks_executed': 0,
            'average_workflow_time': 0,
            'agent_utilization': {}
        }
        
        # Load configuration
        self.load_configuration()
    
    async def initialize(self):
        """Initialize async components"""
        try:
            self.redis_client = await aioredis.from_url(
                os.getenv('REDIS_URL', 'redis://localhost:6379')
            )
            print("✅ Connected to Redis message bus")
        except Exception as e:
            print(f"⚠️ Redis connection failed: {e}")
        
        # Register available agents
        await self.discover_agents()
        
        # Start background workers
        asyncio.create_task(self.task_processor())
        asyncio.create_task(self.health_monitor())
    
    def load_configuration(self):
        """Load orchestration configuration"""
        # Default configuration - would load from files in production
        self.config = {
            'max_parallel_tasks': 5,
            'task_timeout': 300,  # 5 minutes
            'retry_attempts': 3,
            'circuit_breaker_threshold': 5,
            'workflows': {
                'pull_request': {
                    'tasks': [
                        {'type': 'code_review', 'priority': 8, 'parallel': True},
                        {'type': 'security_scan', 'priority': 9, 'parallel': True},
                        {'type': 'test_generation', 'priority': 6, 'depends_on': ['code_review']},
                        {'type': 'documentation', 'priority': 4, 'depends_on': ['code_review']},
                        {'type': 'deployment', 'priority': 5, 'depends_on': ['security_scan', 'test_generation']}
                    ]
                },
                'issue_triage': {
                    'tasks': [
                        {'type': 'classification', 'priority': 10},
                        {'type': 'assignment', 'priority': 8, 'depends_on': ['classification']},
                        {'type': 'template_application', 'priority': 6, 'depends_on': ['classification']},
                        {'type': 'notification', 'priority': 7, 'depends_on': ['assignment']}
                    ]
                }
            }
        }
    
    async def discover_agents(self):
        """Discover and register available agents"""
        # In production, this would discover agents via service registry
        self.agents = {
            AgentType.CODE_REVIEW: {
                'instances': ['code-review-1', 'code-review-2'],
                'capacity': 3,
                'current_load': 0,
                'health_status': 'healthy'
            },
            AgentType.SECURITY_SCAN: {
                'instances': ['security-1'],
                'capacity': 2,
                'current_load': 0,
                'health_status': 'healthy'
            },
            AgentType.TEST_GENERATION: {
                'instances': ['test-gen-1'],
                'capacity': 2,
                'current_load': 0,
                'health_status': 'healthy'
            },
            AgentType.DOCUMENTATION: {
                'instances': ['docs-1'],
                'capacity': 1,
                'current_load': 0,
                'health_status': 'healthy'
            },
            AgentType.DEPLOYMENT: {
                'instances': ['deploy-1'],
                'capacity': 2,
                'current_load': 0,
                'health_status': 'healthy'
            }
        }
        
        print(f"✅ Discovered {len(self.agents)} agent types")
    
    async def execute_workflow(self, workflow_type: str, context: Dict) -> WorkflowResult:
        """Execute a multi-agent workflow with optimization"""
        workflow_id = f"{workflow_type}_{int(time.time())}"
        start_time = time.time()
        
        print(f"🚀 Starting workflow: {workflow_id}")
        
        # Create tasks based on workflow definition
        tasks = await self.create_workflow_tasks(workflow_type, context, workflow_id)
        
        # Execute tasks with optimal parallelization
        results = await self.execute_tasks_optimized(tasks)
        
        # Calculate metrics
        end_time = time.time()
        total_time = end_time - start_time
        
        completed_tasks = len([r for r in results if r.status == TaskStatus.COMPLETED])
        failed_tasks = len([r for r in results if r.status == TaskStatus.FAILED])
        
        # Calculate parallel efficiency
        total_task_time = sum([(r.end_time - r.start_time) for r in results if r.start_time and r.end_time])
        parallel_efficiency = total_task_time / total_time if total_time > 0 else 0
        
        workflow_result = WorkflowResult(
            workflow_id=workflow_id,
            total_time=total_time,
            tasks_completed=completed_tasks,
            tasks_failed=failed_tasks,
            parallel_efficiency=parallel_efficiency,
            agent_utilization=self.calculate_agent_utilization()
        )
        
        # Update metrics
        self.update_workflow_metrics(workflow_result)
        
        print(f"✅ Completed workflow {workflow_id} in {total_time:.1f}s")
        print(f"   Tasks: {completed_tasks} completed, {failed_tasks} failed")
        print(f"   Parallel efficiency: {parallel_efficiency:.2f}x speedup")
        
        return workflow_result
    
    async def create_workflow_tasks(self, workflow_type: str, context: Dict, workflow_id: str) -> List[Task]:
        """Create tasks for a workflow with dependencies"""
        workflow_config = self.config['workflows'].get(workflow_type, {})
        task_configs = workflow_config.get('tasks', [])
        
        tasks = []
        for i, task_config in enumerate(task_configs):
            task = Task(
                id=f"{workflow_id}_task_{i}",
                type=AgentType(task_config['type']),
                priority=task_config.get('priority', 5),
                data={**context, 'workflow_id': workflow_id},
                dependencies=task_config.get('depends_on', [])
            )
            tasks.append(task)
        
        return tasks
    
    async def execute_tasks_optimized(self, tasks: List[Task]) -> List[Task]:
        """Execute tasks with optimal parallelization and dependency management"""
        completed_tasks = []
        remaining_tasks = tasks.copy()
        
        while remaining_tasks:
            # Find tasks that can be executed (dependencies met)
            ready_tasks = []
            for task in remaining_tasks:
                if self.are_dependencies_met(task, completed_tasks):
                    ready_tasks.append(task)
            
            if not ready_tasks:
                print("⚠️ No ready tasks found - possible circular dependency")
                break
            
            # Group tasks by priority and availability
            execution_groups = self.group_tasks_for_execution(ready_tasks)
            
            # Execute groups in parallel
            group_results = []
            for group in execution_groups:
                if len(group) == 1:
                    # Single task execution
                    result = await self.execute_single_task(group[0])
                    group_results.append(result)
                else:
                    # Parallel execution
                    parallel_results = await asyncio.gather(
                        *[self.execute_single_task(task) for task in group],
                        return_exceptions=True
                    )
                    group_results.extend([r for r in parallel_results if isinstance(r, Task)])
            
            # Update completed and remaining tasks
            for result in group_results:
                completed_tasks.append(result)
                if result in remaining_tasks:
                    remaining_tasks.remove(result)
        
        return completed_tasks
    
    def are_dependencies_met(self, task: Task, completed_tasks: List[Task]) -> bool:
        """Check if task dependencies are satisfied"""
        if not task.dependencies:
            return True
        
        completed_types = [t.type.value for t in completed_tasks if t.status == TaskStatus.COMPLETED]
        return all(dep in completed_types for dep in task.dependencies)
    
    def group_tasks_for_execution(self, tasks: List[Task]) -> List[List[Task]]:
        """Group tasks for optimal parallel execution"""
        # Sort tasks by priority (higher first)
        sorted_tasks = sorted(tasks, key=lambda t: t.priority, reverse=True)
        
        execution_groups = []
        available_capacity = self.get_available_capacity()
        
        current_group = []
        current_capacity_used = {}
        
        for task in sorted_tasks:
            agent_info = self.agents.get(task.type, {})
            required_capacity = 1
            
            # Check if we can add this task to current group
            current_used = current_capacity_used.get(task.type, 0)
            available = available_capacity.get(task.type, 0)
            
            if current_used + required_capacity <= available:
                current_group.append(task)
                current_capacity_used[task.type] = current_used + required_capacity
            else:
                # Start new group if current group is not empty
                if current_group:
                    execution_groups.append(current_group)
                    current_group = [task]
                    current_capacity_used = {task.type: required_capacity}
                else:
                    # Single task that exceeds capacity
                    execution_groups.append([task])
        
        if current_group:
            execution_groups.append(current_group)
        
        return execution_groups
    
    def get_available_capacity(self) -> Dict[AgentType, int]:
        """Get available capacity for each agent type"""
        capacity = {}
        for agent_type, info in self.agents.items():
            total_capacity = info.get('capacity', 1)
            current_load = info.get('current_load', 0)
            capacity[agent_type] = max(0, total_capacity - current_load)
        return capacity
    
    async def execute_single_task(self, task: Task) -> Task:
        """Execute a single task with monitoring and error handling"""
        task.start_time = time.time()
        task.status = TaskStatus.IN_PROGRESS
        
        try:
            print(f"🔄 Executing {task.type.value} task: {task.id}")
            
            # Simulate task execution (in production, this would call actual agents)
            await self.simulate_agent_work(task)
            
            task.status = TaskStatus.COMPLETED
            task.end_time = time.time()
            
            # Update agent load
            if task.type in self.agents:
                self.agents[task.type]['current_load'] -= 1
            
            execution_time = task.end_time - task.start_time
            print(f"✅ Completed {task.type.value} in {execution_time:.1f}s")
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.end_time = time.time()
            task.result = {'error': str(e)}
            
            print(f"❌ Failed {task.type.value}: {e}")
        
        return task
    
    async def simulate_agent_work(self, task: Task):
        """Simulate agent work with realistic timing"""
        # Simulate different execution times for different agent types
        execution_times = {
            AgentType.CODE_REVIEW: (2, 5),      # 2-5 seconds
            AgentType.SECURITY_SCAN: (3, 8),    # 3-8 seconds
            AgentType.TEST_GENERATION: (4, 10), # 4-10 seconds
            AgentType.DOCUMENTATION: (1, 3),    # 1-3 seconds
            AgentType.DEPLOYMENT: (2, 6)        # 2-6 seconds
        }
        
        min_time, max_time = execution_times.get(task.type, (1, 3))
        execution_time = min_time + (max_time - min_time) * 0.5  # Use average
        
        await asyncio.sleep(execution_time)
        
        # Simulate successful result
        task.result = {
            'success': True,
            'agent_type': task.type.value,
            'execution_time': execution_time,
            'data': f"Processed by {task.type.value} agent"
        }
    
    async def task_processor(self):
        """Background task processor for queued tasks"""
        while True:
            try:
                # Process any queued tasks
                await asyncio.sleep(1)  # Simple polling, could use more sophisticated queuing
            except Exception as e:
                print(f"Task processor error: {e}")
                await asyncio.sleep(5)
    
    async def health_monitor(self):
        """Monitor agent health and performance"""
        while True:
            try:
                # Check agent health
                for agent_type, info in self.agents.items():
                    if info['health_status'] != 'healthy':
                        print(f"⚠️ Agent {agent_type.value} is unhealthy")
                
                await asyncio.sleep(30)  # Check every 30 seconds
            except Exception as e:
                print(f"Health monitor error: {e}")
                await asyncio.sleep(60)
    
    def calculate_agent_utilization(self) -> Dict[str, float]:
        """Calculate agent utilization metrics"""
        utilization = {}
        for agent_type, info in self.agents.items():
            capacity = info.get('capacity', 1)
            current_load = info.get('current_load', 0)
            utilization[agent_type.value] = current_load / capacity if capacity > 0 else 0
        return utilization
    
    def update_workflow_metrics(self, result: WorkflowResult):
        """Update overall orchestrator metrics"""
        self.metrics['workflows_processed'] += 1
        self.metrics['total_tasks_executed'] += result.tasks_completed
        
        # Update running average
        current_avg = self.metrics['average_workflow_time']
        count = self.metrics['workflows_processed']
        self.metrics['average_workflow_time'] = (
            (current_avg * (count - 1) + result.total_time) / count
        )
    
    def print_metrics(self):
        """Print orchestrator performance metrics"""
        print("\n📊 Orchestrator Metrics:")
        print(f"   Workflows Processed: {self.metrics['workflows_processed']}")
        print(f"   Total Tasks Executed: {self.metrics['total_tasks_executed']}")
        print(f"   Average Workflow Time: {self.metrics['average_workflow_time']:.1f}s")
        print("   Agent Utilization:")
        for agent_type, utilization in self.calculate_agent_utilization().items():
            print(f"     {agent_type}: {utilization:.1%}")

async def main():
    """Demo multi-agent workflow execution"""
    orchestrator = AgentOrchestrator()
    await orchestrator.initialize()
    
    # Example: Process a pull request
    pr_context = {
        'pr_number': 123,
        'repository': os.getenv('GITHUB_REPOSITORY', 'example/repo'),
        'changed_files': ['src/main.py', 'tests/test_main.py'],
        'author': 'developer'
    }
    
    print("🎯 Executing Pull Request Workflow")
    result = await orchestrator.execute_workflow('pull_request', pr_context)
    
    print(f"\n🎉 Workflow completed with {result.parallel_efficiency:.2f}x speedup")
    
    orchestrator.print_metrics()

if __name__ == "__main__":
    import os
    asyncio.run(main())