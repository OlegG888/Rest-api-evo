# Tutorial for use API:<br />

In this tutorial we will go through an example of taking an existing simple web app based on Flask and MySQL with parsing function and making it run with Docker and docker-compose. <br />
Steps: <br />
When we start docker compose, our API create two containers **APP** and **DB**.<br />
We begin with the following project layout:<br />
**app.py** — contains the Flask app which connects to the database and exposes one REST API endpoint with simple html form for upload csv file.<br />
**init.sql** — an SQL script to initialize the database before the first time the app runs.<br />

2. Upload file on the server .<br />
3. Upload the CSV using Flask.<br />
4. Parse CSV file data.<br />
5. Connect to the database.<br />
6. Insert rows into a specific table in the database. <br />