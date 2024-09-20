import json


async def mean_app(scope, receive, send):
    # Ensure the request type is HTTP
    assert scope['type'] == 'http'

    # Handle only GET method
    if scope['method'] == 'GET':
        body = b''
        while True:
            event = await receive()
            body += event.get('body', b'')
            if event.get('more_body', False) is False:
                break

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            # Return 422 if body is not valid JSON
            await send({
                'type': 'http.response.start',
                'status': 422,
                'headers': [(b'content-type', b'application/json')]
            })
            await send({
                'type': 'http.response.body',
                'body': json.dumps({'detail': '422 Unprocessable Entity: Request body must be valid JSON'}).encode(
                    'utf-8')
            })
            return

        if not isinstance(data, list):
            # Return 422 if body is not a list
            await send({
                'type': 'http.response.start',
                'status': 422,
                'headers': [(b'content-type', b'application/json')]
            })
            await send({
                'type': 'http.response.body',
                'body': json.dumps({'detail': '422 Unprocessable Entity: Body must be a list'}).encode('utf-8')
            })
            return

        if len(data) == 0:
            # Return 400 if array is empty
            await send({
                'type': 'http.response.start',
                'status': 400,
                'headers': [(b'content-type', b'application/json')]
            })
            await send({
                'type': 'http.response.body',
                'body': json.dumps({'detail': '400 Bad Request: Array cannot be empty'}).encode('utf-8')
            })
            return

        if not all(isinstance(x, (int, float)) for x in data):
            # Return 422 if array contains non-floats
            await send({
                'type': 'http.response.start',
                'status': 422,
                'headers': [(b'content-type', b'application/json')]
            })
            await send({
                'type': 'http.response.body',
                'body': json.dumps({'detail': '422 Unprocessable Entity: Array must contain only numbers'}).encode(
                    'utf-8')
            })
            return

        # Calculate the mean
        mean_value = sum(data) / len(data)

        # Return result as JSON
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [(b'content-type', b'application/json')]
        })
        await send({
            'type': 'http.response.body',
            'body': json.dumps({'result': mean_value}).encode('utf-8')
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