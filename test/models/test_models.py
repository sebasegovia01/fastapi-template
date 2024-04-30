# test/test_models.py
from app.models.users import User

# user model
def test_user_model():
    user = User(id=1, userId="123456789", userPhoneNumber="+5691234567")
    assert user.id == 1
    assert user.userId == "123456789"
    assert user.userPhoneNumber == "+5691234567"
