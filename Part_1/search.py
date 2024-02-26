from typing import Any

import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def search_by_authors(author_name: str) -> dict[Any, list[Any]]:
    authors = Author.objects(fullname__istartswith=author_name)
    result_authors = {}
    unique_quotes = set()
    for a in authors:
        quotes = Quote.objects(author=a)
        for q in quotes:
            unique_quotes.add(q.quote)
            result_authors[a.fullname] = list(unique_quotes)
    return result_authors


@cache
def search_by_tags(tag_name: str) -> list[str | None]:
    quotes = Quote.objects()
    unique_quotes = set()
    for q in quotes:
        if any(t.lower().startswith(tag_name.lower()) for t in q.tags):
            unique_quotes.add(q.quote)
    return list(unique_quotes)


def parse_input(user_inp: str) -> tuple[str, str]:
    parts = user_inp.split(":")
    command_name = parts[0].strip()
    argument_name = ":".join(parts[1:]).strip()
    return command_name, argument_name


if __name__ == "__main__":
    while True:

        user_input = input(">>> ").strip()

        command, argument = parse_input(user_input)

        if command == "name":
            author = argument
            print(search_by_authors(author))

        elif command == "tag":
            tag = argument
            print(f"Quotes by tag: {tag}")
            print(search_by_tags(tag))

        elif command == "tags":
            tags = argument.split(",")
            print(f'Quotes by tags: {", ".join(tags)}')
            result = [search_by_tags(tag.strip()) for tag in tags]
            print(result)

        if user_input == "exit":
            break
