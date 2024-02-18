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


## TODOS:
There several feature to be done for production ready API:
* `Alembic` migrations
* `.env` configuration for different environments
* `Dockerfile` for deployment into docker-compose/Kubernetes
* `API test coverage`. For the moment CRUD test coverage is implemented
* `HATEOAS` and `Pagination` for endpoints that return multiple entries
* `Versioning` of the API