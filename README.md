# Django REST Framework Blog API

This project is a RESTful API for managing blog articles, categories, and tags. It allows users to create, read, update, and delete articles, as well as search for articles based on various criteria.

## Features

- *Article Management:*
    - Create, read, update, and delete articles.
    - Search articles by title, content, category, or tags.
- *Category Management:*
    - Associate articles with categories.
    - Automatically create categories if they don't exist.
- *Tag Management:*
    - Associate articles with tags.
    - Automatically create tags if they don't exist.
- *Search Functionality:*
    - Search articles using query parameters (`search`).

## Installation

*Prerequisites:*
- Python 3.6 or higher
- PostgreSQL

1. Clone the Repository

```
git clone https://github.com/Anguilla-anguilla/blogging_platform_API.git
cd blogging_platform_API
```

2. Set Up a Virtual Environment

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Dependencies

```
pip install -r requirements.txt
```

4. Set Up the Database
Create a PostgreSQL database for the project. Update the database settings in settings.py:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
Apply migrations:

```
python manage.py migrate
```

5. Run the Development Server

```
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/schema/swagger`.

[Project URL](https://roadmap.sh/projects/blogging-platform-api)