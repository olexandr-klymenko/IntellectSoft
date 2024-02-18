# The task descriptions

Develop a RESTful API service using your preferred web framework
(such as FastAPI, Django, or Flask).  
This service will offer CRUD operations for Client entities
and their corresponding Requests entities.  
Additionally, there will be an Operator entity responsible for  
updating the Status of the Request entity.  
Note that CRUD operations for the Operator entity are not required.  
Utilize the Object-Relational Mapping (ORM) of your choice.  
The basic structure of the entities should include the following fields:

### Client:
- Id
- First Name
- Last Name
- Phone

### Request:
- Id
- Body
- Status (Pending, Completed, Rejected)
- Processed By (Operator Id)

### Operator:
- Id
- First Name
- Last Name

# Pre-requisites
`Poetry` is recommended to help manage the dependencies and virtualenv.
```sh
$ pip install poetry
```

# Usage

## Installing with Poetry
```sh
# Install packages with poetry
$ poetry install
```

## Running
```sh
$ uvicorn customer_support_api.main:app
```

## Playing around with REST API
You can make requests to API in swagger UI.
open in browser http://127.0.0.1:8000/docs

## REST API flow example:
### Create customer
```sh
$ curl -X 'POST' \
  'http://127.0.0.1:8000/api/customers/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name": "Ed",
  "last_name": "Stark",
  "phone": "+442083661171"
}
```
```json
{
  "first_name": "Ed",
  "last_name": "Stark",
  "phone": "+442083661171",
  "id": 1
}
```

### Create operator 
```sh
$ curl -X 'POST' \
  'http://127.0.0.1:8000/api/operators/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name": "Jennie",
  "last_name": "Lanister"
}'
```
```json
{
  "first_name": "Jennie",
  "last_name": "Lanister",
  "id": 1
}
```
### Create request
```sh
$ curl -X 'POST' \
  'http://127.0.0.1:8000/api/customers/1/requests' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "body": "Winter is coming"
}'
```
```json
{
  "body": "Winter is coming",
  "id": 1,
  "created_by": 1,
  "status": "PENDING",
  "processed_by": null,
  "resolution_comment": null
}
```
### Assign request to operator
```shell
$ curl -X 'PATCH' \
  'http://127.0.0.1:8000/api/operators/1/requests/1' \
  -H 'accept: application/json'
```
```json
{
  "body": "Winter is coming",
  "id": 1,
  "created_by": 1,
  "status": "IN_PROGRESS",
  "processed_by": 1,
  "resolution_comment": null
}
```
### Complete request
```shell
curl -X 'PATCH' \
  'http://127.0.0.1:8000/api/requests/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "status": "COMPLETED",
  "resolution_comment": "Keep yourself warm"
}'
```
```json
{
  "body": "Winter is coming",
  "id": 1,
  "created_by": 1,
  "status": "COMPLETED",
  "processed_by": 1,
  "resolution_comment": "Keep yourself warm"
}
```
### Get requests by customer
```shell
curl -X 'GET' \
  'http://127.0.0.1:8000/api/customers/1/requests' \
  -H 'accept: application/json'
```
```json
[
  {
    "body": "Winter is coming",
    "id": 1,
    "created_by": 1,
    "status": "COMPLETED",
    "processed_by": 1,
    "resolution_comment": "Keep yourself warm"
  }
]
```
### Delete (Archive) request
```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8000/api/requests/1' \
  -H 'accept: */*'
```

## TODOS:
There several feature to be done for production ready API:
* `Alembic` migrations
* `.env` configuration for different environments
* `Dockerfile` for deployment into docker-compose/Kubernetes
* `API test coverage`. For the moment CRUD test coverage is implemented
* `HATEOAS` and `Pagination` for endpoints that return multiple entries
* `Versioning` of the API