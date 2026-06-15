import pytest

from dao_users import create_user, get_user, get_list_of_users
from models import CartItem, User



def test_not_user():
    with pytest.raises(ValueError, match="L'utilisateur n'est pas valide."):
        create_user(CartItem(id=1, cart_id=1, product_id=1, quantity=2))


@pytest.mark.parametrize(
    "x, y",
    [
        ("", "2"),
        ("r", ""),
    ],
)
def test_identifiant_not_provided(x, y):
    with pytest.raises(
        ValueError, match="L'identifiant et le mot de passe doivent être renseigné."
    ):
        create_user(User(id=x, password=y, client=True, administrator=False))


@pytest.mark.parametrize(
    "client, administrator",
    [
        (False, False),
        (True, True),
    ],
)
def test_client_or_administrator(client, administrator):
    with pytest.raises(
        ValueError, match="Soit l'utilisateur est client, soit il est administrateur."
    ):
        create_user(
            User(
                id="admin",
                password="password",
                firstName="firstName",
                lastName="lastName",
                client=client,
                administrator=administrator,
            )
        )


def test_user_is_created(db_session):
    user = User(
        id="test@mail.fr",
        password="secret",
        firstName="firstName",
        lastName="lastName",
        client=True,
        administrator=False,
    )
    create_user(user)

    found = db_session.session.query(User).filter_by(id="test@mail.fr").one()
    assert found.id == "test@mail.fr"
    assert found.password == "secret"
    assert found.firstName == "firstName"
    assert found.lastName == "lastName"
    assert found.client is True
    assert found.administrator is False


def test_user_already_exists(db_session):
    user = User(
        id="dup@mail.fr",
        password="secret",
        firstName="firstName",
        lastName="lastName",
        client=True,
        administrator=False,
    )
    create_user(user)

    response, status_code  = create_user(
        User(
            id="dup@mail.fr",
            password="other",
            firstName="firstName",
            lastName="lastName",
            client=True,
            administrator=False,
            )
        )
    assert status_code == 401
    assert response.get_json() == {
        "error": "L'utilisateur existe déjà en base de donnée."
    }

def test_get_user(db_session):
    user = User(
        id="get@mail.fr",
        password="secret",
        firstName="firstName",
        lastName="lastName",
        client=False,
        administrator=True,
    )
    create_user(user)

    found = get_user("get@mail.fr")
    assert found.id == "get@mail.fr"
    assert found.administrator is True


def test_get_user_not_found(db_session):
    with pytest.raises(ValueError, match="L'utilisateur n'est pas enregistré en base."):
        get_user("inconnu@mail.fr")

def test_get_all_user(db_session):
    user = User(
        id="get@mail.fr",
        password="secret",
        firstName="firstName",
        lastName="lastName",
        client=False,
        administrator=True,
    )
    user1 = User(
        id="get1@mail.fr",
        password="secret1",
        firstName="firstName1",
        lastName="lastName1",
        client=True,
        administrator=False,
    )
    create_user(user)
    create_user(user1)

    founds = get_list_of_users()
    assert len(founds) == 2
    founds = [op for op in founds]
    assert founds[0].id == "get@mail.fr"
    assert founds[0].password == "secret"
    assert founds[0].firstName == "firstName"
    assert founds[0].lastName == "lastName"
    assert founds[0].client == False
    assert founds[0].administrator == True

    assert founds[1].id == "get1@mail.fr"
    assert founds[1].password == "secret1"
    assert founds[1].firstName == "firstName1"
    assert founds[1].lastName == "lastName1"
    assert founds[1].client == True
    assert founds[1].administrator == False


