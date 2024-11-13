from datetime import datetime

from .models import User
from .database import create_session


def get_user_by_address(address: str):
    session = create_session()
    user = session.query(User).filter(User.address == address).first()
    session.close()

    return user


def get_user_by_username(username: str):
    session = create_session()
    user = session.query(User).filter(User.username == username).first()
    session.close()

    return user


def get_unverified_users():
    session = create_session()
    users = (
        session.query(User)
        .filter(User.verified == False, User.id_number != None)
        .all()
    )
    session.close()

    return users


def add_user(address: str, nonce: str):
    session = create_session()
    user = User(address=address, nonce=nonce)
    session.add(user)
    session.commit()
    session.refresh(user)
    session.close()

    return user


def activate_user(address: str):
    session = create_session()
    user = session.query(User).filter(User.address == address).first()
    user.active = True
    session.commit()
    session.refresh(user)
    session.close()

    return user


def check_username(username: str):
    session = create_session()
    user = session.query(User).filter(User.username == username).first()
    session.close()

    return user


def update_username(address: str, username: str):
    session = create_session()
    user = session.query(User).filter(User.address == address).first()
    user.username = username
    session.commit()
    session.refresh(user)
    session.close()

    return user


def update_kyc_info(
    address: str,
    name: str,
    age: int,
    location: str,
    id_number: str,
    id_front: bytes,
    id_back: bytes,
):
    session = create_session()
    user = session.query(User).filter(User.address == address).first()
    user.name = name
    user.age = age
    user.location = location
    user.id_number = id_number
    user.id_front = id_front
    user.id_back = id_back
    session.commit()
    session.refresh(user)
    session.close()

    return user


def approve_user(address: str):
    session = create_session()
    user = session.query(User).filter(User.address == address).first()
    user.verified = True
    user.verified_at = datetime.now()
    user.kyc_status = 1
    user.id_front = None
    user.id_back = None
    session.commit()
    session.refresh(user)
    session.close()


def reject_user(address: str):
    session = create_session()
    user = session.query(User).filter(User.address == address).first()
    user.kyc_status = -1
    user.name = None
    user.age = None
    user.location = None
    user.id_number = None
    user.id_front = None
    user.id_back = None
    session.commit()
    session.close()


def pending_notification(address: str):
    session = create_session()
    user = session.query(User).filter(User.address == address).first()
    session.close()

    return user.kyc_status != 0


def get_kyc_status(address: str):
    session = create_session()
    user = session.query(User).filter(User.address == address).first()
    session.close()

    return user.kyc_status


def reset_kyc_status(address: str):
    session = create_session()
    user = session.query(User).filter(User.address == address).first()
    user.kyc_status = 0
    session.commit()
    session.refresh(user)
    session.close()


def revoke_kyc(address: str):
    session = create_session()
    user = session.query(User).filter(User.address == address).first()
    user.verified = False
    user.verified_at = None
    user.name = None
    user.age = None
    user.location = None
    user.id_number = None
    user.id_front = None
    user.id_back = None
    session.commit()
    session.refresh(user)
    session.close()


def verify_info(
    address: str,
    name: str = None,
    age: int = None,
    location: str = None,
    id_number: str = None,
):
    session = create_session()

    if name and not age and not location and not id_number:
        user = (
            session.query(User)
            .filter(User.address == address, User.name == name)
            .first()
        )

    elif not name and age and not location and not id_number:
        user = (
            session.query(User)
            .filter(User.address == address, User.age == age)
            .first()
        )

    elif not name and not age and location and not id_number:
        user = (
            session.query(User)
            .filter(User.address == address, User.location == location)
            .first()
        )

    elif not name and not age and not location and id_number:
        user = (
            session.query(User)
            .filter(User.address == address, User.id_number == id_number)
            .first()
        )

    elif name and age and not location and not id_number:
        user = (
            session.query(User)
            .filter(User.address == address, User.name == name, User.age == age)
            .first()
        )

    elif name and not age and location and not id_number:
        user = (
            session.query(User)
            .filter(
                User.address == address, User.name == name, User.location == location
            )
            .first()
        )

    elif name and not age and not location and id_number:
        user = (
            session.query(User)
            .filter(
                User.address == address,
                User.name == name,
                User.id_number == id_number,
            )
            .first()
        )

    elif not name and age and location and not id_number:
        user = (
            session.query(User)
            .filter(
                User.address == address, User.age == age, User.location == location
            )
            .first()
        )

    elif not name and age and not location and id_number:
        user = (
            session.query(User)
            .filter(
                User.address == address, User.age == age, User.id_number == id_number
            )
            .first()
        )

    elif not name and not age and location and id_number:
        user = (
            session.query(User)
            .filter(
                User.address == address,
                User.location == location,
                User.id_number == id_number,
            )
            .first()
        )

    elif name and age and location and not id_number:
        user = (
            session.query(User)
            .filter(
                User.address == address,
                User.name == name,
                User.age == age,
                User.location == location,
            )
            .first()
        )

    elif name and age and not location and id_number:
        user = (
            session.query(User)
            .filter(
                User.address == address,
                User.name == name,
                User.age == age,
                User.id_number == id_number,
            )
            .first()
        )

    elif name and not age and location and id_number:
        user = (
            session.query(User)
            .filter(
                User.address == address,
                User.name == name,
                User.location == location,
                User.id_number == id_number,
            )
            .first()
        )

    elif not name and age and location and id_number:
        user = (
            session.query(User)
            .filter(
                User.address == address,
                User.age == age,
                User.location == location,
                User.id_number == id_number,
            )
            .first()
        )

    else:
        user = (
            session.query(User)
            .filter(
                User.address == address,
                User.name == name,
                User.age == age,
                User.location == location,
                User.id_number == id_number,
            )
            .first()
        )

    session.close()

    return True if user else False


def get_allowed_attributes(address: str):
    session = create_session()
    user = session.query(User).filter(User.address == address).first()
    session.close()

    return (
        user.name_allowed,
        user.age_allowed,
        user.location_allowed,
        user.id_number_allowed,
    )


def set_allowed_attributes(
    address: str,
    name: bool,
    age: bool,
    location: bool,
    id_number: bool,
):
    session = create_session()
    user = session.query(User).filter(User.address == address).first()

    user.name_allowed = name
    user.age_allowed = age
    user.location_allowed = location
    user.id_number_allowed = id_number

    session.commit()
    session.refresh(user)
    session.close()


def check_allowed_attribute(address: str, attribute: str, value: str):
    if not value:
        return True

    session = create_session()
    user = session.query(User).filter(User.address == address).first()
    session.close()

    return getattr(user, f"{attribute}_allowed")
