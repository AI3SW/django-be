# AI3SW django-be styletransfer app
Django backend app for style transfer application

## Supported APIs

### Get available style images

#### Request

`GET /style`

#### Response

    HTTP/1.1 200 OK
    Date: Thu, 29 July 2021 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    {
        "styles": [
            {
                "style_id": 1,
                "style_img": <b64 string>,
                "style_theme": <string>,
                "model": "stargan"
            },
            
            {
                "style_id": 2,
                "style_img": <b64 string>,
                "style_theme": <string>,
                "model": "simswap"
            },
        ]
    }

### Perform style transfer on an image

#### Request

`POST /result`

`{"session_id":"", "img":"", "style_id":int}`

#### Response

Success response:

    HTTP/1.1 200
    Date: Thu, 29 July 2021 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    {"output_img": "<Base64 encoded image>"}

Error response for styletransfer AI failure:

    HTTP/1.1 503
    Date: Thu, 29 July 2021 12:36:30 GMT
    Status: 503 Service Unavailable
    Connection: close