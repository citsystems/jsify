class UndefinedClass:
    """
    Class which behaves like JavaScript "undefined" value
    """
    Undefined = None

    @classmethod
    def __new__(cls, *args):
        if UndefinedClass.Undefined is None:
            UndefinedClass.Undefined = super().__new__(*args)
        return UndefinedClass.Undefined

    @classmethod
    def __call__(cls):
        return UndefinedClass.Undefined

    @classmethod
    def __repr__(cls):
        return None

    @classmethod
    def __str__(cls):
        return "Undefined"

    @classmethod
    def __getattr__(cls, item):
        return UndefinedClass.Undefined

    @classmethod
    def __getitem__(cls, item):
        return UndefinedClass.Undefined

    @classmethod
    def __eq__(cls, other):
        return (other is None) or isinstance(other, cls)

    @classmethod
    def __setstate__(cls, state):
        pass

    @classmethod
    def __getstate__(cls):
        return {}

    @classmethod
    def __bool__(cls):
        return False


# Object which behaves like JavaScript 'undefined' value
Undefined = UndefinedClass()
