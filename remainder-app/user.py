#Needed by flask_login for session maintenance
users = { 
    "shankar" : { "name": "shankar", "email": "s@h.com", "pass":"none" } ,
    "krithika" : { "name": "krithika", "email": "k@h.com", "pass":"none" } ,
    }
class User():
    def __init__(self,n):
        self.name = n
        self.password = users[n]
        self.email = users[n]

    def to_json(self):
        return {"name": self.name,
                "email": self.email}
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.name)

