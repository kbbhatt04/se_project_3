from abc import ABC, abstractmethod


class FilterCriteria(ABC):
    @abstractmethod
    def meetsCriteria(self, course):
        pass
