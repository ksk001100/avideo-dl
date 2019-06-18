import re
from urllib.parse import urlparse
from typing import Dict, Any

def headers() -> Dict[str, Any]:
    return {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36",
    }

def camel_case(s: str) -> str:
    return ''.join(map(lambda x: x.capitalize(), re.split('[-,_]', s)))

def snake_case(s: str) -> str:
    return '_'.join(map(lambda x: x.lower(), re.split('[-,_]', s)))

def service_name(url: str) -> str:
    pattern = ['www', 'com', 'co', 'jp', 'se', 'video']
    return next(filter(lambda x: x not in pattern, urlparse(url).netloc.split('.')))
