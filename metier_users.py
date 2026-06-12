from sqlalchemy.orm.exc import NoResultFound
from models import db, User

def authenticate(id, password):
    try:
        print("id")
        print(id)
        print("password")
        print(password)
        user = db.session.query(User).filter_by(id=id, password=password).one()
        return True
    except NoResultFound:
        # Cet utilisateur n'existe pas en base.
        return False