from slowapi import limiter
from slowapi.util import get_remote_address

limiter = limiter.Limiter(key_func=get_remote_address)
