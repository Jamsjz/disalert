from .models import Session, Alert, User, Location, AlertTime
from bcrypt import hashpw, checkpw, gensalt
import base64


class DBGet:
    @staticmethod
    def get_user(username: str):
        session = Session()
        user = session.query(User).filter_by(username=username).first()
        return user

    @staticmethod
    def get_alert(id: int):
        session = Session()
        alert = session.query(Alert).filter_by(id=id).first()
        return alert

    @staticmethod
    def get_location(id: int):
        session = Session()
        location = session.query(Location).filter_by(id=id).first()
        return location

    @staticmethod
    def get_alerts(user):
        session = Session()
        alerts = session.query(Alert).filter_by(user_id=user.id).all()
        return alerts

    @staticmethod
    def get_alerts_by_location(location):
        session = Session()
        alerts = session.query(Alert).filter_by(location_id=location.id).all()
        return alerts

    @staticmethod
    def get_alerts_by_time(date, time):
        session = Session()
        alerts = (
            session.query(Alert)
            .filter(Alert.creation_time.any(date=date, time=time))
            .all()
        )
        return alerts

    @staticmethod
    def get_alerts_by_type(type):
        session = Session()
        alerts = session.query(Alert).filter_by(alert_type=type).all()
        return alerts

    @staticmethod
    def get_alerts_by_user(user):
        session = Session()
        alerts = session.query(Alert).filter_by(user_id=user.id).all()
        return alerts

    @staticmethod
    def get_alerts_by_user_and_location(user, location):
        session = Session()
        alerts = (
            session.query(Alert)
            .filter_by(user_id=user.id, location_id=location.id)
            .all()
        )
        return alerts

    @staticmethod
    def get_alerts_by_user_and_time(user, date, time):
        session = Session()
        alerts = (
            session.query(Alert)
            .filter(
                Alert.user_id == user.id, Alert.creation_time.any(date=date, time=time)
            )
            .all()
        )
        return alerts

    @staticmethod
    def get_alerts_by_user_and_type(user, type):
        session = Session()
        alerts = session.query(Alert).filter_by(user_id=user.id, alert_type=type).all()
        return alerts

    @staticmethod
    def verify_password(username: str, password: str) -> bool:
        try:
            stored_password = DBGet.get_user_password(username)
            if stored_password is None:
                return False
            else:
                stored_password_bytes = base64.b64decode(
                    stored_password.encode("utf-8")
                )
                return checkpw(password.encode("utf-8"), stored_password_bytes)
        except Exception as e:
            print(e)
            exit(1)

    @staticmethod
    def get_user_password(username: str):
        try:
            session = Session()
            user = session.query(User).filter_by(username=username).first()
            if user is not None:
                return user.password
        except Exception as e:
            print(e)
            exit(1)


class DBPost:
    @staticmethod
    def create_user(username: str, password: str, email: str):
        # Hash the password before storing it
        hashed = hashpw(password.encode("utf-8"), gensalt())
        hashed_str = base64.b64encode(hashed).decode("utf-8")

        session = Session()
        user = User(username=username, password=hashed_str, email=email)
        session.add(user)
        session.commit()
        return user

    @staticmethod
    def create_alert(
        title: str, description: str, location_id: int, user_id: int, alert_type: str
    ):
        session = Session()
        alert = Alert(
            title=title,
            description=description,
            location_id=location_id,
            user_id=user_id,
            alert_type=alert_type,
        )
        session.add(alert)
        session.commit()
        return alert

    @staticmethod
    def create_location(
        lat: float, lon: float, country: str, state: str, city: str, road: str
    ):
        session = Session()
        location = Location(
            lat=lat,
            lon=lon,
            country=country,
            state=state,
            city=city,
            road=road,
        )
        session.add(location)
        session.commit()
        return location

    @staticmethod
    def create_alert_time(date: str, time: str, alert_id: int):
        session = Session()
        alert_time = AlertTime(
            date=date,
            time=time,
            alert_id=alert_id,
        )
        session.add(alert_time)
        session.commit()
        return alert_time


class DBDelete:
    @staticmethod
    def delete_alert(id: int):
        session = Session()
        alert = session.query(Alert).filter_by(id=id).first()
        session.delete(alert)
        session.commit()
        return alert

    @staticmethod
    def delete_user(id: int):
        session = Session()
        user = session.query(User).filter_by(id=id).first()
        session.delete(user)
        session.commit()
        return user

    @staticmethod
    def delete_alert_by_userid(user_id: int):
        session = Session()
        alerts = session.query(Alert).filter_by(user_id=user_id).all()
        for alert in alerts:
            session.delete(alert)
        session.commit()


class DBUpdate:
    @staticmethod
    def update_username(id: int, username: str) -> bool:
        try:
            session = Session()
            user = session.query(User).filter_by(id=id).first()
            if user is not None:
                user.username = username
                session.commit()
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def update_password(id: int, password: str):
        # Hash the password and encode it to store as a string
        hashed = hashpw(password.encode("utf-8"), gensalt())
        hashed_str = base64.b64encode(hashed).decode("utf-8")

        try:
            session = Session()
            user = session.query(User).filter_by(id=id).first()
            if user is not None:
                if isinstance(user.password, str):
                    user.password = hashed_str
                session.commit()
            return user
        except Exception as e:
            print(e)
        finally:
            return user

    @staticmethod
    def update_alert(id, alert):
        try:
            session = Session()
            existing_alert = session.query(Alert).filter_by(id=id).first()
            if existing_alert:
                for attr, value in alert.__dict__.items():
                    setattr(existing_alert, attr, value)
                session.commit()
            return existing_alert
        except Exception as e:
            print(e)
            return None
