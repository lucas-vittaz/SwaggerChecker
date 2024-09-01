import pytest
from src.gui.user_interface import UserInterface

@pytest.fixture
def app():
    app = UserInterface()
    yield app
    app.destroy()

def test_interface_launch(app):
    assert isinstance(app, UserInterface), "L'interface ne s'est pas lancée correctement."
