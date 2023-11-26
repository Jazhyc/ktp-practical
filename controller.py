import time

class Controller:

    def __init__(self, model, view):
        """
        Creates a controller object which contains a reference to the expert system
        Needs to be added via add model
        """
        self.model = model
        self.view = view

        model.set_observer(view)
        view.set_controller(self)

    def run(self):
        """Runs the system"""

        self.model.get_question()

    
    def update_model(self, response):
        
        self.model.add_fact(response)

        if self.model.resolve():
            self.view.display_answer(self.model.get_output_detail())
        else:
            self.model.get_question()
    
    def reset(self):
        self.model.reset()
        self.run()
            


