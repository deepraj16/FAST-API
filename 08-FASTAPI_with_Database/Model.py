from  .database import Base 
from sqlalchemy import Column,Integer,Boolean,String 
from sqlalchemy.sql.expression import Null 


class Post(Base): 
    __tablename__ ="post"

    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,default=True)


