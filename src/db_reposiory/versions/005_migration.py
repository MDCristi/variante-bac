from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
varianta = Table('varianta', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('description', String),
    Column('user_id', SmallInteger),
    Column('category', String),
)

quiz = Table('quiz', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('description', String(length=80)),
    Column('timestamp', DateTime),
    Column('last_time_solved', DateTime),
    Column('votes', Integer),
    Column('category', String(length=80)),
    Column('user_id', SmallInteger),
)

quiz_votes = Table('quiz_votes', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('timestamp', DateTime),
    Column('author', Integer),
)

user_activity = Table('user_activity', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('timestamp', DateTime),
    Column('quiz_id', Integer),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=60)),
    Column('email', String(length=140)),
    Column('role', SmallInteger, default=ColumnDefault(0)),
    Column('created_quizes', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['varianta'].drop()
    post_meta.tables['quiz'].create()
    post_meta.tables['quiz_votes'].create()
    post_meta.tables['user_activity'].create()
    post_meta.tables['user'].columns['created_quizes'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['varianta'].create()
    post_meta.tables['quiz'].drop()
    post_meta.tables['quiz_votes'].drop()
    post_meta.tables['user_activity'].drop()
    post_meta.tables['user'].columns['created_quizes'].drop()
