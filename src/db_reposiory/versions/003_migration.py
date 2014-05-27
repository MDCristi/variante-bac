from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
answer = Table('answer', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text', String(length=500)),
    Column('correct', Boolean),
    Column('question_id', Integer),
)

question = Table('question', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text', String(length=500)),
    Column('varianta_id', Integer),
)

varianta = Table('varianta', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('description', String(length=80)),
    Column('user_id', SmallInteger),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['answer'].create()
    post_meta.tables['question'].create()
    post_meta.tables['varianta'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['answer'].drop()
    post_meta.tables['question'].drop()
    post_meta.tables['varianta'].drop()
