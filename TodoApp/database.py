from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote_plus

## sqlite
# SQLALCHAMY_DATABASE_URL = "sqlite:///./todosapp.db"
# engine = create_engine(SQLALCHAMY_DATABASE_URL, connect_args={"check_same_thread": False})

## postgresql
db_pass = quote_plus("Zubu@123456789")
SQLALCHAMY_DATABASE_URL = f"postgresql://todosapp_sbme_user:SqkGj0mUb8dC8GpwH6MB0kxtVp6FEzke@dpg-d608jv7pm1nc73bcarig-a/todosapp_sbme"
engine = create_engine(SQLALCHAMY_DATABASE_URL)

## mysql
# SQLALCHAMY_DATABASE_URL = f"mysql+pymysql://root:{db_pass}@localhost:3306/TodoApplicationDatabase"
# engine = create_engine(SQLALCHAMY_DATABASE_URL)
SesssionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()