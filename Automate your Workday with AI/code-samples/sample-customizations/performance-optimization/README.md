# Performance Optimization Examples

Speed and efficiency improvements for AI agents and automation workflows, implementing best practices from the [GitHub Copilot optimization guide](https://docs.github.com/en/enterprise-cloud@latest/copilot/tutorials/coding-agent/get-the-best-results).

## ⚡ Caching Strategies

### Intelligent Result Caching
```python
# intelligent-cache.py
import hashlib
import json
import time
from typing import Any, Dict, Optional
from functools import wraps
import asyncio

class IntelligentCache:
    def __init__(self, default_ttl: int = 3600):
        self.cache = {}
        self.default_ttl = default_ttl
    
    def _generate_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Generate a unique cache key based on function name and parameters"""
        key_data = {
            'function': func_name,
            'args': args,
            'kwargs': kwargs
        }
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _is_expired(self, cached_item: dict) -> bool:
        """Check if cached item has expired"""
        return time.time() > cached_item['expires_at']
    
    def get(self, key: str) -> Optional[Any]:
        """Get item from cache if it exists and hasn't expired"""
        if key in self.cache:
            cached_item = self.cache[key]
            if not self._is_expired(cached_item):
                cached_item['hits'] += 1
                return cached_item['value']
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Store item in cache with TTL"""
        ttl = ttl or self.default_ttl
        self.cache[key] = {
            'value': value,
            'expires_at': time.time() + ttl,
            'created_at': time.time(),
            'hits': 0
        }
    
    def cache_decorator(self, ttl: Optional[int] = None):
        """Decorator to automatically cache function results"""
        def decorator(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                cache_key = self._generate_key(func.__name__, args, kwargs)
                
                # Try to get from cache first
                cached_result = self.get(cache_key)
                if cached_result is not None:
                    print(f"🚀 Cache hit for {func.__name__}")
                    return cached_result
                
                # Execute function and cache result
                print(f"⏳ Cache miss, executing {func.__name__}")
                result = await func(*args, **kwargs)
                self.set(cache_key, result, ttl)
                return result
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                cache_key = self._generate_key(func.__name__, args, kwargs)
                
                cached_result = self.get(cache_key)
                if cached_result is not None:
                    print(f"🚀 Cache hit for {func.__name__}")
                    return cached_result
                
                print(f"⏳ Cache miss, executing {func.__name__}")
                result = func(*args, **kwargs)
                self.set(cache_key, result, ttl)
                return result
            
            return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        return decorator

# Usage example
cache = IntelligentCache(default_ttl=1800)  # 30 minutes

@cache.cache_decorator(ttl=3600)  # Cache for 1 hour
async def expensive_api_call(endpoint: str, params: dict) -> dict:
    """Simulate expensive API call that should be cached"""
    await asyncio.sleep(2)  # Simulate network delay
    return {
        'data': f"Result from {endpoint}",
        'params': params,
        'timestamp': time.time()
    }

@cache.cache_decorator(ttl=300)  # Cache for 5 minutes
def generate_documentation(file_path: str) -> str:
    """Generate documentation - expensive operation that benefits from caching"""
    time.sleep(1)  # Simulate processing time
    return f"Generated documentation for {file_path}"
```

## 🔄 Parallel Processing Patterns

### Concurrent Task Execution
```python
# parallel-execution.py
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Callable, Any
import multiprocessing as mp

class ParallelProcessor:
    def __init__(self, max_workers: int = None):
        self.max_workers = max_workers or mp.cpu_count()
    
    async def async_parallel_map(self, func: Callable, items: List[Any], chunk_size: int = 10) -> List[Any]:
        """Execute function on items in parallel using asyncio"""
        semaphore = asyncio.Semaphore(self.max_workers)
        
        async def bounded_task(item):
            async with semaphore:
                return await func(item)
        
        # Process in chunks to avoid overwhelming the system
        results = []
        for i in range(0, len(items), chunk_size):
            chunk = items[i:i + chunk_size]
            chunk_results = await asyncio.gather(
                *[bounded_task(item) for item in chunk],
                return_exceptions=True
            )
            results.extend(chunk_results)
        
        return results
    
    def thread_parallel_map(self, func: Callable, items: List[Any]) -> List[Any]:
        """Execute function on items in parallel using threads"""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_item = {executor.submit(func, item): item for item in items}
            
            results = []
            for future in as_completed(future_to_item):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"Error processing item: {e}")
                    results.append(None)
            
            return results
    
    def process_parallel_map(self, func: Callable, items: List[Any]) -> List[Any]:
        """Execute function on items in parallel using processes"""
        with mp.Pool(processes=self.max_workers) as pool:
            results = pool.map(func, items)
            return results

# Batch processing with smart chunking
class BatchProcessor:
    def __init__(self, batch_size: int = 50, max_concurrent_batches: int = 5):
        self.batch_size = batch_size
        self.max_concurrent_batches = max_concurrent_batches
    
    def create_batches(self, items: List[Any]) -> List[List[Any]]:
        """Split items into optimally sized batches"""
        return [items[i:i + self.batch_size] for i in range(0, len(items), self.batch_size)]
    
    async def process_batches(self, items: List[Any], processor_func: Callable) -> List[Any]:
        """Process items in batches with controlled concurrency"""
        batches = self.create_batches(items)
        semaphore = asyncio.Semaphore(self.max_concurrent_batches)
        
        async def process_batch(batch):
            async with semaphore:
                return await processor_func(batch)
        
        # Process all batches concurrently
        batch_results = await asyncio.gather(
            *[process_batch(batch) for batch in batches],
            return_exceptions=True
        )
        
        # Flatten results
        all_results = []
        for batch_result in batch_results:
            if isinstance(batch_result, Exception):
                print(f"Batch processing error: {batch_result}")
                continue
            if isinstance(batch_result, list):
                all_results.extend(batch_result)
            else:
                all_results.append(batch_result)
        
        return all_results

# Example usage
async def example_parallel_processing():
    """Demonstrate parallel processing techniques"""
    
    # Sample data
    items = [f"item_{i}" for i in range(100)]
    
    # Define processing function
    async def process_item(item: str) -> str:
        await asyncio.sleep(0.1)  # Simulate work
        return f"processed_{item}"
    
    # Time comparison
    start_time = time.time()
    
    # Sequential processing (slow)
    sequential_results = []
    for item in items[:10]:  # Test with fewer items
        result = await process_item(item)
        sequential_results.append(result)
    
    sequential_time = time.time() - start_time
    print(f"Sequential processing: {sequential_time:.2f}s for 10 items")
    
    # Parallel processing (fast)
    start_time = time.time()
    processor = ParallelProcessor(max_workers=10)
    parallel_results = await processor.async_parallel_map(process_item, items[:10])
    parallel_time = time.time() - start_time
    
    print(f"Parallel processing: {parallel_time:.2f}s for 10 items")
    print(f"Speedup: {sequential_time / parallel_time:.1f}x")

if __name__ == "__main__":
    asyncio.run(example_parallel_processing())
```

## 🎯 Selective Processing

### Smart File Processing
```python
# selective-processing.py
import os
import hashlib
import json
from pathlib import Path
from typing import Set, Dict, List, Optional
from datetime import datetime

class SelectiveProcessor:
    def __init__(self, cache_file: str = ".processing_cache.json"):
        self.cache_file = cache_file
        self.cache = self._load_cache()
    
    def _load_cache(self) -> Dict:
        """Load processing cache from disk"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_cache(self) -> None:
        """Save processing cache to disk"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save cache: {e}")
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Calculate hash of file contents"""
        hasher = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except IOError:
            return ""
    
    def _needs_processing(self, file_path: Path) -> bool:
        """Check if file needs processing based on hash comparison"""
        file_str = str(file_path)
        current_hash = self._get_file_hash(file_path)
        
        if file_str not in self.cache:
            return True
        
        cached_hash = self.cache[file_str].get('hash')
        return cached_hash != current_hash
    
    def get_files_to_process(self, directory: Path, extensions: Set[str] = None) -> List[Path]:
        """Get list of files that need processing"""
        extensions = extensions or {'.py', '.js', '.ts', '.md', '.yaml', '.yml'}
        
        files_to_process = []
        
        for file_path in directory.rglob('*'):
            if (file_path.is_file() and 
                file_path.suffix.lower() in extensions and
                not self._is_ignored(file_path)):
                
                if self._needs_processing(file_path):
                    files_to_process.append(file_path)
        
        return files_to_process
    
    def _is_ignored(self, file_path: Path) -> bool:
        """Check if file should be ignored based on common patterns"""
        ignore_patterns = {
            'node_modules', '.git', '__pycache__', '.pytest_cache',
            'dist', 'build', '.venv', 'venv', '.env'
        }
        
        for part in file_path.parts:
            if part in ignore_patterns:
                return True
        
        return False
    
    def mark_processed(self, file_path: Path, metadata: Dict = None) -> None:
        """Mark file as processed and update cache"""
        file_str = str(file_path)
        self.cache[file_str] = {
            'hash': self._get_file_hash(file_path),
            'processed_at': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
    
    def process_directory(self, directory: Path, processor_func, extensions: Set[str] = None) -> Dict:
        """Process only changed files in directory"""
        files_to_process = self.get_files_to_process(directory, extensions)
        
        if not files_to_process:
            print("✅ No files need processing")
            return {'processed': 0, 'skipped': 0, 'results': []}
        
        print(f"📁 Processing {len(files_to_process)} changed files...")
        
        results = []
        processed_count = 0
        
        for file_path in files_to_process:
            try:
                print(f"⚡ Processing: {file_path}")
                result = processor_func(file_path)
                
                # Mark as processed
                self.mark_processed(file_path, {'result': str(result)[:100]})
                results.append({'file': str(file_path), 'result': result})
                processed_count += 1
                
            except Exception as e:
                print(f"❌ Error processing {file_path}: {e}")
                results.append({'file': str(file_path), 'error': str(e)})
        
        # Save cache
        self._save_cache()
        
        total_files = len(list(directory.rglob('*')))
        skipped_count = total_files - processed_count
        
        return {
            'processed': processed_count,
            'skipped': skipped_count,
            'results': results
        }

# Example usage
def example_selective_processing():
    """Demonstrate selective processing"""
    
    def dummy_processor(file_path: Path) -> str:
        """Example processor function"""
        # Simulate processing work
        import time
        time.sleep(0.1)
        return f"Processed {file_path.name}"
    
    processor = SelectiveProcessor()
    current_dir = Path(".")
    
    # Process only changed Python and Markdown files
    results = processor.process_directory(
        current_dir, 
        dummy_processor, 
        extensions={'.py', '.md'}
    )
    
    print(f"📊 Results: {results['processed']} processed, {results['skipped']} skipped")

if __name__ == "__main__":
    example_selective_processing()
```

## 📊 Performance Monitoring

### Metrics Collection
```python
# performance-metrics.py
import time
import psutil
import json
from typing import Dict, List, Any
from datetime import datetime
from functools import wraps

class PerformanceMonitor:
    def __init__(self):
        self.metrics = []
        self.start_time = time.time()
    
    def timing_decorator(self, operation_name: str):
        """Decorator to measure execution time"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                start_memory = psutil.Process().memory_info().rss
                
                try:
                    result = func(*args, **kwargs)
                    success = True
                    error = None
                except Exception as e:
                    result = None
                    success = False
                    error = str(e)
                    raise
                finally:
                    end_time = time.time()
                    end_memory = psutil.Process().memory_info().rss
                    
                    self.record_metric({
                        'operation': operation_name,
                        'function': func.__name__,
                        'duration': end_time - start_time,
                        'memory_delta': end_memory - start_memory,
                        'success': success,
                        'error': error,
                        'timestamp': datetime.now().isoformat()
                    })
                
                return result
            return wrapper
        return decorator
    
    def record_metric(self, metric: Dict[str, Any]) -> None:
        """Record a performance metric"""
        self.metrics.append(metric)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        if not self.metrics:
            return {'message': 'No metrics recorded'}
        
        total_operations = len(self.metrics)
        successful_operations = sum(1 for m in self.metrics if m.get('success', True))
        total_duration = sum(m.get('duration', 0) for m in self.metrics)
        avg_duration = total_duration / total_operations
        
        # Group by operation
        by_operation = {}
        for metric in self.metrics:
            op = metric.get('operation', 'unknown')
            if op not in by_operation:
                by_operation[op] = []
            by_operation[op].append(metric)
        
        operation_stats = {}
        for op, metrics in by_operation.items():
            durations = [m['duration'] for m in metrics]
            operation_stats[op] = {
                'count': len(metrics),
                'avg_duration': sum(durations) / len(durations),
                'min_duration': min(durations),
                'max_duration': max(durations),
                'success_rate': sum(1 for m in metrics if m.get('success', True)) / len(metrics)
            }
        
        return {
            'total_operations': total_operations,
            'successful_operations': successful_operations,
            'success_rate': successful_operations / total_operations,
            'total_duration': total_duration,
            'average_duration': avg_duration,
            'operation_stats': operation_stats,
            'uptime': time.time() - self.start_time
        }
    
    def export_metrics(self, filename: str) -> None:
        """Export metrics to JSON file"""
        with open(filename, 'w') as f:
            json.dump({
                'summary': self.get_summary(),
                'raw_metrics': self.metrics
            }, f, indent=2)

# Example usage
monitor = PerformanceMonitor()

@monitor.timing_decorator("file_processing")
def process_file(filename: str) -> str:
    time.sleep(0.1)  # Simulate work
    return f"Processed {filename}"

@monitor.timing_decorator("api_call")
def make_api_call(endpoint: str) -> Dict:
    time.sleep(0.2)  # Simulate API call
    return {"data": f"Response from {endpoint}"}

# Run some operations
for i in range(10):
    process_file(f"file_{i}.txt")
    make_api_call(f"api/endpoint/{i}")

# Get performance summary
summary = monitor.get_summary()
print(json.dumps(summary, indent=2))
```

## 🔧 Optimization Best Practices

1. **Profile Before Optimizing**: Measure current performance to identify bottlenecks
2. **Cache Intelligently**: Cache expensive operations with appropriate TTL
3. **Process in Parallel**: Use async/await and threading for I/O bound tasks
4. **Batch Operations**: Group similar operations to reduce overhead
5. **Selective Processing**: Only process what has changed
6. **Monitor Continuously**: Track performance metrics over time

## 📈 Performance Gains Expected

- **Caching**: 50-90% reduction in repeated operations
- **Parallel Processing**: 3-10x speedup for I/O bound tasks
- **Selective Processing**: 70-95% reduction in unnecessary work
- **Batch Operations**: 30-60% improvement in throughput