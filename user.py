class User():
    def __init__(self, user_data):
        self.name = user_data["name"]
        self.email = user_data["email"]
        self.id = str(user_data["_id"])
        self.confirmed_email = user_data["confirmed_email"]
        self.role = user_data["role"]
        self.is_anonymous = False

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return self.id
