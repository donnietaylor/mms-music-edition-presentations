#!/usr/bin/env python3
"""
AI Documentation Generation Agent
Demonstrates intelligent documentation automation with speed optimizations
"""

import os
import ast
import json
import yaml
import asyncio
import time
from typing import Dict, List, Any, Optional
from pathlib import Path
import openai
from github import Github
import hashlib
import re
from dataclasses import dataclass

@dataclass
class DocumentationSection:
    title: str
    content: str
    section_type: str
    priority: int
    file_references: List[str]
    last_updated: float

class DocumentationAgent:
    def __init__(self):
        self.github = Github(os.getenv('GITHUB_TOKEN'))
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Load configurations
        self.load_configurations()
        
        # Performance tracking
        self.metrics = {
            'start_time': time.time(),
            'files_analyzed': 0,
            'docs_generated': 0,
            'sections_updated': 0,
            'cache_hits': 0,
            'template_compilations': 0
        }
        
        # Content cache
        self.content_cache = {}
        self.template_cache = {}
    
    def load_configurations(self):
        """Load documentation generation configurations"""
        # Default configuration - would load from files in production
        self.config = {
            'templates': {
                'readme': {
                    'sections': ['overview', 'installation', 'usage', 'api', 'contributing'],
                    'required_info': ['name', 'description', 'installation_method'],
                    'optional_info': ['badges', 'screenshots', 'examples']
                },
                'api_docs': {
                    'formats': ['markdown', 'html'],
                    'include_examples': True,
                    'group_by': 'module'
                }
            },
            'extraction_patterns': {
                'python': {
                    'class_docstring': r'class\s+(\w+).*?:\s*"""(.*?)"""',
                    'function_docstring': r'def\s+(\w+).*?:\s*"""(.*?)"""',
                    'module_docstring': r'^"""(.*?)"""'
                },
                'javascript': {
                    'function_comment': r'/\*\*(.*?)\*/\s*function\s+(\w+)',
                    'class_comment': r'/\*\*(.*?)\*/\s*class\s+(\w+)'
                }
            },
            'generation_rules': {
                'update_triggers': ['code_changes', 'new_files', 'config_changes'],
                'batch_processing': True,
                'parallel_sections': True,
                'cache_duration': 3600  # 1 hour
            }
        }
        
        print("✅ Documentation configuration loaded")
    
    async def analyze_project_structure(self, repo_path: str) -> Dict[str, Any]:
        """Analyze project structure to understand documentation needs"""
        print("🔍 Analyzing project structure...")
        
        structure = {
            'languages': set(),
            'frameworks': set(),
            'project_type': 'unknown',
            'has_tests': False,
            'has_docs': False,
            'api_endpoints': [],
            'main_modules': [],
            'dependencies': {}
        }
        
        # Analyze files in parallel for speed
        analysis_tasks = []
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                file_path = os.path.join(root, file)
                analysis_tasks.append(self.analyze_file(file_path, structure))
        
        if analysis_tasks:
            await asyncio.gather(*analysis_tasks, return_exceptions=True)
        
        # Determine project type
        structure['project_type'] = self.determine_project_type(structure)
        
        print(f"   Languages: {', '.join(structure['languages'])}")
        print(f"   Project type: {structure['project_type']}")
        print(f"   Has tests: {structure['has_tests']}")
        
        return structure
    
    async def analyze_file(self, file_path: str, structure: Dict):
        """Analyze individual file for documentation extraction"""
        try:
            file_ext = Path(file_path).suffix.lower()
            
            # Identify language
            lang_map = {
                '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
                '.java': 'java', '.cpp': 'cpp', '.cs': 'csharp',
                '.go': 'go', '.rs': 'rust', '.rb': 'ruby'
            }
            
            if file_ext in lang_map:
                structure['languages'].add(lang_map[file_ext])
            
            # Check for framework indicators
            filename = Path(file_path).name.lower()
            if 'test' in filename or filename.startswith('test_'):
                structure['has_tests'] = True
            
            if filename in ['readme.md', 'docs', 'documentation']:
                structure['has_docs'] = True
            
            # Extract code documentation
            if file_ext == '.py':
                await self.extract_python_docs(file_path, structure)
            elif file_ext in ['.js', '.ts']:
                await self.extract_javascript_docs(file_path, structure)
            
        except Exception as e:
            print(f"   Warning: Could not analyze {file_path}: {e}")
    
    async def extract_python_docs(self, file_path: str, structure: Dict):
        """Extract documentation from Python files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST for better extraction
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    if ast.get_docstring(node):
                        structure['main_modules'].append({
                            'type': 'class',
                            'name': node.name,
                            'docstring': ast.get_docstring(node),
                            'file': file_path
                        })
                
                elif isinstance(node, ast.FunctionDef):
                    if ast.get_docstring(node) and not node.name.startswith('_'):
                        structure['main_modules'].append({
                            'type': 'function',
                            'name': node.name,
                            'docstring': ast.get_docstring(node),
                            'file': file_path
                        })
            
        except Exception as e:
            print(f"   Warning: Could not parse Python file {file_path}: {e}")
    
    async def extract_javascript_docs(self, file_path: str, structure: Dict):
        """Extract documentation from JavaScript/TypeScript files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract JSDoc comments
            jsdoc_pattern = r'/\*\*(.*?)\*/\s*(function|class|const|let|var)\s+(\w+)'
            matches = re.finditer(jsdoc_pattern, content, re.DOTALL)
            
            for match in matches:
                doc_comment = match.group(1).strip()
                item_type = match.group(2)
                item_name = match.group(3)
                
                structure['main_modules'].append({
                    'type': item_type,
                    'name': item_name,
                    'docstring': doc_comment,
                    'file': file_path
                })
                
        except Exception as e:
            print(f"   Warning: Could not parse JavaScript file {file_path}: {e}")
    
    def determine_project_type(self, structure: Dict) -> str:
        """Determine project type based on analysis"""
        languages = structure['languages']
        
        if 'python' in languages:
            if any('flask' in str(dep) or 'django' in str(dep) for dep in structure.get('dependencies', {})):
                return 'python_web'
            elif structure['has_tests']:
                return 'python_library'
            else:
                return 'python_script'
        
        elif 'javascript' in languages or 'typescript' in languages:
            return 'javascript_project'
        
        elif 'java' in languages:
            return 'java_project'
        
        return 'generic'
    
    async def generate_documentation(self, repo_path: str, doc_types: List[str]) -> Dict[str, DocumentationSection]:
        """Generate documentation with speed optimizations"""
        print(f"📚 Generating documentation for: {', '.join(doc_types)}")
        
        # Analyze project first
        project_structure = await self.analyze_project_structure(repo_path)
        
        # Generate documentation sections in parallel
        generation_tasks = []
        for doc_type in doc_types:
            task = self.generate_single_doc_type(doc_type, project_structure, repo_path)
            generation_tasks.append(task)
        
        # Wait for all generation tasks
        results = await asyncio.gather(*generation_tasks, return_exceptions=True)
        
        # Combine results
        documentation = {}
        for i, result in enumerate(results):
            if isinstance(result, dict):
                documentation.update(result)
            else:
                print(f"   Warning: Failed to generate {doc_types[i]}: {result}")
        
        return documentation
    
    async def generate_single_doc_type(self, doc_type: str, structure: Dict, repo_path: str) -> Dict[str, DocumentationSection]:
        """Generate a single type of documentation efficiently"""
        cache_key = f"{doc_type}_{hashlib.md5(str(structure).encode()).hexdigest()}"
        
        # Check cache first
        if cache_key in self.content_cache:
            cache_entry = self.content_cache[cache_key]
            if time.time() - cache_entry['timestamp'] < self.config['generation_rules']['cache_duration']:
                print(f"   💾 Cache hit for {doc_type}")
                self.metrics['cache_hits'] += 1
                return cache_entry['content']
        
        print(f"   🔄 Generating {doc_type} documentation...")
        start_time = time.time()
        
        if doc_type == 'readme':
            content = await self.generate_readme(structure, repo_path)
        elif doc_type == 'api_docs':
            content = await self.generate_api_docs(structure, repo_path)
        elif doc_type == 'changelog':
            content = await self.generate_changelog(structure, repo_path)
        else:
            content = {}
        
        # Cache the result
        self.content_cache[cache_key] = {
            'content': content,
            'timestamp': time.time()
        }
        
        generation_time = time.time() - start_time
        print(f"   ✅ Generated {doc_type} in {generation_time:.1f}s")
        
        self.metrics['docs_generated'] += 1
        return content
    
    async def generate_readme(self, structure: Dict, repo_path: str) -> Dict[str, DocumentationSection]:
        """Generate README.md with AI assistance"""
        
        # Create context for AI generation
        context = {
            'project_type': structure['project_type'],
            'languages': list(structure['languages']),
            'has_tests': structure['has_tests'],
            'main_modules': structure['main_modules'][:5],  # Limit for speed
            'repo_path': repo_path
        }
        
        prompt = f"""
Generate a comprehensive README.md for this project:

Project Type: {context['project_type']}
Languages: {', '.join(context['languages'])}
Has Tests: {context['has_tests']}

Main Components:
{self.format_modules_for_prompt(context['main_modules'])}

Create a professional README with these sections:
1. Project overview and description
2. Installation instructions
3. Usage examples
4. API documentation (if applicable)
5. Contributing guidelines

Make it clear, concise, and developer-friendly.
"""
        
        try:
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.3
            )
            
            readme_content = response.choices[0].message.content
            
            return {
                'readme': DocumentationSection(
                    title="README",
                    content=readme_content,
                    section_type="readme",
                    priority=10,
                    file_references=[repo_path],
                    last_updated=time.time()
                )
            }
            
        except Exception as e:
            print(f"   ❌ Failed to generate README: {e}")
            return {}
    
    async def generate_api_docs(self, structure: Dict, repo_path: str) -> Dict[str, DocumentationSection]:
        """Generate API documentation from code analysis"""
        
        api_sections = {}
        
        # Group modules by file for better organization
        modules_by_file = {}
        for module in structure['main_modules']:
            file_path = module['file']
            if file_path not in modules_by_file:
                modules_by_file[file_path] = []
            modules_by_file[file_path].append(module)
        
        # Generate documentation for each file
        for file_path, modules in modules_by_file.items():
            relative_path = os.path.relpath(file_path, repo_path)
            
            # Create API documentation for this file
            api_content = f"# API Documentation - {relative_path}\n\n"
            
            for module in modules:
                api_content += f"## {module['name']} ({module['type']})\n\n"
                if module['docstring']:
                    api_content += f"{module['docstring']}\n\n"
                else:
                    api_content += f"*No documentation available*\n\n"
            
            section_key = f"api_{relative_path.replace('/', '_').replace('.', '_')}"
            api_sections[section_key] = DocumentationSection(
                title=f"API - {relative_path}",
                content=api_content,
                section_type="api",
                priority=8,
                file_references=[file_path],
                last_updated=time.time()
            )
        
        return api_sections
    
    async def generate_changelog(self, structure: Dict, repo_path: str) -> Dict[str, DocumentationSection]:
        """Generate changelog from git history"""
        try:
            # This would integrate with git history in a real implementation
            changelog_content = """# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
- Generated documentation system
- AI-powered documentation updates

## Guidelines
- Keep a changelog format
- Add new entries at the top
- Use semantic versioning
"""
            
            return {
                'changelog': DocumentationSection(
                    title="Changelog",
                    content=changelog_content,
                    section_type="changelog",
                    priority=6,
                    file_references=[repo_path],
                    last_updated=time.time()
                )
            }
            
        except Exception as e:
            print(f"   ❌ Failed to generate changelog: {e}")
            return {}
    
    def format_modules_for_prompt(self, modules: List[Dict]) -> str:
        """Format modules for AI prompt"""
        formatted = []
        for module in modules:
            formatted.append(f"- {module['type']}: {module['name']}")
            if module['docstring']:
                # Truncate long docstrings for prompt efficiency
                docstring = module['docstring'][:200]
                if len(module['docstring']) > 200:
                    docstring += "..."
                formatted.append(f"  {docstring}")
        return "\n".join(formatted)
    
    async def save_documentation(self, documentation: Dict[str, DocumentationSection], output_dir: str):
        """Save generated documentation to files"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        for section_key, section in documentation.items():
            if section.section_type == 'readme':
                file_path = output_path / "README.md"
            elif section.section_type == 'api':
                file_path = output_path / f"{section_key}.md"
            elif section.section_type == 'changelog':
                file_path = output_path / "CHANGELOG.md"
            else:
                file_path = output_path / f"{section_key}.md"
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(section.content)
            
            print(f"   💾 Saved {file_path}")
    
    def print_metrics(self):
        """Print performance metrics"""
        total_time = time.time() - self.metrics['start_time']
        print("\n📊 Documentation Agent Metrics:")
        print(f"   Total Time: {total_time:.1f}s")
        print(f"   Files Analyzed: {self.metrics['files_analyzed']}")
        print(f"   Documents Generated: {self.metrics['docs_generated']}")
        print(f"   Cache Hits: {self.metrics['cache_hits']}")
        if self.metrics['docs_generated'] > 0:
            print(f"   Avg Time/Document: {total_time/self.metrics['docs_generated']:.1f}s")

async def main():
    """Demo documentation generation"""
    repo_path = os.getenv('REPO_PATH', '.')
    output_dir = os.getenv('OUTPUT_DIR', './generated-docs')
    
    agent = DocumentationAgent()
    
    print("🤖 AI Documentation Agent Starting...")
    
    # Generate different types of documentation
    doc_types = ['readme', 'api_docs', 'changelog']
    documentation = await agent.generate_documentation(repo_path, doc_types)
    
    # Save generated documentation
    await agent.save_documentation(documentation, output_dir)
    
    print(f"\n✅ Generated {len(documentation)} documentation sections")
    agent.print_metrics()

if __name__ == "__main__":
    asyncio.run(main())