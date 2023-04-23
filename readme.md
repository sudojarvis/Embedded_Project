Install xgboost on linux

 1. sudo pip install xgboost
 2. pip install djangorestframework

python manage.py runserver

go to http://localhost:8000/sensordata/ to start sensor data being stored in the database.

go to http://localhost:8000/home/ to predict temperature, humidity and and water level.
Enter the 24 hour format of the time you want to predict for and click on submit.