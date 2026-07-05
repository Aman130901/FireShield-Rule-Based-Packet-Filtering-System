import json


class RuleParser:

    def __init__(self, rule_file):
        self.rule_file = rule_file

    def load_rules(self):

        with open(self.rule_file, "r") as file:
            rules = json.load(file)

        return rules