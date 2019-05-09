from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, CategoryItem, User

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Create dummy user
user1 = User(name="Jay Pretet", email="jay@example.com", picture="https://sample.com/hello.png")
session.add(user1)
session.commit()

category1 = Category(user_id=1, name="Swimming", description="Swimming is an individual or team sport that requires the use of one's entire body to move through water.")
session.add(category1)
session.commit()