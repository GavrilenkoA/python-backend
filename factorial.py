import json
import math


async def app(scope, receive, send) -> None:
    # Ensure the request type is HTTP
    assert scope['type'] == 'http'

    # Handle only GET method
    if scope['method'] == 'GET':
        # Parse the query string
        query_string = scope['query_string'].decode()
        params = dict(q.split('=') for q in query_string.split('&') if '=' in q)

        # Check if 'n' is present and is a valid integer
        if 'n' not in params:
            # Return 422 Unprocessable Entity if 'n' is absent
            await send({
                'type': 'http.response.start',
                'status': 422,
                'headers': [(b'content-type', b'application/json')]
            })
            await send({
                'type': 'http.response.body',
                'body': json.dumps({'detail': "n query parameter is required"}).encode('utf-8')
            })
            return

        try:
            n = int(params['n'])
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

        # Calculate factorial
        result = math.factorial(n)

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


    # else:
    #     # Method not allowed for other HTTP methods
    #     await send({
    #         'type': 'http.response.start',
    #         'status': 405,
    #         'headers': [(b'content-type', b'application/json')]
    #     })
    #     await send({
    #         'type': 'http.response.body',
    #         'body': json.dumps({'detail': 'Method not allowed'}).encode('utf-8')
    #     })
