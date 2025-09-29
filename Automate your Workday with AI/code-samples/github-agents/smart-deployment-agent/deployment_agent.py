#!/usr/bin/env python3
"""
Smart Deployment Agent
Demonstrates intelligent deployment decisions with risk assessment and automation
"""

import os
import json
import yaml
import asyncio
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import openai
from github import Github
from datetime import datetime, timedelta
import aiohttp
import statistics

class DeploymentStrategy(Enum):
    BLUE_GREEN = "blue_green"
    CANARY = "canary"
    ROLLING = "rolling"
    DIRECT = "direct"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class RiskAssessment:
    overall_risk: RiskLevel
    risk_score: float
    factors: Dict[str, float]
    recommended_strategy: DeploymentStrategy
    additional_checks: List[str]
    rollback_plan: Dict[str, Any]

@dataclass
class DeploymentResult:
    deployment_id: str
    success: bool
    strategy_used: DeploymentStrategy
    deployment_time: float
    risk_assessment: RiskAssessment
    health_checks_passed: int
    health_checks_failed: int
    rollback_triggered: bool

class SmartDeploymentAgent:
    def __init__(self):
        self.github = Github(os.getenv('GITHUB_TOKEN'))
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Load configurations
        self.load_configurations()
        
        # Performance tracking
        self.metrics = {
            'start_time': time.time(),
            'deployments_analyzed': 0,
            'deployments_executed': 0,
            'rollbacks_triggered': 0,
            'successful_deployments': 0,
            'risk_assessments_made': 0
        }
        
        # Deployment history for learning
        self.deployment_history = []
        
    def load_configurations(self):
        """Load deployment configurations and rules"""
        # Default configuration - would load from files in production
        self.config = {
            'risk_rules': {
                'change_factors': {
                    'lines_changed': {'weight': 0.3, 'max_score': 10},
                    'files_changed': {'weight': 0.2, 'max_score': 8},
                    'critical_files': {'weight': 0.4, 'max_score': 15},
                    'test_coverage': {'weight': -0.2, 'max_score': -5},  # Negative = good
                    'complexity_increase': {'weight': 0.3, 'max_score': 12}
                },
                'environmental_factors': {
                    'peak_hours': {'weight': 0.2, 'peak_start': 9, 'peak_end': 17},
                    'recent_failures': {'weight': 0.4, 'lookback_hours': 24},
                    'system_load': {'weight': 0.3, 'threshold': 0.8}
                },
                'risk_thresholds': {
                    'low': 2.0,
                    'medium': 5.0,
                    'high': 8.0,
                    'critical': 10.0
                }
            },
            'deployment_strategies': {
                'blue_green': {
                    'min_risk': 'low',
                    'health_check_duration': 300,  # 5 minutes
                    'traffic_switch_delay': 60
                },
                'canary': {
                    'min_risk': 'medium',
                    'initial_traffic': 0.05,  # 5%
                    'progression_steps': [0.05, 0.10, 0.25, 0.50, 1.0],
                    'step_duration': 600  # 10 minutes per step
                },
                'rolling': {
                    'min_risk': 'low',
                    'batch_size': 2,
                    'batch_delay': 120
                }
            },
            'health_checks': {
                'endpoints': ['/health', '/ready', '/metrics'],
                'timeout': 30,
                'retry_count': 3,
                'success_threshold': 0.95
            },
            'rollback_triggers': {
                'error_rate_increase': 0.05,  # 5% increase
                'response_time_increase': 2.0,  # 2x increase
                'health_check_failures': 3,
                'manual_trigger': True
            }
        }
        
        print("✅ Smart deployment configuration loaded")
    
    async def analyze_deployment_risk(self, pr_data: Dict) -> RiskAssessment:
        """Analyze deployment risk using multiple factors"""
        print("🔍 Analyzing deployment risk...")
        
        start_time = time.time()
        
        # Gather risk factors
        change_factors = await self.analyze_code_changes(pr_data)
        environmental_factors = await self.analyze_environment()
        historical_factors = await self.analyze_historical_data(pr_data)
        
        # Calculate overall risk score
        risk_score = 0
        all_factors = {**change_factors, **environmental_factors, **historical_factors}
        
        for factor, value in all_factors.items():
            risk_score += value
        
        # Determine risk level
        thresholds = self.config['risk_rules']['risk_thresholds']
        if risk_score <= thresholds['low']:
            risk_level = RiskLevel.LOW
        elif risk_score <= thresholds['medium']:
            risk_level = RiskLevel.MEDIUM
        elif risk_score <= thresholds['high']:
            risk_level = RiskLevel.HIGH
        else:
            risk_level = RiskLevel.CRITICAL
        
        # Recommend deployment strategy
        recommended_strategy = self.recommend_deployment_strategy(risk_level, all_factors)
        
        # Generate additional checks and rollback plan
        additional_checks = self.generate_additional_checks(risk_level, all_factors)
        rollback_plan = self.generate_rollback_plan(recommended_strategy)
        
        assessment = RiskAssessment(
            overall_risk=risk_level,
            risk_score=risk_score,
            factors=all_factors,
            recommended_strategy=recommended_strategy,
            additional_checks=additional_checks,
            rollback_plan=rollback_plan
        )
        
        analysis_time = time.time() - start_time
        print(f"✅ Risk analysis completed in {analysis_time:.1f}s")
        print(f"   Risk Level: {risk_level.value}")
        print(f"   Risk Score: {risk_score:.2f}")
        print(f"   Recommended Strategy: {recommended_strategy.value}")
        
        self.metrics['risk_assessments_made'] += 1
        return assessment
    
    async def analyze_code_changes(self, pr_data: Dict) -> Dict[str, float]:
        """Analyze code changes for risk factors"""
        factors = {}
        
        # Lines changed factor
        lines_changed = pr_data.get('additions', 0) + pr_data.get('deletions', 0)
        factors['lines_changed'] = min(lines_changed / 100, 10) * 0.3
        
        # Files changed factor
        files_changed = len(pr_data.get('changed_files', []))
        factors['files_changed'] = min(files_changed / 20, 8) * 0.2
        
        # Critical files factor
        critical_patterns = ['src/auth/', 'src/payment/', 'src/security/', 'database/']
        critical_files = sum(1 for file in pr_data.get('changed_files', []) 
                           if any(pattern in file for pattern in critical_patterns))
        factors['critical_files'] = min(critical_files * 3, 15) * 0.4
        
        # Test coverage factor (negative = good)
        has_tests = any('test' in file for file in pr_data.get('changed_files', []))
        factors['test_coverage'] = -2 if has_tests else 3
        
        # Use AI to assess complexity if available
        if pr_data.get('diff_content'):
            complexity_score = await self.assess_complexity_with_ai(pr_data['diff_content'])
            factors['complexity_increase'] = complexity_score * 0.3
        
        return factors
    
    async def assess_complexity_with_ai(self, diff_content: str) -> float:
        """Use AI to assess code complexity changes"""
        try:
            prompt = f"""
Analyze this code diff for complexity changes and deployment risk:

{diff_content[:2000]}...

Rate the complexity and risk on a scale of 0-10:
- 0-2: Simple changes (config, docs, simple fixes)
- 3-5: Moderate changes (new features, refactoring)
- 6-8: Complex changes (architecture changes, new integrations)
- 9-10: High-risk changes (security, payment, core infrastructure)

Respond with just a number (0-10).
"""
            
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
                temperature=0.1
            )
            
            # Extract numeric score
            content = response.choices[0].message.content.strip()
            return float(content) if content.isdigit() else 5.0
            
        except Exception as e:
            print(f"   Warning: AI complexity assessment failed: {e}")
            return 5.0  # Default medium complexity
    
    async def analyze_environment(self) -> Dict[str, float]:
        """Analyze environmental factors for deployment risk"""
        factors = {}
        
        # Peak hours factor
        current_hour = datetime.now().hour
        peak_config = self.config['risk_rules']['environmental_factors']['peak_hours']
        
        if peak_config['peak_start'] <= current_hour <= peak_config['peak_end']:
            factors['peak_hours'] = 2.0 * peak_config['weight']
        else:
            factors['peak_hours'] = 0.0
        
        # Recent failures factor
        recent_failures = await self.get_recent_deployment_failures()
        factors['recent_failures'] = min(recent_failures * 1.5, 5.0) * 0.4
        
        # System load factor (simulated - would query actual monitoring)
        system_load = await self.get_system_load()
        load_threshold = self.config['risk_rules']['environmental_factors']['system_load']['threshold']
        
        if system_load > load_threshold:
            factors['system_load'] = (system_load - load_threshold) * 10 * 0.3
        else:
            factors['system_load'] = 0.0
        
        return factors
    
    async def analyze_historical_data(self, pr_data: Dict) -> Dict[str, float]:
        """Analyze historical deployment data for risk patterns"""
        factors = {}
        
        # Author history factor
        author = pr_data.get('author', 'unknown')
        author_success_rate = await self.get_author_success_rate(author)
        
        if author_success_rate < 0.8:  # Less than 80% success rate
            factors['author_history'] = (0.8 - author_success_rate) * 5
        else:
            factors['author_history'] = 0.0
        
        # Similar change history
        similar_changes = await self.find_similar_changes(pr_data)
        if similar_changes:
            avg_success_rate = statistics.mean([c['success'] for c in similar_changes])
            if avg_success_rate < 0.9:
                factors['similar_changes'] = (0.9 - avg_success_rate) * 3
            else:
                factors['similar_changes'] = 0.0
        else:
            factors['similar_changes'] = 1.0  # Unknown = slight risk
        
        return factors
    
    async def get_recent_deployment_failures(self) -> int:
        """Get count of recent deployment failures"""
        # Simulate querying deployment history
        # In production, this would query your deployment database
        cutoff_time = datetime.now() - timedelta(hours=24)
        
        failures = 0
        for deployment in self.deployment_history:
            if deployment.get('timestamp', datetime.min) > cutoff_time:
                if not deployment.get('success', True):
                    failures += 1
        
        return min(failures, 5)  # Cap at 5 for scoring
    
    async def get_system_load(self) -> float:
        """Get current system load (simulated)"""
        # In production, this would query actual monitoring systems
        import random
        return random.uniform(0.3, 0.9)  # Simulate load between 30-90%
    
    async def get_author_success_rate(self, author: str) -> float:
        """Get historical success rate for author"""
        # Simulate author success rate lookup
        # In production, this would query deployment history
        author_deployments = [d for d in self.deployment_history if d.get('author') == author]
        
        if not author_deployments:
            return 0.85  # Default decent success rate for unknown authors
        
        successful = sum(1 for d in author_deployments if d.get('success', False))
        return successful / len(author_deployments)
    
    async def find_similar_changes(self, pr_data: Dict) -> List[Dict]:
        """Find similar historical changes for risk assessment"""
        # Simulate finding similar changes
        # In production, this would use ML to find similar code changes
        return []  # Simplified for demo
    
    def recommend_deployment_strategy(self, risk_level: RiskLevel, factors: Dict[str, float]) -> DeploymentStrategy:
        """Recommend deployment strategy based on risk assessment"""
        strategies = self.config['deployment_strategies']
        
        if risk_level == RiskLevel.CRITICAL:
            return DeploymentStrategy.CANARY  # Most careful approach
        elif risk_level == RiskLevel.HIGH:
            if factors.get('critical_files', 0) > 5:
                return DeploymentStrategy.CANARY
            else:
                return DeploymentStrategy.BLUE_GREEN
        elif risk_level == RiskLevel.MEDIUM:
            return DeploymentStrategy.BLUE_GREEN
        else:  # LOW risk
            if factors.get('lines_changed', 0) < 1:  # Very small changes
                return DeploymentStrategy.DIRECT
            else:
                return DeploymentStrategy.ROLLING
    
    def generate_additional_checks(self, risk_level: RiskLevel, factors: Dict[str, float]) -> List[str]:
        """Generate additional checks based on risk factors"""
        checks = []
        
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            checks.extend([
                "Extended health check duration",
                "Manual approval required",
                "Enhanced monitoring",
                "Database backup verification"
            ])
        
        if factors.get('critical_files', 0) > 0:
            checks.append("Security team approval required")
        
        if factors.get('peak_hours', 0) > 0:
            checks.append("Consider delaying until off-peak hours")
        
        if factors.get('recent_failures', 0) > 2:
            checks.append("Review recent failure patterns")
        
        return checks
    
    def generate_rollback_plan(self, strategy: DeploymentStrategy) -> Dict[str, Any]:
        """Generate rollback plan based on deployment strategy"""
        base_plan = {
            'automated': True,
            'max_rollback_time': 300,  # 5 minutes
            'health_check_failures_threshold': 3,
            'error_rate_threshold': 0.05
        }
        
        if strategy == DeploymentStrategy.BLUE_GREEN:
            base_plan.update({
                'method': 'traffic_switch',
                'rollback_time': 30,  # Very fast
                'verification_steps': ['health_check', 'smoke_test']
            })
        elif strategy == DeploymentStrategy.CANARY:
            base_plan.update({
                'method': 'traffic_reduction',
                'rollback_time': 60,
                'verification_steps': ['metrics_check', 'error_rate_check', 'performance_check']
            })
        elif strategy == DeploymentStrategy.ROLLING:
            base_plan.update({
                'method': 'service_restart',
                'rollback_time': 180,
                'verification_steps': ['service_health', 'dependency_check']
            })
        
        return base_plan
    
    async def execute_deployment(self, assessment: RiskAssessment, deployment_config: Dict) -> DeploymentResult:
        """Execute deployment based on risk assessment"""
        deployment_id = f"deploy_{int(time.time())}"
        start_time = time.time()
        
        print(f"🚀 Executing deployment: {deployment_id}")
        print(f"   Strategy: {assessment.recommended_strategy.value}")
        print(f"   Risk Level: {assessment.overall_risk.value}")
        
        try:
            # Execute based on strategy
            success = await self.execute_strategy(assessment.recommended_strategy, deployment_config)
            
            # Run health checks
            health_results = await self.run_health_checks()
            
            # Check if rollback is needed
            rollback_triggered = await self.check_rollback_conditions(health_results)
            
            if rollback_triggered:
                await self.execute_rollback(assessment.rollback_plan)
                success = False
            
            deployment_time = time.time() - start_time
            
            result = DeploymentResult(
                deployment_id=deployment_id,
                success=success and not rollback_triggered,
                strategy_used=assessment.recommended_strategy,
                deployment_time=deployment_time,
                risk_assessment=assessment,
                health_checks_passed=health_results['passed'],
                health_checks_failed=health_results['failed'],
                rollback_triggered=rollback_triggered
            )
            
            # Update metrics
            self.metrics['deployments_executed'] += 1
            if result.success:
                self.metrics['successful_deployments'] += 1
            if rollback_triggered:
                self.metrics['rollbacks_triggered'] += 1
            
            # Store in history for learning
            self.deployment_history.append({
                'deployment_id': deployment_id,
                'success': result.success,
                'strategy': assessment.recommended_strategy.value,
                'risk_score': assessment.risk_score,
                'timestamp': datetime.now()
            })
            
            print(f"✅ Deployment {deployment_id} completed in {deployment_time:.1f}s")
            print(f"   Success: {result.success}")
            print(f"   Health Checks: {health_results['passed']}/{health_results['passed'] + health_results['failed']}")
            
            return result
            
        except Exception as e:
            print(f"❌ Deployment {deployment_id} failed: {e}")
            
            # Always try rollback on exception
            await self.execute_rollback(assessment.rollback_plan)
            
            return DeploymentResult(
                deployment_id=deployment_id,
                success=False,
                strategy_used=assessment.recommended_strategy,
                deployment_time=time.time() - start_time,
                risk_assessment=assessment,
                health_checks_passed=0,
                health_checks_failed=1,
                rollback_triggered=True
            )
    
    async def execute_strategy(self, strategy: DeploymentStrategy, config: Dict) -> bool:
        """Execute specific deployment strategy"""
        print(f"   🔄 Executing {strategy.value} deployment...")
        
        if strategy == DeploymentStrategy.BLUE_GREEN:
            return await self.execute_blue_green_deployment(config)
        elif strategy == DeploymentStrategy.CANARY:
            return await self.execute_canary_deployment(config)
        elif strategy == DeploymentStrategy.ROLLING:
            return await self.execute_rolling_deployment(config)
        elif strategy == DeploymentStrategy.DIRECT:
            return await self.execute_direct_deployment(config)
        else:
            return False
    
    async def execute_blue_green_deployment(self, config: Dict) -> bool:
        """Execute blue-green deployment"""
        # Simulate blue-green deployment steps
        steps = [
            "Deploy to green environment",
            "Run health checks on green",
            "Switch traffic to green",
            "Monitor green environment",
            "Decommission blue environment"
        ]
        
        for step in steps:
            print(f"     - {step}")
            await asyncio.sleep(1)  # Simulate work
        
        return True  # Simulate success
    
    async def execute_canary_deployment(self, config: Dict) -> bool:
        """Execute canary deployment"""
        strategy_config = self.config['deployment_strategies']['canary']
        steps = strategy_config['progression_steps']
        
        for i, traffic_percent in enumerate(steps):
            print(f"     - Canary step {i+1}: {traffic_percent*100:.0f}% traffic")
            
            # Simulate deployment step
            await asyncio.sleep(2)
            
            # Check health at each step
            health = await self.run_health_checks()
            if health['failed'] > 0:
                print(f"     ❌ Health check failed at {traffic_percent*100:.0f}% traffic")
                return False
        
        return True
    
    async def execute_rolling_deployment(self, config: Dict) -> bool:
        """Execute rolling deployment"""
        # Simulate rolling deployment
        batch_size = self.config['deployment_strategies']['rolling']['batch_size']
        total_instances = config.get('instances', 6)
        
        for batch_start in range(0, total_instances, batch_size):
            batch_end = min(batch_start + batch_size, total_instances)
            print(f"     - Deploying instances {batch_start+1}-{batch_end}")
            
            await asyncio.sleep(1.5)  # Simulate deployment time
            
            # Health check after each batch
            health = await self.run_health_checks()
            if health['failed'] > 1:  # Allow some failures in rolling
                return False
        
        return True
    
    async def execute_direct_deployment(self, config: Dict) -> bool:
        """Execute direct deployment (for low-risk changes)"""
        print(f"     - Direct deployment to production")
        await asyncio.sleep(0.5)  # Very fast for low-risk changes
        return True
    
    async def run_health_checks(self) -> Dict[str, int]:
        """Run comprehensive health checks"""
        endpoints = self.config['health_checks']['endpoints']
        timeout = self.config['health_checks']['timeout']
        
        passed = 0
        failed = 0
        
        # Simulate health checks
        for endpoint in endpoints:
            try:
                # In production, this would make actual HTTP requests
                await asyncio.sleep(0.1)  # Simulate check time
                
                # Simulate 95% success rate
                import random
                if random.random() < 0.95:
                    passed += 1
                else:
                    failed += 1
                    print(f"     ⚠️ Health check failed: {endpoint}")
                    
            except Exception as e:
                failed += 1
                print(f"     ❌ Health check error for {endpoint}: {e}")
        
        return {'passed': passed, 'failed': failed}
    
    async def check_rollback_conditions(self, health_results: Dict) -> bool:
        """Check if rollback conditions are met"""
        triggers = self.config['rollback_triggers']
        
        # Health check failures
        if health_results['failed'] >= triggers['health_check_failures']:
            print("   🔄 Rollback triggered: Too many health check failures")
            return True
        
        # Simulate other rollback conditions
        # In production, these would check actual metrics
        
        return False
    
    async def execute_rollback(self, rollback_plan: Dict):
        """Execute rollback according to plan"""
        print("   🔄 Executing rollback...")
        
        method = rollback_plan.get('method', 'unknown')
        rollback_time = rollback_plan.get('rollback_time', 60)
        
        print(f"     Method: {method}")
        print(f"     Estimated time: {rollback_time}s")
        
        # Simulate rollback execution
        await asyncio.sleep(min(rollback_time / 10, 3))  # Simulate rollback work
        
        print("   ✅ Rollback completed")
    
    def print_metrics(self):
        """Print deployment agent metrics"""
        total_time = time.time() - self.metrics['start_time']
        success_rate = (self.metrics['successful_deployments'] / 
                       max(self.metrics['deployments_executed'], 1)) * 100
        
        print("\n📊 Smart Deployment Agent Metrics:")
        print(f"   Total Time: {total_time:.1f}s")
        print(f"   Risk Assessments: {self.metrics['risk_assessments_made']}")
        print(f"   Deployments Executed: {self.metrics['deployments_executed']}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Rollbacks Triggered: {self.metrics['rollbacks_triggered']}")

async def main():
    """Demo smart deployment agent"""
    # Sample PR data for testing
    pr_data = {
        'number': 123,
        'title': "Add user authentication feature",
        'author': 'developer',
        'additions': 150,
        'deletions': 20,
        'changed_files': [
            'src/auth/authentication.py',
            'src/auth/middleware.py',
            'tests/test_auth.py',
            'docs/authentication.md'
        ],
        'diff_content': "Sample diff content..."
    }
    
    deployment_config = {
        'environment': 'production',
        'instances': 6,
        'health_check_urls': ['https://api.example.com/health'],
        'monitoring_enabled': True
    }
    
    agent = SmartDeploymentAgent()
    
    print("🤖 Smart Deployment Agent Starting...")
    
    # Analyze deployment risk
    assessment = await agent.analyze_deployment_risk(pr_data)
    
    # Execute deployment if risk is acceptable
    if assessment.overall_risk != RiskLevel.CRITICAL:
        result = await agent.execute_deployment(assessment, deployment_config)
        
        print(f"\n🎉 Deployment Result:")
        print(f"   ID: {result.deployment_id}")
        print(f"   Success: {result.success}")
        print(f"   Strategy: {result.strategy_used.value}")
        print(f"   Time: {result.deployment_time:.1f}s")
        
    else:
        print("\n⚠️ Deployment blocked due to critical risk level")
        print("   Additional approvals required")
    
    agent.print_metrics()

if __name__ == "__main__":
    asyncio.run(main())