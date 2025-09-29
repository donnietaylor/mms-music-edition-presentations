# Custom Instructions for Intelligent Issue Triage Agent

## Project Context
This agent automatically triages GitHub issues by analyzing content, assigning labels, setting priorities, and routing to appropriate team members.

## Issue Triage Guidelines

### Classification Logic
Implement intelligent classification based on:
- Issue content analysis using NLP
- Historical patterns and similar issues
- Keyword detection and sentiment analysis
- Integration with project management systems

### Expected Code Patterns
```python
class IssueTriageAgent:
    """Automatically triages and classifies GitHub issues."""
    
    async def process_new_issue(self, issue: GitHubIssue) -> TriageResult:
        """Process a new issue and determine appropriate triage actions."""
        
        # Analyze issue content
        classification = await self._classify_issue_type(issue)
        priority = await self._determine_priority(issue)
        labels = await self._suggest_labels(issue)
        assignee = await self._suggest_assignee(issue, classification)
        
        return TriageResult(
            classification=classification,
            priority=priority,
            suggested_labels=labels,
            suggested_assignee=assignee,
            confidence_score=self._calculate_confidence(issue)
        )
    
    async def _classify_issue_type(self, issue: GitHubIssue) -> IssueType:
        """Classify issue as bug, feature request, documentation, etc."""
        # AI-powered classification logic
        pass
```

### Classification Categories
Support these issue types:
- **Bug Report**: Code defects and errors
- **Feature Request**: New functionality proposals  
- **Documentation**: Documentation improvements
- **Question**: User support and help requests
- **Enhancement**: Improvements to existing features
- **Security**: Security-related issues

### Priority Assignment Rules
```python
PRIORITY_RULES = {
    'critical': ['security vulnerability', 'data loss', 'system crash'],
    'high': ['blocks development', 'affects many users', 'regression'],
    'medium': ['feature request', 'minor bug', 'improvement'],
    'low': ['typo', 'cosmetic issue', 'nice to have']
}
```

### Auto-Assignment Logic
- Route security issues to security team
- Assign documentation issues to technical writers
- Direct UI/UX issues to design team
- Consider team workload and expertise

### Integration Requirements
- Connect with GitHub API for issue management
- Support custom label taxonomies
- Integration with project management tools (Jira, Azure DevOps)
- Webhook support for real-time processing

### Quality Assurance
- Track triage accuracy over time
- Allow manual override of automated decisions
- Provide explanation for triage decisions
- Regular model retraining based on feedback