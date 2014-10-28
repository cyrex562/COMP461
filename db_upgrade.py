################################################################################
# IMPORTS
################################################################################
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO


################################################################################
# DEFINES
################################################################################
################################################################################
# FUNCTION
################################################################################
def run():
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print 'Current database version: ' + str(
        api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO))


################################################################################
# ENTRY POINT
################################################################################
if __name__ == '__main__':
    run()


################################################################################
# END OF FILE
################################################################################
