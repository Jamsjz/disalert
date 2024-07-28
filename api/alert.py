from database.operations import DBGet, DBPost, DBUpdate, DBDelete


def create_alert(title, description, location_id, user_id, alert_type):
    return DBPost.create_alert(title, description, location_id, user_id, alert_type)


def get_alert(alert_id):
    return DBGet.get_alert(alert_id)


def get_alerts_by_user(user):
    return DBGet.get_alerts_by_user(user)


def update_alert(
    alert_id,
    title=None,
    description=None,
    location_id=None,
    user_id=None,
    alert_type=None,
):
    alert = get_alert(alert_id)
    if not alert:
        return None

    if title:
        alert.title = title
    if description:
        alert.description = description
    if location_id:
        alert.location_id = location_id
    if user_id:
        alert.user_id = user_id
    if alert_type:
        alert.alert_type = alert_type

    DBUpdate.update_alert(alert_id, alert)
    return alert


def delete_alert(alert_id):
    return DBDelete.delete_alert(alert_id)
