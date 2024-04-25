from PaymentStrategy import PaymentStrategy


class DebitCardPayment(PaymentStrategy):
    def __init__(self, card_number, pin):
        self.card_number = card_number
        self.pin = pin

    def pay(self, amount):
        print(f"Paying ${amount} using debit card {self.card_number[-4:]}")
        return True
