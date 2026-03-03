from sqlalchemy import insert, select, update, delete, ColumnElement, UnaryExpression
from sqlalchemy import Table

from db import engine, Session, Base
from models import Movie, Directory

# create tables once at startup
Base.metadata.create_all(engine)



def get_movies(filter_expr:ColumnElement[bool]=True, order_by_columns:list[UnaryExpression]=None):
    with Session() as session:
        stmt = select(Movie).where(filter_expr)
        if order_by_columns:
            stmt = stmt.order_by(*order_by_columns)
        return session.execute(stmt).scalars().all()

def delete_movies():
    with Session() as session:
        session.execute(delete(Movie))
        session.commit()


def insert_movie(m:Movie):
    with Session() as session:
        session.add(m)
        session.commit()

def update_movie(m:Movie):
    with Session() as session:
        mov = session.execute(select(Movie).where(Movie.id == m.id)).scalar_one()
        mov.hasSeen,mov.personalRating,mov.imdbRating = m.hasSeen,m.personalRating,m.imdbRating
        session.commit()



def get_directories():
    with Session() as session:
        return session.execute(select(Directory)).scalars().all()


def insert_directory(d:Directory):
    with Session() as session:
        session.add(d)
        session.commit()
