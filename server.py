from app import app
from app.controllers import users_controller, recipes_controller


if __name__ == '__main__':
    app.run(debug=True)