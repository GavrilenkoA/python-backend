import json


async def fibonacci_app(scope, receive, send):
    # Ensure the request type is HTTP
    assert scope['type'] == 'http'

    # Handle only GET method
    if scope['method'] == 'GET':
        # Extract the path parameters from the scope
        path = scope['path']
        path_params = path.strip('/').split('/')

        if len(path_params) != 2 or path_params[0] != 'fibonacci':
            await send({
                'type': 'http.response.start',
                'status': 404,
                'headers': [(b'content-type', b'application/json')]
            })
            await send({
                'type': 'http.response.body',
                'body': json.dumps({'detail': '404 Not Found'}).encode('utf-8')
            })
            return

        try:
            n = int(path_params[1])
        except ValueError:
            # Return 422 if 'n' is not an integer
            await send({
                'type': 'http.response.start',
                'status': 422,
                'headers': [(b'content-type', b'application/json')]
            })
            await send({
                'type': 'http.response.body',
                'body': json.dumps({'detail': '422 Unprocessable Entity: "n" must be an integer'}).encode('utf-8')
            })
            return

        # Return 400 Bad Request if 'n' is a negative number
        if n < 0:
            await send({
                'type': 'http.response.start',
                'status': 400,
                'headers': [(b'content-type', b'application/json')]
            })
            await send({
                'type': 'http.response.body',
                'body': json.dumps({'detail': '400 Bad Request: "n" must be a non-negative integer'}).encode('utf-8')
            })
            return

        # Calculate the n-th Fibonacci number
        def fibonacci(n):
            if n == 0:
                return 0
            elif n == 1:
                return 1
            else:
                a, b = 0, 1
                for _ in range(2, n + 1):
                    a, b = b, a + b
                return b

        result = fibonacci(n)

        # Return result as JSON
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [(b'content-type', b'application/json')]
        })
        await send({
            'type': 'http.response.body',
            'body': json.dumps({'result': result}).encode('utf-8')
        })
    else:
        # Method not allowed for other HTTP methods
        await send({
            'type': 'http.response.start',
            'status': 405,
            'headers': [(b'content-type', b'application/json')]
        })
        await send({
            'type': 'http.response.body',
            'body': json.dumps({'detail': '405 Method Not Allowed'}).encode('utf-8')
        })