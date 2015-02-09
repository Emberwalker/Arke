# Arke
# User-configurable settings.

# Dirty little seeekrits...
SECRET_KEY='much_sekrit_such_secure_wow'

# Database
# See http://docs.sqlalchemy.org/en/rel_0_9/core/engines.html#database-urls
# With DEBUG defined, this is ignored and a SQLite DB in the root folder is used instead.
# SQLite is probably not the best for production, either...
DB_URL='sqlite:///arke.db'

# Development
DEBUG=True
