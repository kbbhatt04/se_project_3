from PaymentStrategy import PaymentStrategy


class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number, cvv):
        self.card_number = card_number
        self.cvv = cvv

    def pay(self, amount):
        print(f"Paying ${amount} using credit card {self.card_number[-4:]}")
        return True
