def get_username(obj):
    username = obj.user.username.replace("_", " ")
    return username
