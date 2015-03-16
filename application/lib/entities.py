
class BaseEntity(dict):
    pass


class SQLAlchemyEntity(BaseEntity):

    def __init__(self, model):
        props = (prop for prop in dir(model)
                 if not prop.startswith('_')
                 and not callable(getattr(model, prop)))

        kwargs = dict((prop, getattr(model, prop)) for prop in props if hasattr(self, prop))
        super(SQLAlchemyEntity, self).__init__(self, **kwargs)


class Subject(SQLAlchemyEntity):

    id = None
    code = None
    teachers = None
    groups = None


class Group(SQLAlchemyEntity):

    id = None
    name = None
    subject = None
    students = None

