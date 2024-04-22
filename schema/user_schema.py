def user_data(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "hashed_password": user["hashed_password"],
        "email": user["email"]
    }

def list_users(users) -> list:
    return [user_data(user) for user in users]

