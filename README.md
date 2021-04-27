# Persona API
The Persona API is a fake RESTful API that delivers made up data on a few endpoints. The data sits within a zip file and needs to be decompressed only on deployment. A crucial task is to find a way to do that in an elegant manner.

## Requirements
We would like to see best practice developing the API, structuring your project and code, documentation and security. Your server will need to be able to ingest new data and we are expecting to see good use of design patterns where needed. The tasks that need to be completed can be seen in the following sections.

## Deliverables

### Endpoints
You will need to deliver the following endpoints:

- GET /search/{username} Searches the data for the specific username
- GET /people Returns all people with pagination
- DELETE /people/{username} Delete a person

Produce a Swagger UI that will allow us to test the endpoints as a minimum.

### Tests
Write unit tests to cover key areas of the code. We are expecting to see at least one unit test per endpoint. 

### Documentation
Write a short README that describes how your server works and how to run it.

## Nice To Haves
- Dockerise your web server
- Create a simple front-end that allows users to search for a person
