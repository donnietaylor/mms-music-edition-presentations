# Workflow Automation Examples

This directory contains complete workflow automation examples that demonstrate speed optimization techniques and best practices following [GitHub Copilot best results guide](https://docs.github.com/en/enterprise-cloud@latest/copilot/tutorials/coding-agent/get-the-best-results).

## 🚀 CI/CD Pipeline Optimizations

### Smart Build Optimization
Automatically determine what needs to be built based on changes:

```yaml
# .github/workflows/smart-build.yml
name: Smart Build and Deploy
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  analyze-changes:
    runs-on: ubuntu-latest
    outputs:
      frontend-changed: ${{ steps.changes.outputs.frontend }}
      backend-changed: ${{ steps.changes.outputs.backend }}
      docs-changed: ${{ steps.changes.outputs.docs }}
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - uses: dorny/paths-filter@v2
        id: changes
        with:
          filters: |
            frontend:
              - 'src/web/**'
              - 'package.json'
              - 'package-lock.json'
            backend:
              - 'src/api/**'
              - 'requirements.txt'
              - 'Dockerfile'
            docs:
              - 'docs/**'
              - '*.md'

  build-frontend:
    needs: analyze-changes
    if: needs.analyze-changes.outputs.frontend-changed == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Frontend
        run: |
          npm ci
          npm run build
          echo "✅ Frontend build completed"

  build-backend:
    needs: analyze-changes
    if: needs.analyze-changes.outputs.backend-changed == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Backend
        run: |
          pip install -r requirements.txt
          python -m pytest
          echo "✅ Backend build completed"

  deploy:
    needs: [analyze-changes, build-frontend, build-backend]
    if: always() && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy Changes
        run: |
          echo "Deploying only changed components..."
          if [ "${{ needs.analyze-changes.outputs.frontend-changed }}" == "true" ]; then
            echo "🚀 Deploying frontend changes"
          fi
          if [ "${{ needs.analyze-changes.outputs.backend-changed }}" == "true" ]; then
            echo "🚀 Deploying backend changes"
          fi
```

## 📋 Issue Management Automation

### Intelligent Issue Triage
Automatically categorize and assign issues:

```python
# issue-triage-bot.py
import json
import re
from typing import Dict, List, Tuple

class IntelligentIssueTriage:
    def __init__(self):
        self.keywords = {
            'bug': ['error', 'bug', 'broken', 'issue', 'problem', 'fail'],
            'feature': ['feature', 'enhancement', 'new', 'add', 'implement'],
            'documentation': ['docs', 'documentation', 'readme', 'guide'],
            'security': ['security', 'vulnerability', 'exploit', 'breach'],
            'performance': ['slow', 'performance', 'optimization', 'speed']
        }
        
        self.priority_indicators = {
            'critical': ['production', 'down', 'outage', 'critical', 'urgent'],
            'high': ['important', 'blocking', 'high priority'],
            'medium': ['moderate', 'medium'],
            'low': ['minor', 'low priority', 'nice to have']
        }
        
        self.team_expertise = {
            'frontend': ['ui', 'react', 'css', 'javascript', 'typescript'],
            'backend': ['api', 'server', 'database', 'python', 'java'],
            'devops': ['deployment', 'ci/cd', 'docker', 'kubernetes'],
            'security': ['auth', 'security', 'vulnerability', 'encryption']
        }

    def analyze_issue(self, title: str, body: str) -> Dict:
        """Analyze issue and provide categorization and assignment suggestions"""
        text = f"{title} {body}".lower()
        
        # Determine category
        category_scores = {}
        for category, keywords in self.keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                category_scores[category] = score
        
        primary_category = max(category_scores.items(), key=lambda x: x[1])[0] if category_scores else 'general'
        
        # Determine priority
        priority = 'medium'  # default
        for pri, indicators in self.priority_indicators.items():
            if any(indicator in text for indicator in indicators):
                priority = pri
                break
        
        # Suggest team assignment
        team_scores = {}
        for team, keywords in self.team_expertise.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                team_scores[team] = score
        
        suggested_team = max(team_scores.items(), key=lambda x: x[1])[0] if team_scores else 'general'
        
        return {
            'category': primary_category,
            'priority': priority,
            'suggested_team': suggested_team,
            'confidence': min(max(category_scores.values()) * 0.2, 1.0) if category_scores else 0.1,
            'labels': self._generate_labels(primary_category, priority, suggested_team)
        }
    
    def _generate_labels(self, category: str, priority: str, team: str) -> List[str]:
        """Generate appropriate labels for the issue"""
        labels = [f"type:{category}", f"priority:{priority}"]
        if team != 'general':
            labels.append(f"team:{team}")
        return labels

# GitHub Action integration
def process_github_issue(issue_data: Dict) -> Dict:
    """Process a GitHub issue webhook and return triage results"""
    triage = IntelligentIssueTriage()
    
    title = issue_data.get('title', '')
    body = issue_data.get('body', '')
    
    analysis = triage.analyze_issue(title, body)
    
    return {
        'issue_number': issue_data.get('number'),
        'analysis': analysis,
        'suggested_actions': [
            f"Add labels: {', '.join(analysis['labels'])}",
            f"Assign to {analysis['suggested_team']} team",
            f"Set priority to {analysis['priority']}"
        ]
    }
```

## ⚡ Performance Optimization Patterns

### Parallel Processing Example
```python
# parallel-processing-example.py
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any

class ParallelWorkflowProcessor:
    def __init__(self, max_workers: int = 10):
        self.max_workers = max_workers
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def process_items_in_parallel(self, items: List[Dict]) -> List[Dict]:
        """Process multiple items concurrently for maximum speed"""
        semaphore = asyncio.Semaphore(self.max_workers)
        
        async def process_single_item(item: Dict) -> Dict:
            async with semaphore:
                # Simulate processing with actual work
                result = await self._process_item(item)
                return {'item_id': item['id'], 'result': result, 'status': 'completed'}
        
        # Execute all items in parallel
        tasks = [process_single_item(item) for item in items]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    'item_id': items[i]['id'],
                    'result': None,
                    'status': 'failed',
                    'error': str(result)
                })
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def _process_item(self, item: Dict) -> Any:
        """Individual item processing logic"""
        # Example: API call, database operation, file processing, etc.
        await asyncio.sleep(0.1)  # Simulate work
        return f"Processed {item.get('name', 'unknown')}"

# Usage example in GitHub Action or automation script
async def main():
    items = [{'id': i, 'name': f'task_{i}'} for i in range(100)]
    
    async with ParallelWorkflowProcessor(max_workers=20) as processor:
        results = await processor.process_items_in_parallel(items)
        
        # Log results
        successful = [r for r in results if r['status'] == 'completed']
        failed = [r for r in results if r['status'] == 'failed']
        
        print(f"✅ Successfully processed: {len(successful)}")
        print(f"❌ Failed to process: {len(failed)}")
        
        return results

if __name__ == "__main__":
    asyncio.run(main())
```

## 🎯 Key Speed Optimization Techniques

1. **Selective Processing**: Only process changed files and their dependencies
2. **Parallel Execution**: Run independent tasks concurrently
3. **Smart Caching**: Cache results and reuse when appropriate
4. **Early Termination**: Stop processing when conditions are met
5. **Resource Pooling**: Reuse connections and resources efficiently

## 📊 Monitoring and Metrics

Track these metrics to measure automation effectiveness:

```yaml
# metrics-config.yaml
automation_metrics:
  speed_improvements:
    - name: "Build Time Reduction"
      baseline: "15 minutes"
      target: "5 minutes"
      current: "6 minutes"
    
    - name: "Issue Triage Time"
      baseline: "30 minutes"
      target: "2 minutes"
      current: "3 minutes"
  
  quality_metrics:
    - name: "Issue Assignment Accuracy"
      target: "90%"
      current: "87%"
    
    - name: "False Positive Rate"
      target: "<5%"
      current: "3%"
  
  efficiency_gains:
    - name: "Developer Time Saved"
      metric: "hours per week"
      current: "12 hours"
    
    - name: "Reduced Manual Tasks"
      metric: "percentage"
      current: "75%"
```

## 🔗 Integration Examples

- [GitHub Actions Integration](./github-actions-examples/)
- [Slack Bot Integration](./slack-bot-examples/)
- [JIRA Automation](./jira-automation-examples/)
- [Microsoft Teams Integration](./teams-integration-examples/)

Each example includes complete code, configuration files, and deployment instructions.