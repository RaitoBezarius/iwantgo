class Stream:

    def __init__(self, iterable):
        self.iterable = iterable
        self.saves = list()
        self.iterator = 0
        self.length = len(iterable)

    def __iter__(self):
        return self

    def __next__(self):
        if self.iterator < self.length:
            rv = self.iterable[self.iterator]
            self.iterator += 1

            return rv

        raise StopIteration

    def save(self):
        self.saves.append(self.iterator)

    def apply(self):
        self.iterator = self.saves[-1]

    def pop(self):
        self.iterator = self.saves.pop()

    def drop(self):
        self.saves.pop()


class WordRule:

    def __init__(self, function_matcher,
                 identifier=None,
                 default=None):
        self.function_matcher = function_matcher
        self.value = default
        self.identifier = identifier

        self.list_callback = list()

    def __call__(self, element):
        if self.function_matcher(element):
            self.value = element
            for callback in self.list_callback:
                self.value = callback(self.value)

            if self.identifier:
                return {self.identifier: self.value}
            else:
                return dict()

    def __add__(self, rule):
        return UnionRule([self, rule])

    def __radd__(self, rule):
        return UnionRule([rule, self])

    def __mul__(self, rule):
        return ConcatenationRule([self, rule])

    def __rmul__(self, rule):
        return ConcatenationRule([rule, self])

    def add_callback(self, callback):
        self.list_callback.append(callback)


class Rule:

    def __init__(self, rules=None):
        if rules == None:
            self.rules = list()
        else:
            self.rules = rules.copy()


class ConcatenationRule(Rule):

    def __add__(self, rule):
        return UnionRule([self, rule])

    def __radd__(self, rule):
        return UnionRule([rule, self])

    def __mul__(self, rule):
        return ConcatenationRule(self.rules + [rule])

    def __rmul__(self, rule):
        return ConcatenationRule([rule] + self.rules)

    def __call__(self, stream):
        if not isinstance(stream, Stream):
            stream = Stream(stream)

        rv = dict()
        stream.save()

        for rule in self.rules:
            result = rule(stream)
            if result == None:
                break
            rv.update(result)
        else:
            stream.drop()
            return rv

        stream.pop()


class UnionRule:

    def __add__(self, rule):
        return UnionRule(self.rules + [rule])

    def __radd__(self, rule):
        return UnionRule([rule] + self.rules)

    def __mul__(self, rule):
        return ConcatenationRule([self, rule])

    def __rmul__(self, rule):
        return ConcatenationRule([rule, self])

    def __call__(self, stream):
        if not isinstance(stream, Stream):
            stream = Stream(stream)

        rv = dict()
        stream.save()

        for rule in self.rules:
            stream.apply()
            result = rule(stream)
            if result != None:
                return result

        stream.pop()


def keyword(keyword):
    return WordRule(lambda s: s == keyword)


def argument(name, default=None, matcher=None):
    if matcher != None:
        return WordRule(matcher, name, default)
    return WordRule(lambda s: bool(s), name, default)
