from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.executor import MigrationExecutor
from django.conf import settings
from .initials import create_initial


def is_database_synchronized(database=DEFAULT_DB_ALIAS):
    connection = connections[database]
    connection.prepare_database()
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    return not executor.migration_plan(targets=targets)


def charge_initial():
    if settings.CHARGE_DATA_DEFAULT:
        if is_database_synchronized(DEFAULT_DB_ALIAS):
            create_initial()
    return

