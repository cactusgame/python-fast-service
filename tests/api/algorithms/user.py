from ab.core import algorithm
from ab.services import user

@api('user')
def current_user():
    return user.get_current_user(required=False)
