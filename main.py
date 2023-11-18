from helper import *
from expert_system import ExpertSystem
from frontend import Frontend
from controller import Controller

def main():
    kb = load_json('kb.json')

    # Ensure decoupling of the frontend and expert system
    frontend = Frontend()
    expert = ExpertSystem(kb)
    controller = Controller(expert, frontend)

    controller.run()

if __name__ == '__main__':
    main()