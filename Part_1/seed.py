import json
from mongoengine.errors import NotUniqueError

from models import Author, Quote

if __name__ == "__main__":
    with open("authors.json", encoding="utf-8") as f_authors:
        data_authors = json.load(f_authors)
        for data in data_authors:
            try:
                author = Author(
                    fullname=data["fullname"],
                    born_date=data["born_date"],
                    born_location=data["born_location"],
                    description=data["description"],
                )
                author.save()
            except NotUniqueError:
                print(f"Author already exists: {author.fullname}")

    with open("quotes.json", encoding="utf-8") as q_quotes:
        data_quotes = json.load(q_quotes)
        for data in data_quotes:
            author, *_ = Author.objects(fullname=data["author"])
            quote = Quote(tags=data["tags"], author=author, quote=data["quote"])
            quote.save()
