from django.db import models
from django.core.exceptions import ValidationError

class SeparatedValuesField(models.TextField):
  __metaclass__ = models.SubfieldBase

  def __init__(self, *args, **kwargs):
    self.token = kwargs.pop('token', ':')
    super(SeparatedValuesField, self).__init__(*args, **kwargs)

  def to_python(self, value):
    if not value: return []
    elif isinstance(value, list) or isinstance(value, tuple) or isinstance(value, set): 
      return self.token.join(list(value))
    elif isinstance(value, unicode) or isinstance(value, str):
      return str(value)
    else:
      raise ValidationError('Invalid input for a SeparatedValuesField instance: ' + str(type(value)))
  
  
  # Since using a database requires conversion in both ways, if you override to_python() you also have to override get_prep_value() to convert Python objects back to query values.  
  def get_prep_value(self, value):
    if not value: return None
    elif isinstance(value, unicode) or isinstance(value, str):
      spl = str(value).split(self.token)
      retlst = list(set(x.strip() for x in spl))
      retlst.sort()
      return self.token.join(retlst)
    elif isinstance(value, list) or isinstance(value, set) or isinstance(value, tuple):
      print 'instance list ' + str(value)
      retlst = list(set([str(x).strip() for x in value]))
      retlst.sort()
      print self.token.join(retlst)
      return self.token.join(retlst)
    else:
      raise ValidationError('Cannot get_prep_value for SeparatedValuesField instance: ' + str(type(value)))

  def value_to_string(self, obj):
    value = self._get_val_from_obj(obj)
    return self.get_prep_value(value)

