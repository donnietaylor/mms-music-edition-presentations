# Custom Instructions for AI Documentation Agent

## Project Context
This agent automatically generates and maintains technical documentation by analyzing code repositories and creating comprehensive documentation.

## Documentation Generation Guidelines

### Documentation Types
Generate the following types of documentation:
- README files with project overviews
- API documentation from code comments
- Code architecture diagrams
- Usage examples and tutorials
- Changelog generation from commit history

### Expected Code Patterns
```python
class DocumentationGenerator:
    """Generates various types of documentation from code analysis."""
    
    async def generate_readme(self, repo_analysis: RepoAnalysis) -> ReadmeContent:
        """Generate a comprehensive README file."""
        sections = {
            'overview': self._generate_overview(repo_analysis),
            'installation': self._generate_installation_guide(repo_analysis),
            'usage': self._generate_usage_examples(repo_analysis),
            'api': self._generate_api_docs(repo_analysis),
            'contributing': self._generate_contributing_guide(repo_analysis)
        }
        return ReadmeContent(sections=sections)
    
    async def extract_docstrings(self, file_content: str, language: str) -> List[DocString]:
        """Extract and parse docstrings from source code."""
        # Language-specific parsing logic here
        pass
```

### Documentation Templates
Use structured templates for consistency:

#### README Template Structure
```markdown
# Project Name

## Overview
Brief description of what the project does and its main features.

## Installation
Step-by-step installation instructions.

## Usage
Basic usage examples with code snippets.

## API Reference
Automatically generated API documentation.

## Contributing
Guidelines for contributors.
```

### Code Analysis Requirements
- Parse multiple programming languages (Python, JavaScript, TypeScript, etc.)
- Extract docstrings, comments, and type annotations
- Analyze function signatures and return types
- Identify public APIs vs internal implementation details

### Content Quality Standards
- Use clear, concise language
- Include practical code examples
- Maintain consistent formatting
- Generate up-to-date information from latest code
- Cross-reference related components

### Integration Features
- Watch for code changes and update docs automatically
- Generate documentation in multiple formats (Markdown, HTML, PDF)
- Version documentation alongside code releases
- Support for documentation hosting platforms