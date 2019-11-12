# seawatch_planner
⛴ Software for planning SeaWatch's rescue operations

SeaWatch Planner is an application which should support SeaWatch by planning their operations. It allows volunteers to register theirself to help SeaWatch. These volunteers create a profile with availabilitys where they have time to volunteer for SeaWatch Operations.
SeaWatch Planner allows the crewing staff to use these Informations in their crewing process and request documents and other information of the volunteers.

## How to run the application
To run the application you have to use `docker`, you will find the installation instructions on https://docs.docker.com/v17.12/install/.

After you downloaded or cloned the repository switch to the directory containing the file `docker-compose.yml` and run

`docker-compose up -d` (`-d`starts the containers in a detached mode (containers run in background)).

The Django app and the database will then start up. 

### How to create a Django admin user
To create a superuser (you will need it to enter the admin interface) run

`docker exec -it seawatch_planner_web_1 python manage.py createsuperuser`

### Urls and ports
The application can be reached at `localhost:8001/`.

The admin interface can be reached at `localhost:8001/admin`.

If you want to change the ports edit them in the `docker-compose.yml` file.

## How to test the application
For testing the application, start the app as described before. Then run the following command: 

`docker exec -it seawatch_planner_web_1 python manage.py test`

