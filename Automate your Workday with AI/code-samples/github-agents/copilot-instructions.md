# GitHub Copilot Custom Instructions for AI Agents

## General Coding Standards

When generating code for GitHub agents, follow these guidelines:

### Code Style
- Use Python 3.9+ features and type hints
- Follow PEP 8 naming conventions
- Include comprehensive docstrings for all functions and classes
- Use async/await for I/O operations
- Implement proper error handling with try/catch blocks

### Architecture Patterns
- Use dependency injection for external services (OpenAI, GitHub API)
- Implement configuration through YAML files when possible
- Create modular, testable components
- Use dataclasses or Pydantic models for structured data

### Example Code Structure
```python
from dataclasses import dataclass
from typing import Dict, List, Optional
import asyncio
import yaml

@dataclass
class AgentConfig:
    """Configuration for AI agent operations."""
    api_key: str
    timeout: int = 30
    max_retries: int = 3

class BaseAgent:
    """Base class for all AI agents."""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.client = self._initialize_client()
    
    async def process_request(self, request: Dict) -> Dict:
        """Process a request with proper error handling."""
        try:
            # Implementation here
            pass
        except Exception as e:
            logger.error(f"Request processing failed: {e}")
            raise
```

### Error Handling
- Always include comprehensive error handling
- Log errors with appropriate detail levels
- Provide meaningful error messages to users
- Implement retry logic for transient failures

### Performance Considerations
- Use connection pooling for HTTP clients
- Implement caching where appropriate
- Use batch processing for multiple operations
- Monitor and log performance metrics

### Security Best Practices
- Never hardcode API keys or secrets
- Use environment variables for sensitive configuration
- Validate all inputs before processing
- Implement rate limiting for API calls