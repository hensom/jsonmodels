from time     import time
from datetime import datetime

class Field(object):
  def __init__(self, key = None):
    self.key = key

  def register_with_model(self, model, name):
    self.name  = name
    self.key   = self.key or name
    self.model = model

    model._fields.append(self)

  def to_python(self, value):
    return value

class DateTimeField(Field):
  FORMAT_EPOCH_SECONDS = 1

  def __init__(self, key = None, format = '%Y-%m-%dT%H:%M:%S'):
    super(DateTimeField, self).__init__(key)

    self.format = format

  def to_python(self, value):
    if self.format == self.FORMAT_EPOCH_SECONDS:
      return datetime.fromtimestamp(value)
    else:
      return time.strptime(value, self.format)

class DateField(DateTimeField):
  def __init__(self, key = None, format = '%Y-%m-%d'):
    super(DateField, self).__init__(key, format)

  def to_python(self, value):
    return super(DateField, self).to_python(value).date()

class ListField(Field):
  def __init__(self, field, key = None):
    super(ListField, self).__init__(key)

    self.field = field

  def to_python(self, value):
    return [self.field.new_from_json(o) for o in value]

class DictField(Field):
  def to_python(self, value):
    if not isinstance(value, dict):
      raise ValueError('%s value must be a dictionary' % self.name)

    return value

