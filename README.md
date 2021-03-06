# ROLE BASED ACCESS CONTROL AUTH SERVICE

A "bootstrap" REST api for implementing a role based access control authentication and authorization service for your application ecosystem built using FastAPI and Postgres.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Pre-requisites

1. Docker - (Instructions on how to install can be found [here](https://docs.docker.com/install/) (God bless the creators and maintainers for docker!)
2. Docker-Compose (Instructions on how to install can be found [here](https://docs.docker.com/compose/install/)
3. Postgres - The application is configured to use an external postgres instance not in a Docker container. You can install PgAdmin to run postgres locally from [here](https://www.pgadmin.org/download/)

### Environment Variables

The application uses an .env file to manage environment varialbes. A `.env.sample` file is included in the project for your modification. (Remember to rename the file to `.env` in order for your environment variables to be read.)

The configuration can be changed to use the OS environment based on the FastAPI Settings documentation if you prefer.

### Get Up and running

Once the prerequisites are met, The following steps can be used to get the application up and running. All commands are run from the root directory of the project

1. Build the docker image using

```
docker-compose build
```

2. Run the application using (This step also all run all upgrade operations on the database using the most recent migration file)

```
docker-compose up
```

3. The service has inbuilt documentation based on OpenAPI Specifications (formerly Swagger) and can be accessed at

```
http://localhost:8000/docs
```

### Running the Tests

The application comes with a few basic tests which can be expanded based to suit other scenario's you may want to cover. A 'test.sh' script based on pytest is used to run the tests together with any pre-requistes it needs to run. The dependencies for testing are configured to run only when the `ENVIRONMENT` variable in your .env file is set to `test`.

Run the tests using

```
docker-compose run web sh -c "./test.sh"
```

## Built With

- [fastapi](https://fastapi.tiangolo.com/) - The web framework used
- [docker](https://www.docker.com/) - For application containerization
- [poetry](https://python-poetry.org/) - For dependency management
- [alembic](https://python-poetry.org/) - For database migrations

## Authors

- **Tsatsu Adogla-Bessa Jnr**

## Credit

This project was primarily made possible by the power, simplicity and wizardry of FastAPI built by [tiangolo](https://github.com/tiangolo).
I also took a lot of inspiration from his [full-stack-fastapi-postgres](https://github.com/tiangolo/full-stack-fastapi-postgresql) bootstrap project.

## License

This project is licensed under the terms of the MIT license.
