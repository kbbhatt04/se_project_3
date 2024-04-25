from FilterCriteria import FilterCriteria


class LevelCriteria(FilterCriteria):
    def __init__(self, criteria):
        super().__init__()
        self.criteria = criteria

    def meetsCriteria(self, course):
        if course["level"] == self.criteria:
            return True
        return False
