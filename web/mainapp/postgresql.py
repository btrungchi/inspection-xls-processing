import sqlalchemy

from sqlalchemy.schema import MetaData, Table, Column
from sqlalchemy.types import Date, Text, Integer, BigInteger


class PostgreSQLHolderConfig:
    user = 'docker'
    password = 'docker'
    host = 'localhost'
    port = 5432
    db = 'Inspectorio'


class PostgreSQLHolderUtils:
    @staticmethod
    def get_engine(user, password, host, port, db):
        print("get engine")
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(user, password, host, port, db)
        postgre_engine = sqlalchemy.create_engine(url, paramstyle="format")
        PostgreSQLHolderUtils.init_tables(postgre_engine)
        return postgre_engine

    @staticmethod
    def init_tables(postgre_engine, drop_all=False):
        with postgre_engine.begin() as connection:
            if not connection.dialect.has_table(connection, 'General Information'):
                metadata = MetaData(connection)
                Table('General Information', metadata,
                      Column('Date', Date, primary_key=True,
                             nullable=False),
                      Column('Vendor', Integer,
                             primary_key=True, nullable=False),
                      Column('BMP Vendor', Text),
                      Column('Vdr Contacts', Text,
                             nullable=False),
                      Column('Factory', Text, nullable=False),
                      Column('Fty Address', Text,
                             nullable=False),
                      Column('Fty Contacts', Text,
                             nullable=False),
                      Column('Auditor', Text, nullable=False),
                      Column('FRM Lebel', Text, nullable=False)
                      )
                metadata.create_all()

            if not connection.dialect.has_table(connection, 'SIP Elements'):
                metadata = MetaData(connection)
                Table('SIP Elements', metadata,
                      Column('Vendor Style/PID', Integer, primary_key=True,
                             nullable=False),
                      Column('PPR document', Text,
                             nullable=False),
                      Column('Red Seal Sample',
                             Text, nullable=False),
                      Column('Technical Specs & Construction',
                             Text, nullable=False),
                      Column('Final Item Set-Up form',
                             Text, nullable=False),
                      Column(
                          'Total Program Quantity and Deliveries', Text, nullable=False),
                      Column('Color Standards',
                             Text, nullable=False),
                      Column(
                          'Production Color/Finish Representation', Text, nullable=False),
                      Column(
                          'Trims, Accessories, Hardware, Components and Labeling', Text, nullable=False),
                      Column('Yellow Seal Sample',
                             Text, nullable=False),
                      Column('Product Testing Results',
                             Text, nullable=False),
                      Column('Floor Ready Requirements',
                             Text, nullable=False),
                      Column('Retail Packaging Design Sample',
                             Text, nullable=False),
                      Column('Carton marks and Labels',
                             Text, nullable=False),
                      Column(
                          'Factory Internal Reports – Inspection and Testing', Text, nullable=False),
                      Column('TCPS Inspection Reports',
                             Text, nullable=False),
                      Column('Completed Packing List',
                             Text, nullable=False)
                      )
                metadata.create_all()

            if not connection.dialect.has_table(connection, 'PIF Info'):
                metadata = MetaData(connection)
                Table('PIF Info', metadata,
                      Column('Vendor Style/PID', Integer, primary_key=True,
                             nullable=False),
                      Column('PO Number', BigInteger,
                             primary_key=True, nullable=False),
                      Column('Purpose', Text, nullable=False),
                      Column('Ship Begin Date',
                             Date, nullable=False),
                      Column('Ship End Date', Date, nullable=False)
                      )
                metadata.create_all()

            if not connection.dialect.has_table(connection, 'POM Info'):
                metadata = MetaData(connection)
                Table('POM Info', metadata,
                      Column('PID/Style', Integer, nullable=False),
                      Column('DPCI', Integer, nullable=False),
                      Column('PO Included', BigInteger,
                             nullable=False),
                      Column('Insp Type', Text, nullable=False),
                      Column('PO Qty', Integer, nullable=False),
                      Column('Available Qty',
                             BigInteger, nullable=False),
                      Column('Description', Text, nullable=False),
                      Column('PWI?', Text, nullable=False)
                      )
                metadata.create_all()

            if not connection.dialect.has_table(connection, 'Item Info'):
                metadata = MetaData(connection)
                Table('Item Info', metadata,
                      Column('Item', Integer, nullable=False),
                      Column('Item Description',
                             Text, nullable=False),
                      Column('PO(s)', BigInteger, nullable=False),
                      Column('Order Quantity',
                             Integer, nullable=False),
                      Column('Available Quantity',
                             Integer, nullable=False),
                      Column('Vendor Style/PID',
                             Integer, nullable=False),
                      Column('Assortment Item(s)', Text)
                      )
                metadata.create_all()

            if drop_all:
                table_names = ['General Information', 'SIP Elements',
                               'PIF Info', 'POM Info', 'Item Info']
                connection.execute('TRUNCATE {} RESTART IDENTITY;'.format(
                    ','.join('"' + table + '"' for table in table_names)))


class PostgreSQLHolder:
    postgre_engine = PostgreSQLHolderUtils.get_engine(
        PostgreSQLHolderConfig.user, PostgreSQLHolderConfig.password, PostgreSQLHolderConfig.host, PostgreSQLHolderConfig.port, PostgreSQLHolderConfig.db)
