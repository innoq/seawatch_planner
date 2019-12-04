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

# Coding conventions
We decided to use the the following coding conventions.

- Use PEP 8 coding style.
- If possible use Djangos generic class based views, for example ListView, CreateView, DetailView, UpdateView and DeleteView.
- ListViews are often represented with tables. For each dataset you have actions like delete this dataset of go to detail view. These actions are represented by links with fontawesome icon in the table and not by buttons.
- General actions like add a new dataset are represented by buttons with fontawesome icons outside of the table.
- Use the following table as an example for the url paths, the naming of the class of the views and the view name itself:

| url path              | class name of view | view name   |
| --------------------- | ------------------ | ----------- |
| ships/                | ShipListView       | ship_list   |
| ships/add             | ShipCreateView     | ship_create |
| ships/<int:pk>/       | ShipDetailView     | ship_detail |
| ships/<int:pk>/edit   | ShipUpdateView     | ship_update |
| ships/<int:pk>/delete | ShipDeleteView     | ship_delete |

