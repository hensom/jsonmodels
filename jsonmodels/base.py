class ModelMetaClass(type):
  def __new__(cls, name, bases, attrs):
    metaclass = attrs.get('__metaclass__')

    super_new = super(ModelMetaClass, cls).__new__

    if metaclass and issubclass(metaclass, ModelMetaClass):
      return super_new(cls, name, bases, attrs)

    new_class = super_new(cls, name, bases, attrs)

    new_class._fields = []

    for attr_name, attr_value in attrs.items():
      new_class.add_to_class(attr_name, attr_value)

    return new_class

  def add_to_class(cls, name, value):
    if hasattr(value, 'register_with_model'):
      value.register_with_model(cls, name)

    setattr(cls, name, value)

class Model(object):
  __metaclass__ = ModelMetaClass

  def __init__(self, **kwargs):
    self._load_params(kwargs)

  @classmethod
  def new_from_json(cls, params):
    self = cls()

    self._load_params(params, raw = True)

    return self

  def _load_params(self, params, raw = False):
    field_map = { }

    for field in self._fields:
      field_map[ field.key ] = field

    for key, value in params.iteritems():
      if key not in field_map:
        raise TypeError("%s got an unexpected keyword argument '%s'" % (self.__class__, key))
      else:
        field = field_map[key]

        del field_map[key]

        if raw:
          setattr(self, field.name, field.to_python(value))
        else:
          setattr(self, field.name, value)
