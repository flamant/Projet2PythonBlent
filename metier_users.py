from models import User
from sqlalchemy.orm.exc import NoResultFound
from models import SQLAlchemy
from app import app

db = SQLAlchemy(app)

def authenticate(id, salt, hashed):  
    try: 
        db.session.query(User).filter_by(id=id, salt=salt, hashed=hashed).one()    
        return True 
    except NoResultFound: 
        print("Cet utilisateur n'existe pas en base.") 
        return False