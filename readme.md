Install xgboost and djangorestframework

 1. sudo pip install xgboost
 2. pip install djangorestframework

Before running arduino code
    
     1. Change the ssid and password to your wifi network.
     2. Change the ip address to the ip address of your computer.
     3. Change the port to the port you want to use.
        go to utils.py and change the port to the same port you used in the arduino code.

To run the django server

1. clone the repository
2. cd mysite
3. python manage.py runserver

go to http://localhost:8000/sensordata/ to start sensor data being stored in the database.

go to http://localhost:8000/home/ to predict temperature, humidity and and water level.
Enter the 24 hour format of the time you want to predict for and click on submit.
