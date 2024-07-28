from database.operations import DBPost, DBGet


def create_location(lat, lon, country, state, city, road):
    return DBPost.create_location(lat, lon, country, state, city, road)


def get_location(location_id):
    return DBGet.get_location(location_id)
