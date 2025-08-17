# app/utils/performance_monitor.py
import tracemalloc
import psutil
from functools import wraps


def memory_profile(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        tracemalloc.start()
        process = psutil.Process()

        # 실행 전 상태
        mem_before = process.memory_info().rss / 1024 / 1024  # MB

        # 함수 실행
        result = await func(*args, **kwargs)

        # 실행 후 상태
        current, peak = tracemalloc.get_traced_memory()
        mem_after = process.memory_info().rss / 1024 / 1024

        print(f"Memory used: {current / 1024 / 1024:.2f}MB")
        print(f"Peak memory: {peak / 1024 / 1024:.2f}MB")
        print(f"Process memory diff: {mem_after - mem_before:.2f}MB")

        tracemalloc.stop()
        return result

    return wrapper
