#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User

engine = create_engine('sqlite:///movie_catalog.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


def create_category(category_list):
    print("Creating movie cateogry")
    for category_name in category_list:
        category = Category(name=category_name)
        session.add(category)
        session.commit()

def create_sampe_user(name, email, pictureURL):
    print("Creating sample user: ", name)
    user = User(name=name, email=email, picture=pictureURL)
    session.add(user)
    session.commit()

def insert_movie_items(category_name, items):
    category = session.query(Category).filter_by(name=category_name.upper()).one()
    print("inserting " + category.name + " movie items")
    for (name, desc) in items:
        movie_item = CategoryItem(name=name, description=desc, category_id=category.id, user_id=1)
        session.add(movie_item)
        session.commit()


# CATEGORIES
movie_cateogry_list = ["COMEDY", "SCI-FI", "HORROR", "ROMANCE", "ACTION", "THRILLER", "DRAMA", "MYSTERY", "CRIME", "ANIMATION", "ADVENTURE", "FANTASY", "COMEDY-ROMANCE"]



# COMEDY
comedy_items = [
    ("Spider-Man: Far from Home", "Following the events of Avengers: Endgame, Spider-Man must step up to take on new threats in a world that has changed forever."),
    ("Pokémon Detective Pikachu", "In a world where people collect Pokémon to do battle, a boy comes across an intelligent talking Pikachu who seeks to be a detective."),
    ("Aladdin", "A kindhearted street urchin and a power-hungry Grand Vizier vie for a magic lamp that has the power to make their deepest wishes come true."),
    ("Thor: Ragnarok", "Thor is imprisoned on the planet Sakaar, and must race against time to return to Asgard and stop Ragnarök, the destruction of his world, at the hands of the powerful and ruthless villain Hela.")
]


# SCI-FI
scifi_items = [
    ("Avengers: Endgame", "After the devastating events of Avengers: Infinity War (2018), the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to undo Thanos' actions and restore order to the universe."),
    ("Sonic the Hedgehog", "A cop in the rural town of Green Hills will help Sonic escape from the government who is looking to capture him."),
    ("Avengers: Infinity War", "The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful Thanos before his blitz of devastation and ruin puts an end to the universe."),
    ("Captain Marvel", "Carol Danvers becomes one of the universe's most powerful heroes when Earth is caught in the middle of a galactic war between two alien races.")
]


# HORROR
horror_items = [
    ("Chambers", "A woman survives a heart transplant and begins to develop different personality traits."),
    ("The Act", "An anthology series that tells startling, stranger-than-fiction true crime stories, including a girl trying to escape her overprotective and abusive mother.")
]


if __name__ == '__main__':
    create_category(movie_cateogry_list)
    categories = session.query(Category).all()
    for x in categories:
        print(x.name)
    create_sampe_user("Jay Pritchett", "jay_pritchett@example.com", "https://sample.com/hello.png")
    insert_movie_items("COMEDY", comedy_items)
    insert_movie_items("SCI-FI", scifi_items)
    insert_movie_items("HORROR", horror_items)
