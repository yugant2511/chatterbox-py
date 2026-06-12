Let's document everything properly. Here's your full Phase 1 revision notes:

What we built:
A running FastAPI server — the Python equivalent of a Spring Boot app.

1. Virtual Environment (venv)
bash

python -m venv venv
.\venv\Scripts\activate

Creates an isolated Python environment for this project
Equivalent of Maven's dependency scope in Java
You know it's active when (venv) appears in terminal
Always activate before working on the project


2. Installing Dependencies
bash

pip install fastapi uvicorn

pip = Maven for Python
fastapi = the web framework (equivalent of Spring Boot)
uvicorn = the server that runs FastAPI (equivalent of embedded Tomcat)


3. main.py breakdown
pythonfrom fastapi import FastAPI        # import the framework

app = FastAPI()                    # create the app instance

@app.get("/")                      # register a GET route at "/"
def root():
    return {"message": "ChatterBox API is running"}
PythonJava Equivalentfrom fastapi import FastAPIimport org.springframework.boot...app = FastAPI()@SpringBootApplication class@app.get("/")@GetMapping("/")return {"message": ...}ResponseEntity.ok(...)

4. Running the server
bashuvicorn main:app --reload

main = your filename (main.py)
app = your FastAPI instance name
--reload = auto-restart on code change (like Spring DevTools)


5. Two important URLs

http://localhost:8000 → your API root
http://localhost:8000/docs → Swagger UI (auto-generated, no setup needed unlike Spring Boot)








## Routes

- `@app.get("/")` → GET route
- `@app.post("/users")` → POST route
- Multiple routes can exist in same file

## Pydantic Models (DTOs)

- Equivalent of Java DTO + @Valid
- Automatically validates incoming JSON
- If a required field is missing → FastAPI returns 422 error automatically

### Example:
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

- `BaseModel` = base class (like extending a Java class)
- Fields defined with type hints (`str`, `int`, `bool`)
- FastAPI reads request body automatically — no `@RequestBody` needed

## Key difference from Java:
- Java: `@RequestBody UserCreate user`
- Python: just `user: UserCreate` in function params — FastAPI handles the rest






## Path Parameters

- Defined using `{param_name}` in the route
- Extracted automatically by FastAPI
- Type is enforced — wrong type returns 422

### Example:
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

- Equivalent of @PathVariable in Java
- Access: http://localhost:8000/users/5

## Query Parameters

- Defined as function parameters WITHOUT `{}` in route
- Optional when given a default value with `=`
- Multiple params separated by `&` in URL

### Example:
@app.get("/messages")
def get_messages(limit: int = 10, skip: int = 0):
    return {"limit": limit, "skip": skip}

- Equivalent of @RequestParam in Java
- Access: http://localhost:8000/messages?limit=5&skip=10

## Key difference from Java:
- Java: `@PathVariable int id`, `@RequestParam int limit`
- Python: FastAPI figures it out automatically
  - param matches `{name}` in route → path parameter
  - param doesn't match → query parameter

  ## Status Codes and Error Handling

### Setting status codes:
@app.post("/users", status_code=status.HTTP_201_CREATED)
- Default is 200
- 201 = resource created
- Import `status` from fastapi for readable constants

### Raising HTTP errors:
from fastapi import HTTPException

raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found"
)

- Equivalent of `throw new ResponseStatusException()` in Java
- `raise` = `throw` in Java
- `detail` = error message in response
- FastAPI automatically returns proper JSON error response

### Common status codes:
- 200 = OK (default)
- 201 = Created
- 400 = Bad Request
- 401 = Unauthorized
- 404 = Not Found
- 422 = Validation Error (automatic by Pydantic)
- 500 = Internal Server Error