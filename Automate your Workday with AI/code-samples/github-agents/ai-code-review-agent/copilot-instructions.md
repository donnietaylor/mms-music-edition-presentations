# Custom Instructions for AI Code Review Agent

## Project Context
This is an AI-powered code review agent that analyzes pull requests and provides intelligent feedback on code quality, security, and best practices.

## Code Review Specific Guidelines

### Review Analysis Logic
- Focus on security vulnerabilities, performance issues, and maintainability
- Generate constructive feedback with specific improvement suggestions
- Prioritize issues by severity (critical, high, medium, low)
- Include code examples when suggesting improvements

### Expected Code Patterns
```python
class CodeReviewAnalyzer:
    """Analyzes code changes for quality and security issues."""
    
    async def analyze_pull_request(self, pr_data: PullRequestData) -> ReviewResult:
        """Analyze a pull request and generate review comments."""
        issues = []
        
        for file_change in pr_data.changed_files:
            # Security analysis
            security_issues = await self._check_security(file_change)
            issues.extend(security_issues)
            
            # Performance analysis  
            performance_issues = await self._check_performance(file_change)
            issues.extend(performance_issues)
            
            # Code quality analysis
            quality_issues = await self._check_quality(file_change)
            issues.extend(quality_issues)
        
        return ReviewResult(issues=issues, overall_score=self._calculate_score(issues))
```

### Review Comment Templates
When generating review comments, use this structure:
- **Issue Description**: Clear explanation of the problem
- **Impact**: Why this matters (security risk, performance impact, etc.)
- **Suggestion**: Specific improvement recommendation with code example
- **Severity**: Critical/High/Medium/Low classification

### Integration Requirements
- Use GitHub API for pull request operations
- Implement webhook handling for real-time reviews
- Support multiple programming languages
- Cache analysis results to avoid duplicate work

### Performance Optimizations
- Parallel analysis of multiple files
- Incremental analysis for large pull requests
- Smart filtering to focus on changed code sections
- Rate limiting to respect API quotas