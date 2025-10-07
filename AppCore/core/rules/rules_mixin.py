class ModelRulesMixin:
    _rules = None
    rules_class = None

    @property
    def rules(self):
        if not self._rules:
            self._rules = self.get_model_rules_class(self)

        return self._rules

    def get_model_rules_class(self):
        if not self.rules_class:
            raise ValueError('rules_class não foi definido no model')
        return self.rules_class(instance=self)