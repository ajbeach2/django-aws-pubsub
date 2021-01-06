from aws_pubsub import register


def foo(message: dict):
    print("fooooooooooooooooooooooo")


def bar(message: dict):
    value = message["Value"]
    return value * 10


def duck(message: dict):
    return "quack"


def cat(message: dict):
    return "meow"


register(foo, alias="foo")
register(bar, alias="bar")
register(cat, alias="cat")
register(duck)
