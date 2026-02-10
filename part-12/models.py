from  database import Base 
from sqlalchemy import Column,Integer,Boolean,String,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text 
from sqlalchemy.sql.sqltypes import TIMESTAMP


class Post(Base): 
    __tablename__ ="post_data"

    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default="True",nullable=True)  # for defalt we had the server defalt
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text("now()"))
    user_id = Column(Integer,ForeignKey
                     ("users.id",ondelete="CASCADE"),
                     nullable=False )
    
    owner = relationship("Users", back_populates="posts")

class Users(Base): 
    __tablename__="users"
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    username=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text("now()"))

    posts = relationship("Post", back_populates="owner", cascade="all, delete")

