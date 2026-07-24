import time
from collections import defaultdict

class InMemoryRateLimiter:
    """
    In-memory sliding window rate limiter.
    (Can easily swap with Redis ZSETs when scaling across multiple nodes).
    """
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        window_start = now - self.window_seconds

        # Clean up timestamps older than the sliding window
        self.requests[client_id] = [
            ts for ts in self.requests[client_id] if ts > window_start
        ]

        if len(self.requests[client_id]) < self.max_requests:
            self.requests[client_id].append(now)
            return True
        
        return False

# Limit each client to 50 requests per minute
rate_limiter = InMemoryRateLimiter(max_requests=50, window_seconds=60)