from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, max_requests: int = 100, window: int = 60):
        self.max_requests = max_requests
        self.window = window
        self.requests = defaultdict(list)

    async def __call__(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host

        # Remove old requests
        current_time = time.time()
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip] 
            if current_time - req_time < self.window
        ]

        # Check if request limit is exceeded
        if len(self.requests[client_ip]) >= self.max_requests:
            raise HTTPException(
                status_code=429, 
                detail="Too many requests. Please try again later."
            )

        # Add current request time
        self.requests[client_ip].append(current_time)

        # Continue with request
        response = await call_next(request)
        return response
