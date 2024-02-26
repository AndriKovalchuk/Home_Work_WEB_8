import pika
from mongoengine import connect, Document, StringField, BooleanField

connect(
    db="Home_Work_WEB_8_Part_2",
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


def send_sms(contact_id):
    contact = Contact.objects.get(id=contact_id)
    contact.sent_sms = True
    contact.save()
    print(f"SMS sent to {contact.cell_phone}")


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="sms_queue")


def callback(ch, method, properties, body):
    contact_id = body.decode()
    send_sms(contact_id)


channel.basic_consume(queue="sms_queue", on_message_callback=callback, auto_ack=True)

print("Consumer SMS is waiting for messages. To exit press CTRL+C")
channel.start_consuming()
