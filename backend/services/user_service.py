from authentication.models import User

def create_user(email, password):
    user = User(
        email=email
    )
    user.set_password(password)
    user.save()
    return user