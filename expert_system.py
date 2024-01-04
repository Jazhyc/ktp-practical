from helper import load_json


class ExpertSystem:

    def __init__(self):
        """
        Creates a expert system using the given knowledge base
        Contains a reference to the controller for communication
        """

        # The knowledge base and facts that are deemed to be true
        self.kb = load_json('kb.json')
        self.known_facts = []

        # The output of the expert system and the reference to the controller
        self.output = None

        # The observer that is notified when the output is found
        self.observer = None

    def set_observer(self, observer):
        """Sets the observer for the expert system"""
        self.observer = observer

    def get_known_facts(self):
        """Returns the known facts"""
        return self.known_facts

    def add_fact(self, fact):
        """Adds a fact to the known facts"""
        print(f"Added fact: {fact}")

        # if fact is enclosed in square brackets, consider it a list of facts and add them all
        if fact.startswith('[') and fact.endswith(']'):
            for f in fact[1:-1].split(','):

                # remove ' and " from the fact
                f = f.replace("'", '').replace('"', '')
                self.known_facts.append(f.strip())

        else:
            self.known_facts.append(fact)

    def get_output_detail(self):
        """Returns the output detail"""
        return self.kb['outputs'][self.output]

    def reset(self):
        """Resets the expert system"""
        self.known_facts = []
        self.kb = load_json('kb.json')
        self.output = None

    def resolve(self):
        """
        Resolves the known facts to find the conclusion
        Returns True if an output is found, False otherwise
        """

        # Iterate over all rules
        for key in list(self.kb['rules'].keys()):

            rule = self.kb['rules'][key]

            # Check if all the conditions are met
            if all(fact in self.known_facts for fact in rule['if']):

                # Check if the then statement is a fact or output
                if list(rule['then'].keys())[0] == 'fact':
                    self.add_fact(rule['then']['fact'])

                    # Remove the rule, only changes internal state and not json
                    self.kb['rules'].pop(key)

                    # Recursively resolve
                    return self.resolve()

                else:
                    self.output = rule['then']['output']
                    return True

        return False

    def get_question(self):
        """
        Gets a valid question from the knowledge base
        Returns None if no question can be asked

        The question consists of a question and a list of answers
        """

        # Check all questions and see if any can be asked
        for key in list(self.kb['questions'].keys()):

            question = self.kb['questions'][key]

            # Check if all the conditions are met
            if all(fact in self.known_facts for fact in question['if']):

                # Pop the question from the knowledge base
                self.kb['questions'].pop(key)

                self.observer.set_question(question)

                # Break the loop incase multiple questions can be asked
                break
