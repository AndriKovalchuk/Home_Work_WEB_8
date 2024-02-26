import faker
from mongoengine import connect, Document, StringField, BooleanField
import pika

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()

channel.queue_declare(queue="email_queue")
channel.queue_declare(queue="sms_queue")

connect(
    username="andrii",
    password="sSMTQV52H7RbLUbm",
    host="mongodb+srv://cluster0.irqsim5.mongodb.net/Home_Work_WEB_8_Part_2?retryWrites=true&w=majority",
    ssl=True,
)


class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    sent_email = BooleanField(default=False)
    cell_phone = StringField(required=True)
    sent_sms = BooleanField(default=False)
    preferred_communication = StringField(choices=("SMS", "Email"))
    meta = {"collection": "contacts"}


def create_contact(num_contact: int) -> None:
    fake = faker.Faker()
    for _ in range(num_contact):
        full_name = fake.name()
        email = fake.email()
        cell_phone = fake.phone_number()
        preferred_communication = fake.random_element(elements=("SMS", "Email"))
        contact = Contact(
            full_name=full_name,
            email=email,
            cell_phone=cell_phone,
            preferred_communication=preferred_communication,
        )
        contact.save()

        if contact.preferred_communication == "SMS":
            channel.basic_publish(
                exchange="", routing_key="sms_queue", body=str(contact.id)
            )
        elif contact.preferred_communication == "Email":
            channel.basic_publish(
                exchange="", routing_key="email_queue", body=str(contact.id)
            )

    print("Contacts sent to queues")

    connection.close()


if __name__ == "__main__":
    create_contact(50)
