from models import User
from sqlalchemy.orm.exc import NoResultFound
from flask import jsonify
from extension import db

def create_user(user):
    if user.__class__.__name__ == 'User':
        if len(user.id) > 0 and len(user.password) > 0:
            if (user.client and not user.administrator) or (user.administrator and not user.client):
                try:
                    db.session.query(User).filter_by(id=user.id).one()
                    return jsonify({"error" : "L'utilisateur existe déjà en base de donnée."}), 401
                except NoResultFound as e:
                    # Ajouter à la session
                    db.session.add(user)
                    db.session.commit()
            else:
                raise ValueError("Soit l'utilisateur est client, soit il est administrateur.")
        else:
            raise ValueError("L'identifiant et le mot de passe doivent être renseigné.")
    else:
        raise ValueError("L'utilisateur n'est pas valide.")



def get_user(id):
    try:
        user = db.session.query(User).filter_by(id=id).one()
    except NoResultFound:
        raise ValueError("L'utilisateur n'est pas enregistré en base.")
    return user


def get_list_of_users():
    # Récupérer tous les utilisateur
    all_users = db.session.query(User).all()
    return all_users