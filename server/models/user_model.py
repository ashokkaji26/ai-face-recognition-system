from datetime import datetime

def create_user(name: str, email: str):
    return {
        "name": name,
        "email": email.lower(),
        "created_at": datetime.utcnow()
    }