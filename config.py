import os

CSRF_ENABLED = True
SECRET_KEY = os.urandom(24)
SQLALCHEMY_DATABASE_URI = \
    'postgresql+psycopg2://postgres:azazel56@localhost:5432/janes_voyages'
SQLALCHEMY_MIGRATE_REPO = 'enterprise_app_project/db_repository'
