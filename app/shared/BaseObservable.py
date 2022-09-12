from typing import List
from collections.abc import Callable


class BaseObserver:

    def get(self):
        pass

    def post(self):
        pass

    def patch(self):
        pass

    def put(self):
        pass

    def delete(self):
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