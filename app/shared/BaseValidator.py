from abc import ABC, abstractmethod


class BaseValidator(ABC):
    @classmethod
    @abstractmethod
    def create(cls, payload, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def replace(cls, payload, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def update(cls, payload, *args, **kwargs):
        pass


class BaseListValidator(ABC):
    @classmethod
    @abstractmethod
    def bulk_create(cls, payload, *args, **kwargs):
        pass
