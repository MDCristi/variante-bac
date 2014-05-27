from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
quiz = Table('quiz', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('description', String),
    Column('timestamp', DateTime),
    Column('last_time_solved', DateTime),
    Column('votes', Integer),
    Column('category', String),
    Column('user_id', SmallInteger),
)

quiz_votes = Table('quiz_votes', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('timestamp', DateTime),
    Column('author', Integer),
)

user_activity = Table('user_activity', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('timestamp', DateTime),
    Column('quiz_id', Integer),
    Column('user_id', Integer),
)

varianta = Table('varianta', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('description', String(length=80)),
    Column('category', String(length=80)),
    Column('user_id', SmallInteger),
)

question = Table('question', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text', String),
    Column('quiz_id', Integer),
)

question = Table('question', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text', String(length=500)),
    Column('varianta_id', Integer),
)

user = Table('user', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('email', String),
    Column('role', SmallInteger),
    Column('created_quizes', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['quiz'].drop()
    pre_meta.tables['quiz_votes'].drop()
    pre_meta.tables['user_activity'].drop()
    post_meta.tables['varianta'].create()
    pre_meta.tables['question'].columns['quiz_id'].drop()
    post_meta.tables['question'].columns['varianta_id'].create()
    pre_meta.tables['user'].columns['created_quizes'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['quiz'].create()
    pre_meta.tables['quiz_votes'].create()
    pre_meta.tables['user_activity'].create()
    post_meta.tables['varianta'].drop()
    pre_meta.tables['question'].columns['quiz_id'].create()
    post_meta.tables['question'].columns['varianta_id'].drop()
    pre_meta.tables['user'].columns['created_quizes'].create()
