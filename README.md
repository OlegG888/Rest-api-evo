# Tutorial for use API:<br />

In this tutorial we will go through an example of taking an existing simple web app based on Flask and MySQL with parsing function and making it run with Docker and docker-compose. <br />

When we start docker compose API create two containers **APP** and **DB**.<br />
We begin with the following project layout:<br />
**app.py** — contains the Flask app which connects to the database and exposes one REST API endpoint with simple html form for upload csv file.<br />
**init.sql** — an SQL script to initialize the database before the first time the app runs.<br /> 
# Dockerfile  <br />
```
# Since Flask apps listen to port 5000  by 
# default, we expose it
EXPOSE 5000

# Sets the working directory
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Run app.py when the container launches
COPY app.py /app
CMD python app.py

```
# Creating a docker-compose.yml <br />
```
 version: "2"
services:
  app:
    build: ./app
    links:
      - db
    ports:
      - "5000:5000"

```

* **build:** specifies the directory which contains the Dockerfile containing the instructions for building this service.<br />
* **links:** links this service to another container. This will also allow us to use the name of the service instead of having to find the ip of the database container, and express a dependency which will determine the order of start up of the container.<br />
* **ports:** mapping of Host : Container ports.<br />
```
db:
    image: mysql:5.7
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: root
    volumes:
      - ./db:/docker-entrypoint-initdb.d/:ro
      
```
* **image:**  writing a new Dockerfile, we are using an existing image from a repository.<br />
* **environment:** add environment variables to assign password for database. <br />
* **ports:** we use port 3306 to connect to the database.<br />
* **volumes:** Since we want the container to be initialized with our schema, we wire the directory containing our init.sql script to the entry point for this container, which by the image’s specification runs all .sql scripts in the given directory. <br />

# Configure connection to the database in app.py. <br />
``` 
# Database
mydb = mysql.connector.connect(
  host="db",
  user="root",
  password="root",
  port= "3306",
  database="csvdata"
)

```
We are connecting as root with the password configured in the docker-compose file. We can (and should) use the name ‘db’ since this is the name of the service we defined. <br />

# Running the app.
Go to the main directory in the terminal and enter the command:
``` 
$ docker-compose up
```
If everything went right, we will get:
``` 
app_1  |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 
```
