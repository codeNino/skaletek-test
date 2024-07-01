# Running My Python App with Pipenv and Docker Compose

This repository contains a Python application that utilizes Pipenv for managing dependencies and Docker Compose for containerization. Follow the steps below to set up and run the application.

## Prerequisites

Make sure you have the following installed on your system:
- Docker
- Docker Compose
- Python 3.9
- Pipenv

## Setup Instructions

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone <https://github.com/codeNino/skaletek-test>
cd <skaletek-test>
```


### 2. Create Virtual Environment and Install Dependencies

Use Pipenv to create a virtual environment and install dependencies:

```bash
pipenv install --dev
```

### 3. Run Tests with Pytest

Before building the Docker container, run tests using pytest:

```bash
pipenv run pytest
```

### 4. Build and Run the Docker Container
Use Docker Compose to build and run the Docker container in background:

```bash
docker compose up -d --build skaletek-srv
```

#### You can set an env file for your docker container to work with

##### create a .env file
 
 add an api key value to protect your service against aunthorized requests;

 API_KEY = "XXXXXX-XXXX"

Run container with:

```bash
docker compose --env-file .env up -d
```




