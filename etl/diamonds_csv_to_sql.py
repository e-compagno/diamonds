import pandas as pd 
import sqlalchemy as db
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
import os

# Load dataset
df = pd.read_csv('../data/diamonds.csv',\
                 header=0)

# Load MYSql connector 
SQL_USR, SQL_PSW= os.environ['SQL_USR'], os.environ['SQL_PSW']
mysql_str = 'mysql+mysqlconnector://'+SQL_USR+':'+SQL_PSW+'@localhost:3306/'
engine = db.create_engine(mysql_str)

print('Create database Diamonds')
print('-'*30)
# Create database diamonds
con=engine.connect()
con.execute('commit')
con.execute('CREATE DATABASE if NOT EXISTS Diamonds;')
con.close()
print('Done.\n')

print('Create tables.')
print('-'*30)
# Select diamonds database
engine = db.create_engine(mysql_str+'Diamonds')
con=engine.connect()

Base=declarative_base()

class Physical(Base):
    """
    Class for creating the physical table.
    """
    __tablename__ = 'physical'
    
    id=Column(Integer, primary_key=True)
    carat=Column(Float)
    cut=Column(String(10))
    color=Column(String(10))
    clarity=Column(String(4))
    depth=Column(Float)
    table=Column(Float)
    price=Column(Float)
    x=Column(Float)
    y=Column(Float)
    z=Column(Float)

    def __init__(self, id, carat, cut, color, clarity, depth, table, price, x, y, z):
        self.id=id
        self.carat=carat
        self.cut=cut
        self.color=color
        self.clarity=clarity
        self.depth=depth
        self.table=table
        self.price=price
        self.x=x
        self.y=y
        self.z=z

Base.metadata.create_all(engine)

print('Done.\n')

print('Insert data from CSV to SQL.')
print('-'*30)
# Copy data into database
# Insert data to database
engine = db.create_engine(mysql_str+'Diamonds')
con=engine.connect()

# Rename first column to id
df=df.rename(columns={'Unnamed: 0':'id'})

df.to_sql(name='diamond',\
             con=engine,\
             if_exists='replace')

print('Done.\n')

# Check database size
print('Database describe:')
eng=create_engine(mysql_str+'Diamonds')
con = eng.connect()
res =con.execute('SELECT COUNT(*) FROM physical;').fetchall()
print('database size: {}'.format(res[0][0]))