Develop a RESTful API service using your preferred web framework (such as FastAPI, Django, or Flask). This service will offer CRUD operations for Client entities and their corresponding Requests entities. Additionally, there will be an Operator entity responsible for updating the Status of the Request entity. Note that CRUD operations for the Operator entity are not required. Utilize the Object-Relational Mapping (ORM) of your choice.
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