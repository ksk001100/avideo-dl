import re
from urllib.parse import urlparse

def camel_case(s: str) -> str:
    return ''.join(map(lambda x : x.capitalize(), re.split('[-,_]', s)))

def snake_case(s: str) -> str:
    return '_'.join(map(lambda x : x.lower(), re.split('[-,_]', s)))

def service_name(url: str) -> str:
    pattern = ['www', 'com', 'co', 'jp', 'se']
    return list(filter(lambda x : x not in pattern, urlparse(url).netloc.split('.')))[0]