from sqlalchemy import create_engine, MetaData, Table, select, and_, or_, Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Text, Date, Time, Time, DateTime, func, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.sql.elements import False_

engine = create_engine('mysql+pymysql://admin:Aisconsola#2021@ais.czudyx9luuct.us-east-1.rds.amazonaws.com/aiscloudfrontend')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()