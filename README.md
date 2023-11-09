# Itinero
Personal Travel Recommendation Model

[Figma Wireframe](https://www.figma.com/team_invite/redeem/mGhBfs7l41S3IAZCViwB4f)

# Setting up PostgreSQL Database

### Step 1: Download and Install PostgreSQL

- Visit the official PostgreSQL website & download the installer appropriate for your operating system:
https://www.postgresql.org/download/


### Step 2: Follow the installation prompts

- Keep the default install directory
- **Uncheck *StackBuilder* from "Select Components".**
- Keep default Data Directory.
- Set superuser password - *Remember It*
- Keep default port (5432).
- Keep Default Locale - Language option

### Step 3: Start PgAdmin4

- Open *Servers* drop down menu.
- Enter the password from installation when prompted.


### Step 4: Create a new local database

- Right-click on the "Database" in the dropdown menu.
- Select Create -> Database...
- Name database: itinero_db
- Save
- Double check database is initialized correctly by going back to the dropdown menu and selecting the newly created database.



# Setting up a Django Project with PostgreSQL and psycopg2-binary

### Step 1: Install Python and pip

Make sure you have Python and Pip installed on your system.
This project works with Python 3.11.6+ and should by default already come with pip installed.

### Step 2: Clone this repository and CD to the folder


### Step 3: Install Django and psycopg2-binary

```
pip install django psycopg2-binary
```
### Step 4: Edit the Setting.py file
- In backend/django/itinero directory edit the database line in the Settings.py file and add your password to the field.
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'itinero_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```
### Step 5: Move To Backend Directory

```
cd backend/django/itinero
```

### Step 6: Migrate and Run the Server

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Now your Django project is set up with a PostgreSQL database. You can access the development server at `http://127.0.0.1:8000/`.

### Access the URLs in your web browser:
   - Login: [http://127.0.0.1:8000/login](http://127.0.0.1:8000/login)
   - Register: [http://127.0.0.1:8000/register](http://127.0.0.1:8000/register)



# How to utilize the 'CrimeClassifier' class of Itinero

### Step 1: Download Git LFS

The path file containing the current model state of the 'CrimeClassifier' feature of Itinero is too large to add to the repository.
Therefore, it is necessary to download Git Large File Storage (LFS) from:
https://git-lfs.com/
This Git extension will be automatically added to your native 'git' path on your PC.

### Step 2: Fetching the 'best_crime_classifier_state.pth' file

Once you have pulled the most recent code into your repo, with Git LFS installed, go to your repo's terminal/console and run:

```
git lfs install
git lfs fetch
```

*Note:
    - It is only necessary to run the commands above when Git LFS has NOT been set up yet, after that, a simple pull request will suffice.

## Now you will have any and all 'large files' within the '.gitattributes' directory installed locally

### Step 3: Utilizing the 'CrimeClassifier' feature/class

Any and all functions of the CrimeClassifier feature are defined within the 'itinero_model.py' file within "Itinero/backend/app"

In short, as long as you import the file and class at the top of your code...

```
from itinero_model import CrimeClassifier
```

...and you create an object instance of the class:

```
crime_classifier = CrimeClassifier()
```

You can use any of its functions freely.

## A short demo of how to utilize the feature can be found in "Itinero/backend/app/__init__.py"



