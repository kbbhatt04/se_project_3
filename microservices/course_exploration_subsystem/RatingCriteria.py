from FilterCriteria import FilterCriteria


class RatingCriteria(FilterCriteria):
    def __init__(self, criteria):
        super().__init__()  # Call the base class constructor without arguments
        self.criteria = criteria

    def meetsCriteria(self, course):
        if course["average_rating"] >= self.criteria:
            return True
        return False
