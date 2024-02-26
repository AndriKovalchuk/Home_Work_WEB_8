from mongoengine import *

connect(
    db="Home_Work_WEB_8",
    host="mongodb+srv://andrii:sSMTQV52H7RbLUbm@cluster0.irqsim5.mongodb.net/?retryWrites=true&w=majority",
)


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=50)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    tags = ListField(max_length=50)
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField()
    meta = {"collection": "quotes"}
