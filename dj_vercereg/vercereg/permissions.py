from rest_framework import permissions 

class CustomObjectPermissions(permissions.DjangoObjectPermissions):
  """
  Similar to `DjangoObjectPermissions`, but adding 'view' permissions.
  """
  perms_map = {
      'GET': ['%(app_label)s.view_%(model_name)s'],
      'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
      'HEAD': ['%(app_label)s.view_%(model_name)s'],
      'POST': ['%(app_label)s.add_%(model_name)s'],
      'PUT': ['%(app_label)s.change_%(model_name)s'],
      'PATCH': ['%(app_label)s.change_%(model_name)s'],
      'DELETE': ['%(app_label)s.delete_%(model_name)s'],
  }
  
  ## For debugging - REMOVE LATER
  def __init__(self):
    print '** In permissions.py'
    super(CustomObjectPermissions, self).__init__()
