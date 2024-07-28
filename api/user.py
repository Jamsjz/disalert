from database.operations import DBGet, DBPost, DBUpdate, DBDelete


def create_user(username, password, email):
    return DBPost.create_user(username, password, email)


def get_user(username):
    return DBGet.get_user(username)


def get_user_password(username):
    return DBGet.get_user_password(username)


def update_user_password(user_id, new_password):
    return DBUpdate.update_password(user_id, new_password)


def delete_user(user_id):
    return DBDelete.delete_user(user_id)


def verify_password(username, password):
    return DBGet.verify_password(username, password)
