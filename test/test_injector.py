from injector import Injector, inject

injector = Injector()


class A:
    name: str = "llmops"


@inject
class B:
    def __init__(self, a: A) -> None:
        self.a = a

    def print_name(self):
        print(self.a.name)


b = injector.get(B)
b.print_name()

