# Loan Management System

### API endpoints to a minimal loan management system.

### Technologies used:
1. Django
2. Django REST framework
3. PostgreSQL
4. Docker
5. Docker Compose

### Introduction to codebase:
1. [backend](./backend) : The API endpoints folder with all settings and configuration.
2. [Dockerfile](./backend/Dockerfile) : Dockerfile to build the image for the backend APIs.
3. [requirements.txt](./backend/requirements.txt) : Requirements file with all the necessary dependencies required to run the project.
4. [docker-compose.yml](docker-compose.yml) : YAML file configure the back end, and the database service.
5. [user](./backend/user) : App for user authentication and user roles and permissions.
6. [loan](./backend/loan) : App for the loan management of the users.

### Steps to run the projects:

**Pre-requites:**
1. python3.7 or greater
2. docker version 20.10.x
3. docker-compose version 1.29.x

**Steps:**
1. Navigate to the directory with [Dockerfile](./backend/Dockerfile) and use the following command:
```buildoutcfg
docker build --force-rm -t backend:latest .
```

2. Check your local docker image repository to see if the image has been built. Use command:
```buildoutcfg
docker images
```
3. Navigate to the folder with [docker-compose.yml](./docker-compose.yml).
4. To run migrations and set up the database, use commands:
```buildoutcfg
docker-compose run --rm apis python manage.py makemigrations user
docker-compose run --rm apis python manage.py makemigrations loan
docker-compose run --rm apis python manage.py migrate
```
5. To start the development server, use command:
```buildoutcfg
docker-compose up --remove-orphans
```
6. To shut the development serve, use command:
```buildoutcfg
docker-compose down --remove-orphans
```
**7. IMPORTANT: To test the backend with test cases, use command:**
```buildoutcfg
docker-compose run --rm apis python manage.py test
```
8. Create the first admin user of the system using command:
```buildoutcfg
docker-compose run --rm apis python manage.py createsuperuser
```

#### Description and Test cases of API endpoints:

* Base URL : http:127.0.0.1:8000/api
* User APIs:
    1. Signup: /user/signup/
        1. This endpoint can be used to sign up a user(customer or agent).
        2. Cannot signup if user already exists.
        3. Tokens have a validity of 2 hours only after which re-login is required.
        4. A user token is generated on successful registration.
        5. POST request has to be sent to this endpoint. 
    2. Create Admin: /user/create-admin/
        1. This endpoint can be used by ADMINS ONLY to make more admin users.
        2. Authorization of admin level required to access this endpoint.
        3. POST request has to be sent to this endpoint.
    3. Login : /user/login/
        1. This endpoint can be used to log in by admin, agent or customer.
        2. Cannot log in agent if it is not approved by the admin.
        3. Admin and Customer can login using correct credentials directly.
        4. A user token is generated on successful login.
        5. Tokens have a validity of 2 hours only after which re-login is required.
        6. POST request has to be sent to this endpoint.
    4. Profile : /user/profile/
        1. This endpoint can display the user information depending on the authorization token present in the header.
        2. Authorization is required to access this endpoint.
        3. GET request has to be sent to this endpoint.
    5. List Users(Agent) : /user/list-agent/
        1. This endpoint can be used by AGENTS OR ADMINS to list the customers present in the system.
        2. Customer role cannot access this endpoint.
        3. Authorization required to access this endpoint.
        4. GET request has to be sent to this endpoint.
    6. List Users(Admin) : /user/list-approvals/
        1. This endpoint can be used by ADMINS only to list the customers and agents present in the system.
        2. Customer and Agent role cannot access this endpoint.
        3. Authorization required to access this endpoint.
        4. GET request has to be sent to this endpoint.
    7. Approve or Delete and Agent : /user/approve-delete/<int:pk>/
        1. This endpoint can be used by ADMINS only to list approve an agent to the system or delete one.
        2. Customer and Agent role cannot access this endpoint.
        3. Authorization required to access this endpoint.
        4. PUT request with agent id as a URL parameter can be used to approve an agent.
        5. DELETE request with agent id as a URL parameter can be used to delete an agent.