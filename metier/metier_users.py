

def authenticate(id, password):  
    try: 
        db.session.query(User).filter_by(id=id, password=password).one()    
        return True 
    except NoResultFound: 
        print("Cet utilisateur n'existe pas en base.") 
        return False