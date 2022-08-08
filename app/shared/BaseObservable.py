from typing import List
from collections.abc import Callable


class BaseObserver:

    def __init__(self, callback: Callable, methods: List[str], *args, **kwargs): 
        self.callback = callback
        self.GET = "GET" in methods
        self.POST = "POST" in methods
        self.PATCH = "PATCH" in methods
        self.DELETE = "DELETE" in methods
        self.PUT = "PUT" in methods
        

class BaseObservable:

    def __init__(self): 
        self.observers = {}

    def notify(self, method: str, payload: any, *args, **kwargs): 
        for _, obs in self.observers.items():
            if getattr(obs, method, False): 
                obs.callback(payload)

    def subscribe(self, observer: BaseObserver):
        self.observers[observer.endpoint] = observer

    def unsubscribe(self, observer: BaseObserver):
        self.observers.pop(observer.endpoint)