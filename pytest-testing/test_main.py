from main import get_weather, add, divide
import pytest

class UserManager:
    def __init__(self):
        self.users = {}

    def add_user(self,username,email):
        if username in self.users:
            raise ValueError("User already exists")
        self.users[username] = email
        return True
    
    def get_user(self,username):
        return self.users.get(username)

def test_get_weather():
    assert get_weather(21) == "hot"
    assert get_weather(19) == "cold"
    assert get_weather(20) == "cold"

def test_add():
    assert add(2,3) == 5, "2 + 3 should be 5"
    assert add(-1,1) == 0, "-1 + 1 should be 0"
    assert add(0,0) == 0, "0 + 0 should be 0"
    assert add(-1,-1) == -2, "-1 + -1 should be -2"

def test_divide():
    assert divide(4,2) == 2, "4 / 2 should be 2"
    assert divide(5,2) == 2.5, "5 / 2 should be 2.5"
    # tests if it raises an error when function is executed
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10,0)
