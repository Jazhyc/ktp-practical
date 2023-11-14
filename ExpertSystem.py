class ExpertSystem:

    def __init__(self, kb):
        """Creates a expert system using the given knowledge base"""
        self.kb = kb
        self.known_facts = []
        self.output = None
    
    def get_known_facts(self):
        """Returns the known facts"""
        return self.known_facts
    
    def add_fact(self, fact):
        """Adds a fact to the known facts"""
        self.known_facts.append(fact)

    def get_output_detail(self):
        """Returns the output detail"""
        return self.kb['outputs'][self.output]
    
    def resolve(self):
        """
        Resolves the known facts to find the conclusion
        Returns True if an output is found, False otherwise
        """

        # Iterate over all rules
        for key in self.kb['rules']:

            rule = self.kb['rules'][key]

            # Check if all the conditions are met
            if all(fact in self.known_facts for fact in rule['if']):
                
                # Check if the then statement is a fact or output
                if list(rule['then'].keys())[0] == 'fact':
                    self.add_fact(rule['then']['fact'])

                    # Remove the rule, only changes internal state and not json
                    del self.kb['rules'][key]

                    # Recursively resolve
                    return self.resolve()

                else:
                    self.output = rule['then']['output']
                    return True
        
        return False
    
    def run(self):
        """Runs the expert system"""
        
        while (True):

            if self.resolve():
                print('Output: ' + self.get_output_detail())
                break
    
    def ask_question(self):
        """
        Prompt the user interface to ask a question
        Adds the appropriate fact to the known facts from the answer
        """

        # Implement once we have a UI
        pass