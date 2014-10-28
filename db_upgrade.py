# @file 
# @brief
# @author
# @copyright
# IMPORTS
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO


# DEFINES


# CLASSES


# GLOBALS


# FUNCTIONS


# ENTRY POINT
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print 'Current database version: ' + str(
    api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))

# END OF FILE
