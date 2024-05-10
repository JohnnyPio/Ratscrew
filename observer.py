class Observer:
    def __init__(self):
        self.callbacks = []

    def add_observer(self, callback):
        self.callbacks.append(callback)

    def notify_observers(self):
        for callback in self.callbacks:
            callback()

    def remove_observers(self):
        self.callbacks = []
