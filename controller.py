import time

class Controller:

    def __init__(self, model, view):
        """
        Creates a controller object which contains a reference to the expert system
        Needs to be added via add model
        """
        self.model = model
        self.view = view

    def run(self):
        """Runs the system"""
        
        while (True):

            question_answer_pair = self.model.get_question()
            
            self.view.display_question(question_answer_pair)

            response = self.get_response()

            self.model.add_fact(response)

            if self.model.resolve():
                self.view.display_answer(self.model.get_output_detail())
                break
    
    def update_model(self, response):
        print("Main thread got response")
        self.model.add_fact(response)

        if self.model.resolve():
            self.view.display_answer(self.model.get_output_detail())

    def get_response(self):
        """Returns the response from the user"""
        
        while (True):

            response = self.view.get_input()

            if response:
                return response
            
            time.sleep(0.1)
            


