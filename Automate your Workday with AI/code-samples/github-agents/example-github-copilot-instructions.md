# Example .github/copilot-instructions.md

This is an example of a repository-wide custom instructions file that teams can place in their `.github/` directory to guide GitHub Copilot across the entire project.

## Repository Context
This repository contains AI-powered automation agents for GitHub workflows. The project uses Python 3.9+, follows async/await patterns, and emphasizes clean architecture with comprehensive testing.

## Project Structure
```
project/
├── agents/               # Core agent implementations
├── shared/              # Shared utilities and models  
├── config/              # Configuration files
├── tests/               # Test suites
└── docs/                # Documentation
```

## Coding Standards

### Python Style Guide
- Follow PEP 8 with 88-character line length (Black formatter)
- Use type hints for all function parameters and return values
- Prefer dataclasses or Pydantic models for structured data
- Use descriptive variable names (avoid abbreviations)

### Example Code Structure
```python
from dataclasses import dataclass
from typing import Dict, List, Optional, Union
import asyncio
import logging

@dataclass
class RequestContext:
    """Context information for processing requests."""
    user_id: str
    request_id: str
    timestamp: float
    metadata: Dict[str, str] = None

class BaseService:
    """Base class for all service implementations."""
    
    def __init__(self, config: ServiceConfig):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
    
    async def process(self, context: RequestContext) -> ServiceResult:
        """Process request with proper error handling and logging."""
        self.logger.info(f"Processing request {context.request_id}")
        
        try:
            result = await self._do_process(context)
            self.logger.info(f"Successfully processed {context.request_id}")
            return result
        except Exception as e:
            self.logger.error(f"Failed to process {context.request_id}: {e}")
            raise ServiceError(f"Processing failed: {e}") from e
    
    async def _do_process(self, context: RequestContext) -> ServiceResult:
        """Override this method in subclasses."""
        raise NotImplementedError
```

### Error Handling Patterns
- Always include comprehensive error handling with try/except blocks
- Use custom exception classes with descriptive names
- Log errors with appropriate context and correlation IDs
- Implement retry logic for transient failures
- Provide meaningful error messages for end users

### Testing Patterns
```python
import pytest
from unittest.mock import AsyncMock, patch

class TestAgentService:
    """Test suite for AgentService class."""
    
    @pytest.fixture
    def service_config(self):
        """Provide test configuration."""
        return ServiceConfig(api_key="test-key", timeout=30)
    
    @pytest.fixture  
    def mock_context(self):
        """Provide test request context."""
        return RequestContext(
            user_id="test-user",
            request_id="test-123",
            timestamp=1234567890.0
        )
    
    @pytest.mark.asyncio
    async def test_successful_processing(self, service_config, mock_context):
        """Test successful request processing."""
        service = AgentService(service_config)
        
        with patch.object(service, '_do_process') as mock_process:
            mock_process.return_value = ServiceResult(status="success")
            
            result = await service.process(mock_context)
            
            assert result.status == "success"
            mock_process.assert_called_once_with(mock_context)
```

### Configuration Management
- Use YAML files for configuration when possible
- Support environment variable overrides
- Validate configuration at startup
- Use Pydantic or similar for configuration models

### API Integration Patterns
- Use httpx or aiohttp for async HTTP clients
- Implement connection pooling and timeout handling
- Add retry logic with exponential backoff
- Include request/response logging for debugging

### Database Patterns
- Use SQLAlchemy with async drivers
- Implement proper connection management
- Use database migrations for schema changes
- Include proper transaction handling

## Security Guidelines
- Never hardcode secrets or API keys
- Use environment variables or secure key management
- Validate all inputs before processing
- Implement proper authentication and authorization
- Log security-relevant events

## Performance Considerations
- Use async/await for I/O operations
- Implement caching where appropriate
- Use connection pooling for external services
- Monitor and log performance metrics
- Consider memory usage in long-running processes

## Documentation Standards
- Include comprehensive docstrings for all public functions
- Use Google-style docstring format
- Document complex business logic with inline comments
- Maintain up-to-date README files
- Include usage examples in docstrings