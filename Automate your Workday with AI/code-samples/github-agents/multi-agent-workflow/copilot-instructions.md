# Custom Instructions for Multi-Agent Workflow System

## Project Context
This system coordinates multiple AI agents to work together on complex tasks, implementing communication patterns, task delegation, and parallel processing optimization.

## Multi-Agent Architecture Guidelines

### Agent Coordination Patterns
Implement these coordination mechanisms:
- **Publisher-Subscriber**: Event-driven communication between agents
- **Request-Response**: Direct agent-to-agent communication
- **Workflow Orchestration**: Centralized task management
- **Event Sourcing**: State management through event history

### Expected Code Patterns
```python
class MultiAgentWorkflow:
    """Coordinates multiple AI agents in a workflow system."""
    
    def __init__(self):
        self.agents = {}
        self.message_bus = MessageBus()
        self.workflow_engine = WorkflowEngine()
        self.state_manager = StateManager()
    
    async def execute_workflow(self, workflow_definition: WorkflowDefinition) -> WorkflowResult:
        """Execute a multi-agent workflow with proper coordination."""
        
        # Initialize workflow state
        workflow_state = await self.state_manager.initialize_workflow(workflow_definition)
        
        # Execute workflow steps
        for step in workflow_definition.steps:
            if step.execution_type == 'parallel':
                results = await self._execute_parallel_tasks(step.tasks, workflow_state)
            else:
                results = await self._execute_sequential_tasks(step.tasks, workflow_state)
            
            # Update workflow state with results
            workflow_state = await self.state_manager.update_state(workflow_state, results)
        
        return WorkflowResult(
            status='completed',
            final_state=workflow_state,
            execution_metrics=self._collect_metrics()
        )
```

### Agent Communication Protocol
```python
@dataclass
class AgentMessage:
    """Standard message format for inter-agent communication."""
    sender_id: str
    receiver_id: str
    message_type: str
    payload: Dict
    correlation_id: str
    timestamp: float
    priority: int = 1

class MessageBus:
    """Handles message routing between agents."""
    
    async def publish(self, message: AgentMessage):
        """Publish message to interested subscribers."""
        pass
    
    async def subscribe(self, agent_id: str, message_types: List[str]):
        """Subscribe agent to specific message types."""
        pass
```

### Task Delegation Strategy
Implement intelligent task assignment:
- **Capability Matching**: Assign tasks based on agent specializations
- **Load Balancing**: Distribute work across available agents
- **Priority Queuing**: Handle high-priority tasks first
- **Failure Recovery**: Reassign tasks when agents fail

### Parallel Processing Optimization
```python
class ParallelExecutor:
    """Optimizes parallel execution of agent tasks."""
    
    async def execute_tasks_in_parallel(self, tasks: List[Task], max_concurrency: int = 10):
        """Execute multiple tasks concurrently with controlled parallelism."""
        semaphore = asyncio.Semaphore(max_concurrency)
        
        async def bounded_task(task):
            async with semaphore:
                return await self._execute_single_task(task)
        
        return await asyncio.gather(*[bounded_task(task) for task in tasks])
```

### Error Handling and Recovery
- **Circuit Breaker**: Prevent cascade failures
- **Retry Logic**: Automatic retry with exponential backoff
- **Graceful Degradation**: Continue workflow with reduced functionality
- **Dead Letter Queue**: Handle permanently failed tasks

### State Management
- **Persistent State**: Store workflow state in reliable storage
- **State Snapshots**: Checkpoint workflow progress
- **State Recovery**: Resume workflows from last checkpoint
- **Conflict Resolution**: Handle concurrent state modifications

### Monitoring and Observability
- Track agent performance and availability
- Monitor message flow and latency
- Generate workflow execution reports
- Alert on workflow failures or performance degradation