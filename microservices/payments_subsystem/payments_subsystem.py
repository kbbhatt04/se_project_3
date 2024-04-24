import sys
sys.path.append("../../microservices")

import requests
from fastapi import FastAPI
from pymongo.mongo_client import MongoClient

from models import PaymentData
from CreditCardPayment import CreditCardPayment
from DebitCardPayment import DebitCardPayment
from PaymentProcessor import PaymentProcessor
from UPIPayment import UPIPayment

import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()


class PaymentsSubsystem:
    _db = None

    def __init__(self):
        try:
            DATABASE_URL = "mongodb+srv://admin:admin@courses.2nficpj.mongodb.net/?retryWrites=true&w=majority"
            client = MongoClient(DATABASE_URL)
            PaymentsSubsystem._db = client["payments_db"]
        except Exception as e:
            print(e)

    @staticmethod
    def do_payment(user_id: str, course_id: str, payment_method: str):
        paymentsubsystem = PaymentsSubsystem()
        # check if subscribed user or not
        pass
        # else
        # if not subscribed:
        if True:
            processor = PaymentProcessor()
            if payment_method == "credit":
                print("Payment with credit card")
                processor.set_payment_strategy(CreditCardPayment("1234567890123456", "123"))
            elif payment_method == "debit":
                processor.set_payment_strategy(DebitCardPayment("9876543210987654", "1234"))
            elif payment_method == "upi":
                processor.set_payment_strategy(UPIPayment("username@bank"))
            else:
                print("Invalid payment method!")

            url = f"http://localhost:{os.getenv('course_exploration_subsystem')}/courses/{course_id}"
            price = 0
            response = requests.get(url)
            if response.status_code == 200:
                course = response.json()
                price = course["price"]

            processor.process_payment(price)

            payment_data = {"user_id": user_id, "course_id": course_id, "amount": price,
                            "payment_method": payment_method}
            payments_collection = PaymentsSubsystem._db["payments"]
            payments_collection.insert_one(payment_data)

            return {"message": "Payment Successful"}


@app.post("/payment")
def do_payment(payment_data: PaymentData):
    return PaymentsSubsystem.do_payment(payment_data.user_id, payment_data.course_id, payment_data.payment_method)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("payments_subsystem:app", host="0.0.0.0", port=int(os.getenv("payments_subsystem")))
