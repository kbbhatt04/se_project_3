from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount):
        print(f"Paying ${amount} in cash")
        return True