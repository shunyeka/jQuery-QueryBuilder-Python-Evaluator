import json
from jqqb_evaluator.rule_group import RuleGroup


class Evaluator:

    def __init__(self, rule_set):
        if isinstance(rule_set, str):
            self.parsed_rule_set = json.loads(rule_set)
        else:
            self.parsed_rule_set = rule_set

    def get_matching_objects(self, objects):
        return list(filter(lambda x: self.object_matches_rules(x), objects))

    def object_matches_rules(self, obj):
        return RuleGroup(self.parsed_rule_set).evaluate(obj)
