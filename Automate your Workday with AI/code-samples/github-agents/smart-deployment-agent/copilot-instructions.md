# Custom Instructions for Smart Deployment Agent

## Project Context
This agent makes intelligent deployment decisions based on code analysis, testing results, and environmental factors to ensure safe and reliable deployments.

## Deployment Decision Guidelines

### Risk Assessment Framework
Implement comprehensive risk evaluation:
- Code complexity analysis and change impact
- Test coverage and success rates
- Historical deployment success patterns
- Environmental readiness checks

### Expected Code Patterns
```python
class SmartDeploymentAgent:
    """Makes intelligent deployment decisions based on risk assessment."""
    
    async def evaluate_deployment_readiness(self, deployment_request: DeploymentRequest) -> DeploymentDecision:
        """Evaluate if deployment should proceed based on multiple factors."""
        
        # Risk assessment
        risk_score = await self._assess_deployment_risk(deployment_request)
        
        # Environment checks
        env_status = await self._check_environment_health(deployment_request.target_env)
        
        # Quality gates
        quality_checks = await self._evaluate_quality_gates(deployment_request)
        
        # Make decision
        decision = self._make_deployment_decision(risk_score, env_status, quality_checks)
        
        return DeploymentDecision(
            approved=decision.approved,
            risk_level=risk_score.level,
            recommendations=decision.recommendations,
            rollback_plan=self._generate_rollback_plan(deployment_request)
        )
```

### Risk Assessment Factors
Evaluate these deployment risks:
- **Code Changes**: Complexity, size, and critical path impact
- **Test Results**: Coverage, pass rates, and performance benchmarks
- **Dependencies**: External service availability and version compatibility
- **Environment Health**: Resource utilization, recent incidents
- **Historical Data**: Previous deployment success rates at similar times

### Decision Matrix
```python
DEPLOYMENT_RULES = {
    'low_risk': {
        'auto_deploy': True,
        'approval_required': False,
        'rollback_threshold': 'error_rate > 1%'
    },
    'medium_risk': {
        'auto_deploy': False,
        'approval_required': True,
        'additional_monitoring': '30_minutes'
    },
    'high_risk': {
        'auto_deploy': False,
        'approval_required': True,
        'staged_rollout': True,
        'monitoring_period': '2_hours'
    }
}
```

### Deployment Strategies
Implement smart deployment patterns:
- **Blue-Green**: For zero-downtime deployments
- **Canary**: Gradual rollout with monitoring
- **Rolling**: Progressive instance updates
- **Feature Flags**: Runtime feature control

### Monitoring and Rollback
- Real-time health monitoring during deployments
- Automated rollback triggers based on metrics
- Performance regression detection
- Error rate and latency monitoring
- User experience impact assessment

### Integration Requirements
- CI/CD pipeline integration (GitHub Actions, Azure DevOps)
- Infrastructure monitoring tools (Prometheus, DataDog)
- Cloud platform APIs (Azure, AWS, GCP)
- Notification systems (Slack, Teams, email)