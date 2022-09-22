from typing import List
from collections.abc import Callable


class BaseObserver:
    
    def __repr__(self, *args, **kwargs):
        return self.__class__.__name__

    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass

    def patch(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

class BaseObservable:

    def __init__(self): 
        self.observers = set()

    def notify(self, method: str, payload: any, *args, **kwargs): 
        for obs in self.observers:
            callback = getattr(obs, method)
            if callback: 
                callback(payload)

    def subscribe(self, observer: BaseObserver):
        self.observers.add(observer)

    def unsubscribe(self, observer: BaseObserver):
        self.observers.discard(observer)