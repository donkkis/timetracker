from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

# Define the database models
Base = declarative_base()

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    time_entries = relationship("TimeEntry", back_populates="project")

class TimeEntry(Base):
    __tablename__ = 'time_entries'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    project = relationship("Project", back_populates="time_entries")

def get_session(conn_str: str = 'sqlite:///time_tracker.db'):
    engine = create_engine(conn_str)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
