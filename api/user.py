from database.operations import DBGet, DBPost, DBUpdate, DBDelete


def create_user(username, password, email):
    return DBPost.create_user(username, password, email)


def get_user(username):
    return DBGet.get_user(username)


def get_users():
    return DBGet.get_users()


def get_usernames():
    users = get_users()
    usernames = []
    for user in users:
        usernames.append(user.username)


def check_username(username):
    usernames = get_usernames()
    if username is not None and usernames is not None:
        return username in usernames
    if not usernames:
        return True
    else:
        return False


def get_user_password(username):
    return DBGet.get_user_password(username)


def update_user_password(user_id, new_password):
    return DBUpdate.update_password(user_id, new_password)


def delete_user(user_id):
    return DBDelete.delete_user(user_id)


def verify_user(username, password):
    return DBGet.verify_user(username, password)
