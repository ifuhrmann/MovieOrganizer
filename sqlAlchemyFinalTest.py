# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 14:11:38 2018

@author: Iddo
"""
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table,MetaData
import os.path
import sys

Base = declarative_base()
db_path = "test.db"
engine = create_engine('sqlite:///' + db_path)
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
metadata = MetaData(engine)

DBSession = sessionmaker(bind=engine)
    # A DBSession() instance establishes all conversations with the database
    # and represents a "staging zone" for all the objects loaded into the
    # database session object. Any change made against the objects in the
    # session won't be persisted into the database until you call
    # session.commit(). If you're not happy about the changes, you can
    # revert all of them back to the last commit by calling
    # session.rollback()
session = DBSession()

    
Base.metadata.create_all(engine)
   
direct = "F:/"

try:
    users = Table(direct, metadata, autoload=True)
except:
    users = Table(direct,metadata,
                  Column('id',Integer, primary_key=True),
                  Column('x',Integer),
                  Column('y',Integer)
                  )
    users.create()



for t in metadata.sorted_tables:
    print ("Table name: ", t.name)


i=users.insert()
i.execute({"x":13,"y":2312})

s = users.select().where(users.c.id >= 5).order_by('x')
rs = s.execute()
row = rs.fetchall()
for r in row:
    print(r['id'],r['x'],r['y'])
print("\n\n")

d = users.delete().where(users.c.id == 5)
rs = d.execute()
print(rs)

print("\n\n")
s=users.select()
rs = s.execute()
row = rs.fetchall()
for r in row:
    print(r[0],r[1],r[2])

session.close()
