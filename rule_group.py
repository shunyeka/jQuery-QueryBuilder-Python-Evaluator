from rule import Rule


class RuleGroup:
    def __init__(self, rule_group_dict):
        self.condition = rule_group_dict['condition']
        self.rules = rule_group_dict['rules']

    def evaluate(self, obj):
        if self.condition == 'AND':
            return all(map(lambda x: RuleGroup.get_rule_object(x).evaluate(obj), self.rules))
        else:
            return any(map(lambda x: RuleGroup.get_rule_object(x).evaluate(obj), self.rules))

    @staticmethod
    def get_rule_object(rule):
        if 'rules' in rule:
            return RuleGroup(rule)
        return Rule(rule)
