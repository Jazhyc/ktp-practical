from helper import *
from ExpertSystem import ExpertSystem

def main():
    kb = load_json('kb.json')
    expert = ExpertSystem(kb)
    expert.add_fact('fact1')
    expert.add_fact('fact2')
    expert.run()

if __name__ == '__main__':
    main()