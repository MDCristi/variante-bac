from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
varianta = Table('varianta', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('valide', Boolean),
    Column('description', String(length=80)),
    Column('category', String(length=80)),
    Column('user_id', SmallInteger),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['varianta'].columns['valide'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['varianta'].columns['valide'].drop()
