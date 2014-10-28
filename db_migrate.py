################################################################################
# IMPORTS
################################################################################
import imp
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from enterprise_app_project import db


################################################################################
# DEFINES
################################################################################


################################################################################
# FUNCTIONS
################################################################################
def run():
    migration = SQLALCHEMY_MIGRATE_REPO + '/versions/%03d_migration.py' % \
                                          (api.db_version(
                                              SQLALCHEMY_DATABASE_URI,
                                              SQLALCHEMY_MIGRATE_REPO)
                                           + 1)
    tmp_module = imp.new_module('old_model')
    old_model = api.create_model(SQLALCHEMY_DATABASE_URI,
                                 SQLALCHEMY_MIGRATE_REPO)
    exec old_model in tmp_module.__dict__
    script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI,
                                              SQLALCHEMY_MIGRATE_REPO,
                                              tmp_module.meta, db.metadata)
    open(migration, 'wt').write(script)
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print 'new migration saved as {0}'.format(migration)
    print 'current database version: {0}'.format(
        str(api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)))


################################################################################
# ENTRY POINT
################################################################################
if __name__ == '__main__':
    run()


################################################################################
# END OF FILE
################################################################################


# END OF FILE
