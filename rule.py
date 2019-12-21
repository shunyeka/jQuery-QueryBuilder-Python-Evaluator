from datetime import datetime

from pytimeparse.timeparse import timeparse

from operators.operators import Operators


class Rule:

    def __init__(self, rule_dict):
        self.id = rule_dict['id']
        self.field = rule_dict['field']
        self.type = rule_dict['type']
        self.input = rule_dict['input']
        self.operator = rule_dict['operator']
        self.value = rule_dict['value']

    def evaluate(self, obj):
        return self.get_operator()(self.get_input(obj), self.get_value())

    def get_operator(self):
        return getattr(Operators, 'eval_' + self.operator)

    def get_input(self, obj):
        fields = self.field.split(".")
        result = obj
        steps = len(fields)
        for i in range(steps):
            last_step = i == steps - 1
            second_last_step = i == steps - 2
            result = result.get(fields[i])
            if second_last_step and isinstance(result, list) and isinstance(result[0], dict):
                result = [x[fields[steps - 1]] for x in result]
                break
            result = result[0] if (result is not None and isinstance(result, list) and not last_step) else result
            if result is None:
                break
        if isinstance(result, list):
            return list(map(lambda x: self.typecast_value(x), result))
        else:
            return self.typecast_value(result)

    def get_value(self):
        if isinstance(self.value, list):
            return list(map(lambda x: self.typecast_value(x), self.value))
        return self.typecast_value(self.value)

    def typecast_value(self, value_to_cast):
        if value_to_cast is None:
            return None

        if self.type == 'string':
            return str(value_to_cast)
        elif self.type == 'integer':
            return int(value_to_cast)
        elif self.type == 'double':
            return float(value_to_cast)
        elif self.type == 'date' or self.type == 'datetime':
            return datetime.strptime(value_to_cast, "%Y-%m-%dT%H:%M:%S.%fZ") if isinstance(value_to_cast,
                                                                                           str) else value_to_cast
        elif self.type == 'time':
            return timeparse(value_to_cast) if isinstance(value_to_cast, str) else value_to_cast
        elif self.type == 'boolean':
            if isinstance(value_to_cast, str):
                return value_to_cast.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
        return value_to_cast
