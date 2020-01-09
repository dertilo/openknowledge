from sqlalchemy import Table, Column, Integer, ForeignKey, String, Date, DateTime, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


# ip = 'localhost'
from sqlalchemy_util.sqlalchemy_methods import get_sqlalchemy_base_engine

# host = '172.17.0.1' # host from inside of docker-container
# ip = 'gunther'
# sqlalchemy_base,sqlalchemy_engine = get_sqlalchemy_base_engine(host=host)

sqlalchemy_engine = None
sqlalchemy_base = declarative_base()
Base = sqlalchemy_base


def init_sqlalchemy(dbname='sqlite:///sqlalchemy.db'):
    global sqlalchemy_engine
    if sqlalchemy_engine is None:
        sqlalchemy_engine = create_engine(dbname, echo=False)
        # Base.metadata.drop_all(sqlalchemy_engine)
    Base.metadata.bind = sqlalchemy_engine
    Base.metadata.create_all(sqlalchemy_engine)

class Affiliation(Base):
    __tablename__ = 'affiliations'
    id = Column(String, primary_key=True)
    rank = Column(Integer)
    normalized_name = Column(String)
    display_name = Column(String)
    grid_id = Column(String)
    official_page = Column(String)
    wiki_page = Column(String)
    paper_count = Column(Integer)
    citation_count = Column(Integer)
    # latitude = Column(Float)# not existent!
    # longitude = Column(Float)# not existent!
    create_date = Column(String)

    authors = relationship("Author",back_populates="affiliations")

class Author(Base):
    __tablename__ = 'authors'
    id = Column(String, primary_key=True)
    rank = Column(Integer)
    normalized_name = Column(String)
    display_name = Column(String)
    last_known_affiliation = Column(String, ForeignKey(Affiliation.id),nullable=True)
    paper_count = Column(Integer)
    citation_count = Column(Integer)
    create_date = Column(String)

    affiliation = relationship("Affiliation",back_populates="authors")

class Papers(Base):
    __tablename__ = 'papers'
    id = Column(String, primary_key=True)
    rank = Column(String)
    doi = Column(String)
    doc_type = Column(String)
    paper_title = Column(String)
    original_title = Column(String)
    book_title = Column(String)
    year = Column(String)
    date = Column(String)
    publisher = Column(String)
    journal_id = Column(String)
    conference_series_id = Column(String)
    conference_instance_id = Column(String)
    volume = Column(String)
    issue = Column(String)
    first_page = Column(String)
    last_page = Column(String)
    reference_count = Column(String)
    citation_count = Column(String)
    estimated_citation = Column(String)
    original_venue = Column(String)
    # family_id = Column(String)# not existent?
    create_date = Column(String)

    # affiliation = relationship("Affiliation",back_populates="authors")

init_sqlalchemy(dbname='sqlite:///mag_sqlite.db')