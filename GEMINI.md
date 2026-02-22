# GEMINI.md

This file provides a comprehensive overview of the CS50 Final Project, a Flask-based web application for managing students, programs, and subjects.

## Project Overview

This project is a web application built with Flask that allows administrators to manage academic information. The key features include:

*   **User Authentication:**  Login/logout functionality for administrators and students.
*   **Admin Dashboard:** A central place for administrators to view statistics and manage academic data.
*   **Academic Management:** Administrators can add, view, and manage students, programs, and subjects.
*   **Student Information System:** The application stores and manages information about students, their programs, and the subjects they are enrolled in.

### Technologies Used

*   **Backend:** Python with the Flask framework.
*   **Database:** A relational database is used, with SQLAlchemy as the ORM. The specific database is MySQL, as indicated by the `mysql_errors` import.
*   **Frontend:** The frontend uses HTML templates with Jinja2, and JavaScript for dynamic functionality.
*   **Authentication:** User authentication is handled by Flask-Login.
*   **PDF Generation:** The `weasyprint` library is included, suggesting that there is functionality for generating PDF documents.

### Project Structure

The project follows a standard Flask application structure:

```
c:\Users\setho\Documents\code\cs50_FinalProject\
├───.gitignore
├───GEMINI.md
├───requirements.txt
├───run.py
├───app\
│   ├───__init__.py
│   ├───db.py
│   ├───decorators.py
│   ├───models.py
│   ├───routes\
│   │   ├───main.py
│   │   ├───admin\
│   │   │   └───admin.py
│   │   └───auth\
│   │       └───auth.py
│   ├───static\
│   └───templates\
└───...
```

*   `run.py`: The entry point to run the application (currently empty).
*   `requirements.txt`: Lists the Python dependencies for the project.
*   `app/`: The main application package.
    *   `__init__.py`: The application factory, where the Flask app is created and configured.
    *   `db.py`: Database configuration and setup.
    *   `decorators.py`: Custom decorators for the application (e.g., `admin_required`).
    *   `models.py`: Defines the database schema using SQLAlchemy.
    *   `routes/`: Contains the application's routes, organized into blueprints.
    *   `static/`: Static assets like CSS and JavaScript.
    *   `templates/`: HTML templates for the application.

## Building and Running

To run this project, you will need to have Python and the required dependencies installed.

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure the Database

The application uses a database, and the connection details are likely configured in a file that is not present in the file listing, probably `config.py`. You will need to create this file and set the appropriate database URI.

**`app/config.py`**

```python
SECRET_KEY = 'a-secret-key'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@host/database'
```

### 3. Running the Application

The `run.py` file is currently empty. To run the application, you can add the following code to it:

**`run.py`**

```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

Then, you can run the application with the following command:

```bash
python run.py
```

Alternatively, you can use the `flask` command:

```bash
export FLASK_APP=run:app
flask run
```

## Development Conventions

*   **Flask Blueprints:** The application is organized using Flask Blueprints to separate different parts of the application.
*   **SQLAlchemy ORM:** The application uses the SQLAlchemy ORM to interact with the database.
*   **Flask-Login:** User authentication is handled by the Flask-Login extension.
*   **Template Inheritance:** The application uses a base HTML template (`base.html`) that other templates extend.
*   **AJAX:** The application uses AJAX to handle some form submissions, providing a more dynamic user experience.
*   **Custom Decorators:** The application uses custom decorators (e.g., `@admin_required`) to restrict access to certain routes.
