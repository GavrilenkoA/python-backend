from factorial import factorial_app
from fibonacci import fibonacci_app
from mean import mean_app


async def app(scope, receive, send):
    if scope['path'].startswith('/fibonacci'):
        await fibonacci_app(scope, receive, send)
    elif scope['path'].startswith('/mean'):
        await mean_app(scope, receive, send)
    elif scope['path'].startswith('/factorial'):
        await factorial_app(scope, receive, send)