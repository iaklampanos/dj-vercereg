from rest_framework import permissions 
    

class RegistryUserGroupAccessPermissions(permissions.BasePermission):
  '''Defines permissions for accessing REST registryusergroup objects'''

  def has_permission(self, request, view):
    '''
    General DELETE permissions given only to staff and superusers; other methods are granted to everyone. 
    TODO: Check this works as expected.
    '''
    if request.method == 'DELETE':
      return request.user.is_superuser or request.user.is_staff
    else: 
      return True

  def has_object_permission(self, request, view, obj):
    '''Full permissions for superusers, staff or group owners'''
    return request.user.is_superuser or request.user.is_staff or request.user==obj.owner


class ConnectionPermissions(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    return request.user.is_superuser or request.user.is_staff or request.user == obj.pesig.user or len(request.user.groups.filter(name='default_read_all_group')) > 0


class FunctionParameterPermissions(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    return request.user.is_superuser or request.user.is_staff or request.user == obj.parent_function.user or len(request.user.groups.filter(name='default_read_all_group')) > 0
  

class UserAccessPermissions(permissions.BasePermission):
  '''Defines permissions for accessing REST user objects'''
  
  def has_permission(self, request, view):
    if request.method == 'POST' or request.method == 'DELETE':
      return request.user.is_superuser or request.user.is_staff
    else: 
      return True

  # def has_object_permission(self, request, view, obj):
  #   return request.user.is_superuser or request.user.is_staff or request.user==obj


class WorkspaceItemPermissions(permissions.BasePermission):
  '''
  Handles the permissions of workspace items.
  '''

  def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
      return request.user == obj.user or request.user.is_superuser or request.user.is_staff or len(request.user.groups.filter(name='default_read_all_group')) > 0
    else:
      # print request.user == obj.workspace.owner or request.user.is_superuser or request.user.is_staff or request.user.has_perm('modify_content_workspace', obj.workspace)
      
      return request.user == obj.workspace.owner or request.user.is_superuser or request.user.is_staff or request.user.has_perm('modify_content_workspace', obj.workspace)


class WorkspaceBasedPermissions(permissions.BasePermission):
  '''
  Handles permissions for workspaces.
  TODO: Document permissions properly...
  '''
  
  # def has_permission(self, request, view):
  #   return True

  def has_object_permission(self, request, view, obj):
    is_owner = request.user == obj.owner
    is_superuser = request.user.is_superuser
    
    if request.method in permissions.SAFE_METHODS:
      has_view_meta_perms = request.user.has_perm('view_meta_workspace', obj)  
      return has_view_meta_perms or is_owner or is_superuser or len(request.user.groups.filter(name='default_read_all_group')) > 0
    else:
      if request.method == 'PUT':
        has_modify_meta_perms = request.user.has_perm('modify_meta_workspace', obj)
        return has_modify_meta_perms or is_superuser or is_owner
      elif request.method == 'POST':
        has_view_contents = request.user.has_perm('view_contents_workspace', obj)
        return has_view_contents or is_superuser or is_owner
      elif request.method == 'DELETE':
        return is_superuser
      else:
        return False
