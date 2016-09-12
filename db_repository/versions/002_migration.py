from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
wager = Table('wager', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('week_num', Integer),
    Column('wager_type', String(length=40)),
    Column('wager_team', String(length=100)),
    Column('wager_amount', Float),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['wager'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['wager'].drop()
