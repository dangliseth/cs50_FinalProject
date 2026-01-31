from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("mysql+mysqlconnector://root:root@localhost/cs50")

# create multithreaded session
db = scoped_session(sessionmaker(autoflush=False,
                                         bind=engine))

# db base for models
Base = declarative_base()
Base.query = db.query_property()

def init_db():
    import app.models  # Import the models so Base knows about them
    Base.metadata.create_all(bind=engine)