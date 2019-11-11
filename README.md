# seawatch_planner
⛴ Software for planning SeaWatch's rescue operations

SeaWatch Planner is an application which should support SeaWatch by planning their operations. It allows volunteers to register theirself to help SeaWatch. These volunteers create a profile with availabilitys where they have time to volunteer for SeaWatch Operations.
SeaWatch Planner allows the crewing staff to use these Informations in their crewing process and request documents and other information of the volunteers.

## How to run the application
To run the application you have to use `docker-compose`, so make sure `docker-compose` is installed. 
You can start the application with the command `docker-compose up`. The Django app and the database will then start up. 
The application can be reached at `localhost:8081/`.

## How to test the application
For testing the application, start the app as described before. Then run the following command: 

`docker exec -it seawatch_planner_web_1 python manage.py test`

## How to create a Django admin user
To create a Django admin user, start the app as described before. Then run the following command: 

`docker exec -it seawatch_planner_web_1 python manage.py test`
