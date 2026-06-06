from pydantic.dataclasses import dataclass


@dataclass()
class User:
    age: int
    name: str


user = User(age=16, name="Nikita")


print(f"user: {user}")
