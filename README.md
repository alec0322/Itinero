# Itinero
Personal Travel Recommendation Model

[Figma Wireframe](https://www.figma.com/team_invite/redeem/mGhBfs7l41S3IAZCViwB4f)

# Setting up PostgreSQL Database

### Step 1: Download and Install PostgreSQL

- Visit the official PostgreSQL website.
- Download the installer appropriate for your operating system.
- Follow the installation instructions provided by the installer.
- When prompted to install and setup stack build; check the box to skip.

### Step 2: Start the PostgreSQL Service

- After installation, start the PostgreSQL service.
- Start the pgAdmin4 client

### Step 3: Access the PostgreSQL Command Line

- Use the following command to access the PostgreSQL command line:

```bash
psql -U postgres
```

### Step 4: Create a New User (if necessary)

- Use the following SQL command to create a new user:

```
sqlCopy code
CREATE USER myuser WITH PASSWORD 'mypassword';
```

Replace 'myuser' with your desired username and 'mypassword' with your preferred password.

### Step 5: Create a New Database

- Use the following SQL command to create a new database:

```
CREATE DATABASE itinero_db;
```





# Setting up a Django Project with PostgreSQL and psycopg2-binary

### Step 1: Install Python and pip

Make sure you have Python and pip installed on your system.

### Step 2: Create a Virtual Environment

```bash
python3 -m venv myenv
source myenv/bin/activate  # for Linux/MacOS
myenv\Scripts\activate  # for Windows
```

### Step 3: Install Django and psycopg2-binary

```
pip install django psycopg2-binary
```

### Step 4: Move To Bacakend Directory

```
cd backend/django/itinero
```

### Step 7: Migrate and Run the Server

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Now your Django project is set up with a PostgreSQL database. You can access the development server at `http://127.0.0.1:8000/`.

### Step 8: Deactivate the Virtual Environment

```
deactivate
```


# To run the backend

1. Activate the environment:

    Windows:
    ```
    myenv\Scripts\activate
    ```

    MacOS:
    ```
    source myenv/Scripts/activate 
    ```


2. Start the server:
    ```
    python manage.py runserver
    ```

3. Access the URLs in your web browser:
   - Login: [http://127.0.0.1:8000/login](http://127.0.0.1:8000/login)
   - Register: [http://127.0.0.1:8000/register](http://127.0.0.1:8000/register)

