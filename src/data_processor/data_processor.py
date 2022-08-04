from abc import abstractmethod
from typing import Generic, TypeVar, TypedDict
from .params_model import ParamsModel

from eventstream.eventstream import Eventstream

P = TypeVar("P", bound=TypedDict)


class DataProcessor(Generic[P]):
    params: ParamsModel[P]

    def __init__(self, params: P):
        pass

    @abstractmethod
    def apply(self, eventstream: Eventstream) -> Eventstream:
        pass
