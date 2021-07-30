# AI3SW django-be polls app
Django backend app for polls application

## Supported APIs

### Get all questions and options

#### Request

`GET /questions`

#### Response

    HTTP/1.1 200 OK
    Date: Thu, 29 July 2021 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    {
        "questions": [
            {
                "id": 1,
                "text": "",
                "options": [
                    {
                        "id": 1,
                        "text": "",
                        "weight": 0.2
                    },
                    ...
                ]
            },
            ...
        ]
    }

### Store game results

#### Request

`POST /result`

`{"session_id":"", "question_list":[], "option_list":[], "n_turns":int}`

#### Response

    HTTP/1.1 201 Created
    Date: Thu, 29 July 2021 12:36:30 GMT
    Status: 201 Created
    Connection: close
    Content-Type: application/json