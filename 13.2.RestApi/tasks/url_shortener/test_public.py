import typing as tp

from fastapi.testclient import TestClient

from .url_shortener import app

client = TestClient(app)

openapi_schema: dict[str, tp.Any] = {
    'openapi': '3.1.0',
    'info': {'title': 'FastAPI', 'version': '0.1.0'},
    'paths': {
        '/shorten': {
            'post': {
                'responses': {
                    '201': {
                        'description': 'Successful Response',
                        'content': {'application/json': {'schema': {'$ref': '#/components/schemas/Shorted'}}},
                    },
                    '422': {
                        'description': 'Validation Error',
                        'content': {
                            'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}},
                    }
                },
                'requestBody': {
                    'content': {'application/json': {'schema': {'$ref': '#/components/schemas/ToShort'}}},
                    'required': True
                },
                'summary': 'Short Url',
                'operationId': 'short_url_shorten_post',
            }
        },
        '/go/{key}': {
            'get': {
                'parameters': [{
                    'in': 'path',
                    'name': 'key',
                    'required': True,
                    'schema': {'title': 'Key', 'type': 'string'},
                }],
                'responses': {
                    '307': {
                        'description': 'Successful Response',
                        'content': {'application/json': {'schema': {'title': 'Response Redirect To Url Go  Key  Get'}}},
                    },
                    '422': {
                        'description': 'Validation Error',
                        'content': {
                            'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}
                        },
                    }
                },
                'summary': 'Redirect To Url',
                'operationId': 'redirect_to_url_go__key__get',
            }
        },
    },
    'components': {
        'schemas': {
            'Shorted': {
                'properties': {
                    'key': {'title': 'Key', 'type': 'string'},
                    'url': {'title': 'Url', 'type': 'string'}
                },
                'required': ['url', 'key'],
                'title': 'Shorted',
                'type': 'object'
            },
            'ToShort': {
                'properties': {
                    'url': {'title': 'Url', 'type': 'string'}
                },
                'required': ['url'],
                'title': 'ToShort',
                'type': 'object'
            },
            'HTTPValidationError': {
                'properties': {
                    'detail': {
                        'items': {'$ref': '#/components/schemas/ValidationError'},
                        'title': 'Detail',
                        'type': 'array'
                    }
                },
                'title': 'HTTPValidationError',
                'type': 'object'
            },
            'ValidationError': {
                'properties': {
                    'loc': {
                        'title': 'Location',
                        'type': 'array',
                        'items': {
                            'anyOf': [{'type': 'string'}, {'type': 'integer'}]
                        }
                    },
                    'msg': {'title': 'Message', 'type': 'string'},
                    'type': {'title': 'Error Type', 'type': 'string'}
                },
                'required': ['loc', 'msg', 'type'],
                'title': 'ValidationError',
                'type': 'object'
            }
        }
    },
}


class TestOpenapiSchema:
    def test_schema_available(self) -> None:
        response = client.get('/openapi.json')
        assert response.status_code == 200, response.text

    def test_schemas(self) -> None:
        response_schema = client.get('/openapi.json').json()
        print(response_schema['components']['schemas'])
        assert 'ToShort' in response_schema['components']['schemas'], 'Name /shorten input model as <ToShort>'
        assert 'Shorted' in response_schema['components']['schemas'], 'Name /shorten output model as <Shorted>'
        assert response_schema['components']['schemas']['ToShort'] == openapi_schema['components']['schemas']['ToShort']
        assert response_schema['components']['schemas']['Shorted'] == openapi_schema['components']['schemas']['Shorted']
        assert response_schema['components']['schemas'] == openapi_schema['components']['schemas']

    def test_paths(self) -> None:
        response_schema = client.get('/openapi.json').json()
        assert '/shorten' in response_schema['paths'] and 'post' in response_schema['paths']['/shorten'], \
            'Did you forget to add /shorten endpoint?'
        assert '/go/{key}' in response_schema['paths'] and 'get' in response_schema['paths']['/go/{key}'], \
            'Did you forget to add /go endpoint?'
        assert response_schema['paths']['/shorten']['post']['summary'] == \
               openapi_schema['paths']['/shorten']['post']['summary'], \
               'Change /shorten function name to get right summary'
        assert response_schema['paths']['/go/{key}']['get']['summary'] == \
               openapi_schema['paths']['/go/{key}']['get']['summary'], \
               'Change /go function name to get right summary'

        assert response_schema['paths']['/go/{key}']['get']['responses']['307'] == \
               openapi_schema['paths']['/go/{key}']['get']['responses']['307']
        assert response_schema['paths']['/go/{key}']['get']['responses']['422'] == \
               openapi_schema['paths']['/go/{key}']['get']['responses']['422']

        assert response_schema['paths'] == openapi_schema['paths']

    def test_full_schema(self) -> None:
        response_schema = client.get('/openapi.json').json()
        assert response_schema == openapi_schema


class TestShorten:
    def test_good_request(self) -> None:
        response = client.post('/shorten', json={'url': 'https://testurl.com/'})
        assert response.status_code == 201, response.text
        assert response.json()['url'] == 'https://testurl.com/'
        assert len(response.json()['key']) > 0

    def test_bad_request(self) -> None:
        response = client.post('/shorten', json={'definitely_not_url': 'https://testurl.com/'})
        assert response.status_code == 422, response.text

    def test_different_urls(self) -> None:
        keys = set()
        for i in range(10):
            response = client.post('/shorten', json={'url': f'https://testurl.com/{i}'})
            assert response.status_code == 201, response.text
            key = response.json()['key']
            assert key not in keys
            keys.add(key)

    def test_same_url_multiple_time(self) -> None:
        response = client.post('/shorten', json={'url': 'https://testurl.com/'})
        assert response.status_code == 201, response.text
        base_key = response.json()['key']

        for i in range(10):
            response = client.post('/shorten', json={'url': 'https://testurl.com/'})
            assert response.status_code == 201, response.text
            key = response.json()['key']
            assert key == base_key


class TestGo:
    def test_good_request(self) -> None:
        response = client.post('/shorten', json={'url': 'https://testurl.com/'})
        key = response.json()['key']

        response = client.get(f'/go/{key}', allow_redirects=False)
        assert response.status_code == 307, response.text
        assert response.headers['location'] == 'https://testurl.com/'

    def test_bad_request(self) -> None:
        response = client.get('/go/wrong_key', allow_redirects=False)
        assert response.status_code == 404, response.text
