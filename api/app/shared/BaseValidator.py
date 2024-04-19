from abc import ABC, abstractmethod


class BaseValidator(ABC):
    @classmethod
    @abstractmethod
    def retrieve(cls, id, payload, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def replace(cls, id, payload, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def update(cls, id, payload, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def destroy(cls, id, payload, *args, **kwargs):
        pass


class BaseListValidator(ABC):
    @classmethod
    @abstractmethod
    def list(cls, payload, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def bulk_create(cls, payload, *args, **kwargs):
        pass
