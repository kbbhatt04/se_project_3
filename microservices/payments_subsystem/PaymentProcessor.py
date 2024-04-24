class PaymentProcessor:
    def __init__(self):
        self.strategy = None

    def set_payment_strategy(self, strategy):
        self.strategy = strategy

    def process_payment(self, amount):
        if self.strategy:
            result = self.strategy.pay(amount)
            if result:
                print("Payment successful!")
        else:
            print("No payment strategy set!")
