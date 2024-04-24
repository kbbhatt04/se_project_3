from FilterCriteria import FilterCriteria


class PriceCriteria(FilterCriteria):
    def __init__(self, criteria):
        super().__init__()  # Call the base class constructor without arguments
        self.criteria = criteria

    def meetsCriteria(self, course):
        if course["price"] >= self.criteria:
            return True
        return False
