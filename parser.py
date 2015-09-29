class Word:
    def __init__(self, function_matcher,
                 set_default=None,
                 identifier=None):
        self.function_matcher = function_matcher
        self.value = set_default
        self.identifer = identifier

        self.list_callback = list()

    def __call__(self, iterable):
        if self.function_matcher(iterable):
            self.value = iterable
            for callback in self.list_callback:
                self.value = callback(self.value)

    def add_callback(self, callback):
        self.list_callback.append(callback)
