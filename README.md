# dsclub
App for data science club

Instructions for running the app:

1. Install python 2.7 and MySQL 5.7;

2. Install Flask and other packages in the "requirements.txt" file;

3. Set up local database

mysql ->
CREATE USER '<admin_name>'@'localhost' IDENTIFIED BY '<password>';
CREATE DATABASE <database_name>;
GRANT ALL PRIVILEGES ON <database_name> . * TO '<admin_name>'@'localhost';
FLUSH PRIVILEGES;

4. Update the "instance/config.py" file

5. Run the following commands:

$cd dsclub
$export FLASK_CONFIG=development
$export FLASK_APP=run.py
$flask db init
$flask db migrate
$flask db upgrade
$flask run
