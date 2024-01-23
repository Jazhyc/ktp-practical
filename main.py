from expert_system import ExpertSystem
from frontend import Frontend
from controller import Controller


def main():

    # Ensure decoupling of the frontend and expert system
    frontend = Frontend()
    expert = ExpertSystem()
    controller = Controller(expert, frontend)

    # Create a thread for the controller
    controller.run()
    frontend.run()


if __name__ == '__main__':
    main()
