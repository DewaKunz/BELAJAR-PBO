from model import DatabaseManager
from view import View
from controller import Controller

if __name__ == "__main__":
    view = View()
    db = DatabaseManager()
    controller = Controller(db, view)
    controller.run()
