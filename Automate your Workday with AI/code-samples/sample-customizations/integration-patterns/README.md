# Integration Patterns for AI Agents

Examples of connecting AI agents with external tools and services, following best practices from the [GitHub Copilot documentation](https://docs.github.com/en/enterprise-cloud@latest/copilot/tutorials/coding-agent/get-the-best-results).

## 🔗 API Integration Examples

### Robust API Client
```python
# robust-api-client.py
import asyncio
import aiohttp
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime, timedelta
import backoff

@dataclass
class APIConfig:
    base_url: str
    api_key: str
    timeout: int = 30
    max_retries: int = 3
    rate_limit: int = 100  # requests per minute

class RobustAPIClient:
    def __init__(self, config: APIConfig):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        self.request_timestamps: List[datetime] = []
    
    async def __aenter__(self):
        headers = {
            'Authorization': f'Bearer {self.config.api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'AI-Agent/1.0'
        }
        
        timeout = aiohttp.ClientTimeout(total=self.config.timeout)
        self.session = aiohttp.ClientSession(
            headers=headers,
            timeout=timeout,
            connector=aiohttp.TCPConnector(limit=10)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def _check_rate_limit(self) -> None:
        """Check and enforce rate limiting"""
        now = datetime.now()
        # Remove timestamps older than 1 minute
        self.request_timestamps = [
            ts for ts in self.request_timestamps 
            if now - ts < timedelta(minutes=1)
        ]
        
        if len(self.request_timestamps) >= self.config.rate_limit:
            sleep_time = 60 - (now - self.request_timestamps[0]).seconds
            if sleep_time > 0:
                print(f"⏳ Rate limit reached, sleeping for {sleep_time}s")
                asyncio.sleep(sleep_time)
    
    @backoff.on_exception(
        backoff.expo,
        (aiohttp.ClientError, asyncio.TimeoutError),
        max_tries=3,
        max_time=300
    )
    async def make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make HTTP request with retry logic and rate limiting"""
        self._check_rate_limit()
        self.request_timestamps.append(datetime.now())
        
        url = f"{self.config.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        async with self.session.request(
            method, 
            url, 
            json=data, 
            params=params
        ) as response:
            response_text = await response.text()
            
            if response.status >= 400:
                error_msg = f"API Error {response.status}: {response_text}"
                print(f"❌ {error_msg}")
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message=error_msg
                )
            
            try:
                return await response.json()
            except json.JSONDecodeError:
                return {'raw_response': response_text}
    
    async def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """GET request"""
        return await self.make_request('GET', endpoint, params=params)
    
    async def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """POST request"""
        return await self.make_request('POST', endpoint, data=data)
    
    async def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """PUT request"""
        return await self.make_request('PUT', endpoint, data=data)
    
    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """DELETE request"""
        return await self.make_request('DELETE', endpoint)

# Example usage with GitHub API
async def github_integration_example():
    """Example of integrating with GitHub API"""
    config = APIConfig(
        base_url="https://api.github.com",
        api_key="your_github_token",
        rate_limit=5000  # GitHub allows 5000 requests per hour
    )
    
    async with RobustAPIClient(config) as client:
        # Get repository information
        repo_info = await client.get("/repos/owner/repo")
        print(f"Repository: {repo_info['name']}")
        print(f"Stars: {repo_info['stargazers_count']}")
        
        # Get recent issues
        issues = await client.get("/repos/owner/repo/issues", 
                                params={"state": "open", "per_page": 5})
        
        for issue in issues:
            print(f"Issue #{issue['number']}: {issue['title']}")
```

## 📊 Database Integration

### Smart Database Operations
```python
# database-integration.py
import asyncio
import aiosqlite
import json
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class ProcessingResult:
    id: Optional[int]
    operation: str
    input_data: str
    result: str
    status: str
    created_at: datetime
    processing_time: float
    metadata: Dict[str, Any]

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection: Optional[aiosqlite.Connection] = None
    
    async def __aenter__(self):
        self.connection = await aiosqlite.connect(self.db_path)
        await self._initialize_tables()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            await self.connection.close()
    
    async def _initialize_tables(self):
        """Create necessary tables"""
        await self.connection.execute('''
            CREATE TABLE IF NOT EXISTS processing_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation TEXT NOT NULL,
                input_data TEXT NOT NULL,
                result TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                processing_time REAL NOT NULL,
                metadata TEXT NOT NULL
            )
        ''')
        
        await self.connection.execute('''
            CREATE INDEX IF NOT EXISTS idx_operation_status 
            ON processing_results(operation, status)
        ''')
        
        await self.connection.execute('''
            CREATE INDEX IF NOT EXISTS idx_created_at 
            ON processing_results(created_at)
        ''')
        
        await self.connection.commit()
    
    async def store_result(self, result: ProcessingResult) -> int:
        """Store processing result in database"""
        cursor = await self.connection.execute('''
            INSERT INTO processing_results 
            (operation, input_data, result, status, created_at, processing_time, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            result.operation,
            result.input_data,
            result.result,
            result.status,
            result.created_at,
            result.processing_time,
            json.dumps(result.metadata)
        ))
        
        await self.connection.commit()
        return cursor.lastrowid
    
    async def get_results_by_operation(
        self, 
        operation: str, 
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[ProcessingResult]:
        """Get results by operation type"""
        query = '''
            SELECT * FROM processing_results 
            WHERE operation = ?
        '''
        params = [operation]
        
        if status:
            query += ' AND status = ?'
            params.append(status)
        
        query += ' ORDER BY created_at DESC LIMIT ?'
        params.append(limit)
        
        cursor = await self.connection.execute(query, params)
        rows = await cursor.fetchall()
        
        results = []
        for row in rows:
            result = ProcessingResult(
                id=row[0],
                operation=row[1],
                input_data=row[2],
                result=row[3],
                status=row[4],
                created_at=datetime.fromisoformat(row[5]),
                processing_time=row[6],
                metadata=json.loads(row[7])
            )
            results.append(result)
        
        return results
    
    async def get_operation_stats(self, operation: str) -> Dict[str, Any]:
        """Get statistics for an operation"""
        cursor = await self.connection.execute('''
            SELECT 
                COUNT(*) as total_count,
                AVG(processing_time) as avg_processing_time,
                MIN(processing_time) as min_processing_time,
                MAX(processing_time) as max_processing_time,
                SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success_count,
                SUM(CASE WHEN status = 'error' THEN 1 ELSE 0 END) as error_count
            FROM processing_results 
            WHERE operation = ?
        ''', (operation,))
        
        row = await cursor.fetchone()
        
        if row[0] == 0:  # No results found
            return {'message': f'No results found for operation: {operation}'}
        
        return {
            'operation': operation,
            'total_count': row[0],
            'avg_processing_time': row[1],
            'min_processing_time': row[2],
            'max_processing_time': row[3],
            'success_count': row[4],
            'error_count': row[5],
            'success_rate': row[4] / row[0] if row[0] > 0 else 0
        }

# Example usage
async def database_integration_example():
    """Example of database integration with AI agent results"""
    async with DatabaseManager('agent_results.db') as db:
        # Store some example results
        for i in range(5):
            result = ProcessingResult(
                id=None,
                operation='code_review',
                input_data=f'file_{i}.py',
                result=f'Review completed with {i} issues found',
                status='success' if i < 4 else 'error',
                created_at=datetime.now(),
                processing_time=0.5 + i * 0.1,
                metadata={'file_size': 1000 + i * 100, 'language': 'python'}
            )
            
            result_id = await db.store_result(result)
            print(f"Stored result with ID: {result_id}")
        
        # Get operation statistics
        stats = await db.get_operation_stats('code_review')
        print(f"Code review stats: {json.dumps(stats, indent=2)}")
        
        # Get recent successful results
        recent_results = await db.get_results_by_operation(
            'code_review', 
            limit=10, 
            status='success'
        )
        
        print(f"Found {len(recent_results)} recent successful results")
```

## 🔔 Webhook Integration

### Webhook Handler
```python
# webhook-handler.py
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import hashlib
import hmac
import json
from typing import Dict, Any, Optional
import asyncio
from datetime import datetime

app = FastAPI()
security = HTTPBearer()

class WebhookProcessor:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.handlers = {}
    
    def verify_signature(self, payload: bytes, signature: str) -> bool:
        """Verify webhook signature for security"""
        expected_signature = hmac.new(
            self.secret_key.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(f"sha256={expected_signature}", signature)
    
    def register_handler(self, event_type: str):
        """Decorator to register event handlers"""
        def decorator(func):
            self.handlers[event_type] = func
            return func
        return decorator
    
    async def process_event(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Process webhook event"""
        if event_type not in self.handlers:
            print(f"⚠️ No handler registered for event type: {event_type}")
            return {'status': 'ignored', 'reason': 'no_handler'}
        
        try:
            handler = self.handlers[event_type]
            result = await handler(payload)
            
            print(f"✅ Successfully processed {event_type} event")
            return {'status': 'success', 'result': result}
            
        except Exception as e:
            print(f"❌ Error processing {event_type} event: {e}")
            return {'status': 'error', 'error': str(e)}

# Initialize webhook processor
webhook_processor = WebhookProcessor(secret_key="your_webhook_secret")

# Register event handlers
@webhook_processor.register_handler('pull_request')
async def handle_pull_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Handle GitHub pull request events"""
    action = payload.get('action')
    pr = payload.get('pull_request', {})
    
    if action == 'opened':
        # Trigger AI code review
        return await trigger_ai_code_review(pr)
    elif action == 'closed' and pr.get('merged'):
        # Update documentation
        return await update_documentation(pr)
    
    return {'message': f'Handled PR {action} event'}

@webhook_processor.register_handler('issues')
async def handle_issues(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Handle GitHub issues events"""
    action = payload.get('action')
    issue = payload.get('issue', {})
    
    if action == 'opened':
        # Auto-triage issue
        return await auto_triage_issue(issue)
    
    return {'message': f'Handled issue {action} event'}

async def trigger_ai_code_review(pr: Dict[str, Any]) -> Dict[str, Any]:
    """Trigger AI-powered code review"""
    # Simulate AI code review process
    await asyncio.sleep(1)  # Simulate processing time
    
    return {
        'action': 'code_review_triggered',
        'pr_number': pr.get('number'),
        'estimated_completion': '5 minutes',
        'review_items': [
            'Security analysis',
            'Performance optimization',
            'Code style checking',
            'Test coverage analysis'
        ]
    }

async def auto_triage_issue(issue: Dict[str, Any]) -> Dict[str, Any]:
    """Auto-triage GitHub issue"""
    title = issue.get('title', '').lower()
    body = issue.get('body', '').lower()
    
    # Simple classification logic
    labels = []
    if any(keyword in title or keyword in body for keyword in ['bug', 'error', 'broken']):
        labels.append('bug')
    if any(keyword in title or keyword in body for keyword in ['feature', 'enhancement']):
        labels.append('enhancement')
    if any(keyword in title or keyword in body for keyword in ['urgent', 'critical']):
        labels.append('high-priority')
    
    return {
        'action': 'issue_triaged',
        'issue_number': issue.get('number'),
        'suggested_labels': labels,
        'assigned_team': 'development' if 'bug' in labels else 'product'
    }

async def update_documentation(pr: Dict[str, Any]) -> Dict[str, Any]:
    """Update documentation after PR merge"""
    # Simulate documentation update
    await asyncio.sleep(2)
    
    return {
        'action': 'documentation_updated',
        'pr_number': pr.get('number'),
        'updated_sections': [
            'API Reference',
            'Change Log',
            'README.md'
        ]
    }

@app.post("/webhook")
async def handle_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    credentials: HTTPAuthorizationCredentials = security
):
    """Handle incoming webhook requests"""
    # Get raw payload for signature verification
    payload = await request.body()
    
    # Verify signature
    signature = request.headers.get('X-Hub-Signature-256', '')
    if not webhook_processor.verify_signature(payload, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Parse JSON payload
    try:
        data = json.loads(payload.decode())
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    
    # Determine event type
    event_type = request.headers.get('X-GitHub-Event', 'unknown')
    
    # Process event in background
    background_tasks.add_task(
        webhook_processor.process_event,
        event_type,
        data
    )
    
    return {
        'status': 'accepted',
        'event_type': event_type,
        'timestamp': datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 🔌 Third-Party Service Integration

### Slack Bot Integration
```python
# slack-integration.py
import asyncio
import aiohttp
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

class SlackBotIntegration:
    def __init__(self, bot_token: str, signing_secret: str):
        self.bot_token = bot_token
        self.signing_secret = signing_secret
        self.base_url = "https://slack.com/api"
    
    async def send_message(
        self, 
        channel: str, 
        text: str, 
        blocks: Optional[List[Dict]] = None,
        thread_ts: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send message to Slack channel"""
        url = f"{self.base_url}/chat.postMessage"
        headers = {
            'Authorization': f'Bearer {self.bot_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'channel': channel,
            'text': text
        }
        
        if blocks:
            payload['blocks'] = blocks
        if thread_ts:
            payload['thread_ts'] = thread_ts
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                return await response.json()
    
    async def create_ai_status_message(
        self, 
        channel: str, 
        operation: str, 
        status: str,
        details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a rich status message about AI operations"""
        
        status_emoji = {
            'running': '⏳',
            'completed': '✅',
            'failed': '❌',
            'warning': '⚠️'
        }
        
        emoji = status_emoji.get(status, '🤖')
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{emoji} AI Agent Status Update"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Operation:*\n{operation}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Status:*\n{status.title()}"
                    }
                ]
            }
        ]
        
        # Add details section
        if details:
            detail_fields = []
            for key, value in details.items():
                detail_fields.append({
                    "type": "mrkdwn",
                    "text": f"*{key.title()}:*\n{value}"
                })
            
            blocks.append({
                "type": "section",
                "fields": detail_fields
            })
        
        # Add timestamp
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                }
            ]
        })
        
        return await self.send_message(
            channel=channel,
            text=f"{emoji} AI Agent: {operation} - {status}",
            blocks=blocks
        )

# Example usage
async def slack_integration_example():
    """Example of Slack integration for AI agent notifications"""
    slack = SlackBotIntegration(
        bot_token="xoxb-your-bot-token",
        signing_secret="your-signing-secret"
    )
    
    # Notify about starting AI code review
    await slack.create_ai_status_message(
        channel="#dev-team",
        operation="AI Code Review",
        status="running",
        details={
            "pull_request": "#123",
            "files_analyzing": "5",
            "estimated_time": "3 minutes"
        }
    )
    
    # Simulate some processing time
    await asyncio.sleep(2)
    
    # Notify about completion
    await slack.create_ai_status_message(
        channel="#dev-team",
        operation="AI Code Review",
        status="completed",
        details={
            "pull_request": "#123",
            "issues_found": "2",
            "suggestions": "7",
            "processing_time": "2.3 seconds"
        }
    )
```

## 📈 Integration Best Practices

### 1. Error Handling and Resilience
- Implement retry logic with exponential backoff
- Use circuit breakers for external services
- Graceful degradation when services are unavailable
- Comprehensive logging and monitoring

### 2. Security
- Always verify webhook signatures
- Use secure token storage (environment variables, key vaults)
- Implement rate limiting to prevent abuse
- Validate all input data

### 3. Performance
- Use connection pooling for HTTP clients
- Implement caching for frequently accessed data
- Process webhooks asynchronously
- Monitor and optimize database queries

### 4. Monitoring and Observability
- Log all integration attempts and results
- Track performance metrics (latency, success rates)
- Set up alerts for integration failures
- Maintain audit trails for compliance

## 🔧 Configuration Management

```yaml
# integration-config.yaml
integrations:
  github:
    api_url: "https://api.github.com"
    webhook_secret: "${GITHUB_WEBHOOK_SECRET}"
    token: "${GITHUB_TOKEN}"
    rate_limit: 5000
    
  slack:
    api_url: "https://slack.com/api"
    bot_token: "${SLACK_BOT_TOKEN}"
    signing_secret: "${SLACK_SIGNING_SECRET}"
    default_channel: "#ai-notifications"
    
  database:
    type: "sqlite"
    path: "./agent_data.db"
    connection_pool_size: 10
    query_timeout: 30
    
  monitoring:
    enable_metrics: true
    metrics_endpoint: "/metrics"
    log_level: "INFO"
    alert_webhook: "${ALERT_WEBHOOK_URL}"

performance:
  async_processing: true
  max_concurrent_requests: 50
  request_timeout: 30
  retry_attempts: 3
  backoff_factor: 2.0
```

These integration patterns provide robust, scalable ways to connect AI agents with external systems while maintaining security, performance, and reliability.