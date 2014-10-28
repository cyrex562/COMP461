################################################################################
# IMPORTS
################################################################################
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
import os.path
from enterprise_app_project import db


################################################################################
# DEFINES
################################################################################
################################################################################
# FUNCTIONS
################################################################################
def run():
    db.create_all()

    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    else:
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO,
                            api.version(SQLALCHEMY_MIGRATE_REPO))


################################################################################
# ENTRY POINT
################################################################################
if __name__ == '__main__':
    run()


################################################################################
# END OF FILE
################################################################################