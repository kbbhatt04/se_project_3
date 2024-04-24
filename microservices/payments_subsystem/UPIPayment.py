from PaymentStrategy import PaymentStrategy


class UPIPayment(PaymentStrategy):
    def __init__(self, vpa):
        self.vpa = vpa

    def pay(self, amount):
        print(f"Paying ${amount} using UPI VPA: {self.vpa}")
        return True
