import pytest

from dao_users import create_user, get_user
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
                client=client,
                administrator=administrator,
            )
        )


def test_user_is_created(db_session):
    user = User(
        id="test@mail.fr",
        password="secret",
        client=True,
        administrator=False,
    )
    create_user(user)

    found = db_session.session.query(User).filter_by(id="test@mail.fr").one()
    assert found.id == "test@mail.fr"
    assert found.client is True
    assert found.administrator is False


def test_user_already_exists(db_session):
    user = User(
        id="dup@mail.fr",
        password="secret",
        client=True,
        administrator=False,
    )
    create_user(user)

    with pytest.raises(ValueError, match="L'utilisateur existe déjà en base de donnée."):
        create_user(
            User(
                id="dup@mail.fr",
                password="other",
                client=True,
                administrator=False,
            )
        )


def test_get_user(db_session):
    user = User(
        id="get@mail.fr",
        password="secret",
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
