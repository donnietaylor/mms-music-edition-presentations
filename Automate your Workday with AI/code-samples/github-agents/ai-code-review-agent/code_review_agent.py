#!/usr/bin/env python3
"""
Customized AI Code Review Agent
Demonstrates speed optimizations and enhanced task execution
"""

import os
import json
import yaml
import asyncio
import time
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor
import openai
from github import Github
import hashlib
import redis

class CodeReviewAgent:
    def __init__(self):
        self.github = Github(os.getenv('GITHUB_TOKEN'))
        self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.mode = os.getenv('REVIEW_MODE', 'standard')
        self.focus = os.getenv('REVIEW_FOCUS', 'comprehensive')
        self.timeout = int(os.getenv('TIMEOUT', '180').rstrip('s'))
        self.parallel = os.getenv('PARALLEL_ANALYSIS', 'false').lower() == 'true'
        
        # Initialize Redis for caching if available
        self.redis_client = None
        if os.getenv('REDIS_URL'):
            try:
                self.redis_client = redis.from_url(os.getenv('REDIS_URL'))
            except Exception as e:
                print(f"Redis connection failed: {e}")
        
        # Load custom configurations
        self.load_configurations()
        
        # Performance tracking
        self.metrics = {
            'start_time': time.time(),
            'files_analyzed': 0,
            'cache_hits': 0,
            'api_calls': 0,
            'errors': 0
        }
    
    def load_configurations(self):
        """Load custom prompts, rules, and performance settings"""
        try:
            with open('prompts.yaml', 'r') as f:
                self.prompts = yaml.safe_load(f)
            
            with open('rules.json', 'r') as f:
                self.rules = json.load(f)
                
            with open('performance-config.yaml', 'r') as f:
                self.perf_config = yaml.safe_load(f)
                
            print("✅ Configurations loaded successfully")
        except FileNotFoundError as e:
            print(f"⚠️ Configuration file not found: {e}")
            # Use minimal default configurations
            self._load_defaults()
    
    def _load_defaults(self):
        """Load minimal default configurations"""
        self.prompts = {
            "prompts": {
                "general_review": {
                    "system": "You are a code reviewer. Provide concise, actionable feedback."
                }
            }
        }
        self.rules = {"rules": {"auto_approve_conditions": []}}
        self.perf_config = {
            "performance_optimizations": {
                "parallel_analysis": False,
                "ai_model_optimization": {
                    "primary_model": "gpt-3.5-turbo",
                    "max_tokens": 1500,
                    "temperature": 0.1
                }
            }
        }
    
    def get_cache_key(self, content: str) -> str:
        """Generate cache key for content"""
        return f"review:{hashlib.md5(content.encode()).hexdigest()}"
    
    def get_cached_review(self, cache_key: str) -> Optional[str]:
        """Get cached review if available"""
        if not self.redis_client:
            return None
            
        try:
            cached = self.redis_client.get(cache_key)
            if cached:
                self.metrics['cache_hits'] += 1
                return cached.decode()
        except Exception as e:
            print(f"Cache read error: {e}")
        return None
    
    def cache_review(self, cache_key: str, review: str):
        """Cache review result"""
        if not self.redis_client:
            return
            
        try:
            # Cache for 24 hours
            self.redis_client.setex(cache_key, 86400, review)
        except Exception as e:
            print(f"Cache write error: {e}")
    
    def get_pr_files(self, pr_number: int) -> List[Dict]:
        """Get changed files with optimized fetching"""
        repo = self.github.get_repo(os.getenv('GITHUB_REPOSITORY'))
        pr = repo.get_pull(pr_number)
        
        files = []
        for file in pr.get_files():
            # Skip large files and binary files for speed
            if file.changes > 500 or self.is_binary_file(file.filename):
                print(f"⏭️ Skipping {file.filename} (too large or binary)")
                continue
                
            files.append({
                'filename': file.filename,
                'status': file.status,
                'patch': file.patch or "",
                'changes': file.changes
            })
        
        return files
    
    def is_binary_file(self, filename: str) -> bool:
        """Quick check for binary files to skip"""
        binary_extensions = {
            '.png', '.jpg', '.jpeg', '.gif', '.pdf', '.zip', 
            '.exe', '.dll', '.so', '.dylib', '.wasm'
        }
        return any(filename.lower().endswith(ext) for ext in binary_extensions)
    
    async def analyze_file_async(self, file_data: Dict) -> Dict:
        """Analyze a single file asynchronously with caching"""
        start_time = time.time()
        filename = file_data['filename']
        
        # Check cache first
        cache_key = self.get_cache_key(f"{filename}:{file_data.get('patch', '')}")
        cached_review = self.get_cached_review(cache_key)
        
        if cached_review:
            print(f"💾 Cache hit for {filename}")
            return {
                'filename': filename,
                'review': cached_review,
                'analysis_time': time.time() - start_time,
                'success': True,
                'cached': True
            }
        
        # Select appropriate prompt
        prompt = self.select_prompt(filename)
        
        try:
            model_config = self.perf_config.get('performance_optimizations', {}).get('ai_model_optimization', {})
            
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model=model_config.get('primary_model', 'gpt-3.5-turbo'),
                messages=[
                    {"role": "system", "content": prompt},
                    {
                        "role": "user", 
                        "content": f"Review this code change:\n\nFile: {filename}\nStatus: {file_data['status']}\n\nChanges:\n{file_data['patch']}"
                    }
                ],
                max_tokens=model_config.get('max_tokens', 1500),
                temperature=model_config.get('temperature', 0.1),
                timeout=self.timeout
            )
            
            self.metrics['api_calls'] += 1
            review_content = response.choices[0].message.content
            
            # Cache the result
            self.cache_review(cache_key, review_content)
            
            analysis_time = time.time() - start_time
            print(f"✅ Analyzed {filename} in {analysis_time:.1f}s")
            
            return {
                'filename': filename,
                'review': review_content,
                'analysis_time': analysis_time,
                'success': True,
                'cached': False
            }
            
        except Exception as e:
            self.metrics['errors'] += 1
            error_time = time.time() - start_time
            print(f"❌ Error analyzing {filename}: {str(e)}")
            
            return {
                'filename': filename,
                'error': str(e),
                'analysis_time': error_time,
                'success': False,
                'cached': False
            }
    
    def select_prompt(self, filename: str) -> str:
        """Select appropriate prompt based on file type and review focus"""
        prompts = self.prompts.get('prompts', {})
        
        # File type-based prompt selection
        if any(pattern in filename.lower() for pattern in ['auth', 'security', 'crypto']):
            return prompts.get('security_focused', {}).get('system', '')
        elif any(pattern in filename.lower() for pattern in ['service', 'controller', 'api']):
            return prompts.get('performance_focused', {}).get('system', '')
        elif any(ext in filename.lower() for ext in ['.js', '.jsx', '.ts', '.tsx', '.vue']):
            return prompts.get('frontend_focused', {}).get('system', '')
        elif filename.lower().endswith(('.py', '.java', '.go', '.rb')):
            return prompts.get('backend_focused', {}).get('system', '')
        elif filename.lower().endswith(('.md', '.txt', '.rst')):
            return prompts.get('documentation_focused', {}).get('system', '')
        
        return prompts.get('general_review', {}).get('system', 'You are a code reviewer.')
    
    def apply_quick_filters(self, files: List[Dict]) -> List[Dict]:
        """Apply quick filters to skip unnecessary analysis"""
        filtered_files = []
        quick_checks = self.perf_config.get('performance_optimizations', {}).get('quick_checks', [])
        
        for file in files:
            skip_file = False
            
            # Apply configured quick checks
            for check in quick_checks:
                if check.get('action') == 'skip':
                    patterns = check.get('pattern', '').split(' OR ')
                    if any(pattern.strip().replace('*', '') in file['filename'] for pattern in patterns):
                        print(f"⏭️ Skipping {file['filename']} ({check['name']})")
                        skip_file = True
                        break
            
            # Skip large files in express mode
            if self.mode == 'express' and file['changes'] > 100:
                print(f"⏭️ Skipping {file['filename']} (too many changes for express mode)")
                skip_file = True
                
            if not skip_file:
                filtered_files.append(file)
        
        return filtered_files
    
    async def analyze_files_parallel(self, files: List[Dict]) -> List[Dict]:
        """Analyze files in parallel for speed"""
        max_concurrent = self.perf_config.get('performance_optimizations', {}).get('max_concurrent_reviews', 3)
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def analyze_with_semaphore(file_data):
            async with semaphore:
                return await self.analyze_file_async(file_data)
        
        print(f"🚀 Starting parallel analysis of {len(files)} files (max concurrent: {max_concurrent})")
        tasks = [analyze_with_semaphore(file) for file in files]
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    async def analyze_files_sequential(self, files: List[Dict]) -> List[Dict]:
        """Analyze files sequentially"""
        print(f"🔄 Starting sequential analysis of {len(files)} files")
        results = []
        for file in files:
            result = await self.analyze_file_async(file)
            results.append(result)
        return results
    
    async def review_pr(self, pr_number: int):
        """Main review function with speed optimizations"""
        print(f"🤖 Starting AI Code Review for PR #{pr_number}")
        print(f"📊 Mode: {self.mode}, Focus: {self.focus}, Parallel: {self.parallel}")
        
        # Get PR files
        files = self.get_pr_files(pr_number)
        print(f"📁 Found {len(files)} files to potentially analyze")
        
        # Apply quick filters
        files = self.apply_quick_filters(files)
        print(f"✅ After filtering: {len(files)} files to analyze")
        
        if not files:
            print("ℹ️ No files to analyze after filtering")
            return
        
        self.metrics['files_analyzed'] = len(files)
        
        # Analyze files (parallel or sequential based on configuration)
        if self.parallel and len(files) > 1:
            results = await self.analyze_files_parallel(files)
        else:
            results = await self.analyze_files_sequential(files)
        
        # Generate and post review
        total_time = time.time() - self.metrics['start_time']
        await self.generate_review_summary(pr_number, results, total_time)
        
        # Print performance metrics
        self.print_metrics(total_time)
    
    def print_metrics(self, total_time: float):
        """Print performance metrics"""
        print("\n📊 Performance Metrics:")
        print(f"   Total Time: {total_time:.1f}s")
        print(f"   Files Analyzed: {self.metrics['files_analyzed']}")
        print(f"   API Calls: {self.metrics['api_calls']}")
        print(f"   Cache Hits: {self.metrics['cache_hits']}")
        print(f"   Errors: {self.metrics['errors']}")
        print(f"   Avg Time/File: {total_time/max(self.metrics['files_analyzed'], 1):.1f}s")
        if self.metrics['files_analyzed'] > 0:
            print(f"   Cache Hit Rate: {self.metrics['cache_hits']/self.metrics['files_analyzed']*100:.1f}%")
    
    async def generate_review_summary(self, pr_number: int, results: List[Dict], total_time: float):
        """Generate and post review summary with metrics"""
        repo = self.github.get_repo(os.getenv('GITHUB_REPOSITORY'))
        pr = repo.get_pull(pr_number)
        
        successful_reviews = [r for r in results if isinstance(r, dict) and r.get('success')]
        failed_reviews = [r for r in results if isinstance(r, dict) and not r.get('success')]
        cached_reviews = [r for r in successful_reviews if r.get('cached')]
        
        # Generate summary
        summary = f"""## 🤖 AI Code Review Summary

**Review Mode**: {self.mode} | **Focus**: {self.focus} | **Parallel**: {'✅' if self.parallel else '❌'}
**Files Analyzed**: {len(successful_reviews)}/{len(results)} | **Total Time**: {total_time:.1f}s
**Average Time/File**: {total_time/len(results):.1f}s | **Cache Hits**: {len(cached_reviews)}

### 📋 Key Findings:
"""
        
        # Add individual file reviews
        for result in successful_reviews:
            if result.get('review'):
                cache_indicator = "💾" if result.get('cached') else "🔍"
                summary += f"\n#### {cache_indicator} {result['filename']}\n{result['review']}\n"
        
        # Add errors if any
        if failed_reviews:
            summary += f"\n### ⚠️ Analysis Errors:\n"
            for result in failed_reviews:
                summary += f"- **{result['filename']}**: {result.get('error', 'Unknown error')}\n"
        
        # Add performance metrics
        model_used = self.perf_config.get('performance_optimizations', {}).get('ai_model_optimization', {}).get('primary_model', 'gpt-3.5-turbo')
        
        summary += f"""
### 📊 Performance Metrics:
- **Model**: {model_used}
- **Parallel Processing**: {'Enabled' if self.parallel else 'Disabled'}
- **API Calls**: {self.metrics['api_calls']}
- **Cache Hit Rate**: {len(cached_reviews)}/{len(results)} ({len(cached_reviews)/len(results)*100:.1f}%)
- **Success Rate**: {len(successful_reviews)}/{len(results)} ({len(successful_reviews)/len(results)*100:.1f}%)

*Generated by AI Code Review Agent v2.0*
"""
        
        # Post review
        try:
            pr.create_issue_comment(summary)
            print("✅ Review summary posted successfully")
        except Exception as e:
            print(f"❌ Failed to post review: {e}")

async def main():
    """Main execution function"""
    try:
        pr_number = int(os.getenv('PR_NUMBER', '1'))
        agent = CodeReviewAgent()
        await agent.review_pr(pr_number)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        exit(1)

if __name__ == "__main__":
    asyncio.run(main())