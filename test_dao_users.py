import pytest

from dao_users import create_user


""" ef create_user(user):
    if user.__class__.__name__ == 'User':
        if len(user.id) > 0 and len(user.password) > 0:
            if (user.client and not user.administrator) or (user.administrator and not user.client):
                try:
                    db.session.query(User).filter_by(id=user.id).one()
                    raise ValueError("L'utilisateur existe déjà en base de donnée.")
                except NoResultFound as e:
                    # Ajouter à la session
                    db.session.add(user)
                    db.session.commit()
            else:
                raise ValueError("Soit l'utilisateur est client, soit il est administrateur.")
        else:
            raise ValueError("L'identifiant et le mot de passe doivent être renseigné.")
    else:
        raise ValueError("L'utilisateur n'est pas valide.") """

def test_not_user():
    with pytest.raises(ValueError("L'utilisateur n'est pas valide.")):
        create_user(CartItem(id=1,cart_id=1,product_id=1,quantity=2))


@pytest.mark.parametrize(
    ["x", "y", "expectation"],
    [
        ("",  "2", pytest.raises(ValueError)),
        ("r", "", pytest.raises(ValueError("L'identifiant et le mot de passe doivent être renseigné.")))
        
    ],
)
def test_identifiant_not_provided(x, y, expectation):
    with expectation:
        create_user(User(id=x,password=y,client=True,administrator=False))

@pytest.mark.parametrize(
    ["x", "y", "expectation"],
    [
        (False,  False, raises(ValueError("Soit l'utilisateur est client, soit il est administrateur."))),
        (True, True, raises(ValueError("Soit l'utilisateur est client, soit il est administrateur.")))
        
    ],
)
def test_client_or_administrator(x, y, expectation):
    with expectation:
        create_user(User(id="admin",password="password",client=x,administrator=y))


def create_user_works():
        create_user(User(id="new1",password="password1",client=True,administrator=False))



@pytest.mark.parametrize(
    ["x", "y", "expectation"],
    [
        (True,  False, raises(ValueError("L'utilisateur existe déjà en base de donnée."))),
        
    ],
)
def test_user_already_exists_in_data_base(x, y, expectation):
    with expectation:
        user = User("admin", "password", True, False)
        db.session.merge(user)
        db.session.commit()
        create_user(User(id="admin",password="password",client=x,administrator=y))
