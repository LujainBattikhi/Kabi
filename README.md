# Kabi Project

## A Job Search E-Platform 

Aiming to retrieve jobs from glassdoor and enable users to search for them in a more user-friendly way.

## Branch naming convention

1. Feature: `feature/some-text-with-dashes`
2. Hot fix: `hotfix/some-text-with-dashes`
3. Support: `support/some-text-with-dashes`
4. Release: `release/1.0.1`
5. Development: `develop`
6. Stable: `master`

## Developer's setup

Please note that you need the .env file from a teammate.

1. install docker and docker compose on your local PC (docker machine is optional)
1. Run `make services` in one shell, wait until all services are ready. There is also `make services-d` to run them in
   background.
1. Run `make image` to build fresh image of the app
1. Now you have couple of options
    1. Run `make tests` to run tests against that image
    2. Run `make dev-run` to run the image as a server and celery worker, open http://localhost:8080 (or your docker
        machine IP address) to play with it
    3. Don't forget to run `make dev-migrate` to run migrations if needed
    4. Run `make dev-ssh` to ssh into running django container
    5. Run `make clean` to down all containers and clean database directories
    6. Run `make help` to get some extra help, read Makefile to see what is going on behind the scenes

