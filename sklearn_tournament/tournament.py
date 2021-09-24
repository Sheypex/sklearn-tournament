from typing import Collection, Iterator

from sklearn_tournament import Model


class Tournament(Collection):
    def __init__(self):
        self._models = list()

    def __iter__(self) -> Iterator[Model]:
        return iter(self._models)

    def __len__(self) -> int:
        return len(self._models)

    def __contains__(self, __x: object) -> bool:
        return self._models.__contains__(__x)
