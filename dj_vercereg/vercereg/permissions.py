from rest_framework import permissions 



class WorkspaceItemPermissions(permissions.BasePermission):
  '''
  Handles the permissions of workspace items.
  '''

  def has_object_permission(self, request, view, obj):
    return request.user == obj.owner or request.user.is_superuser


class WorkspaceBasedPermissions(permissions.BasePermission):
  '''
  Handles permissions for workspaces.
  '''
  
  # def has_permission(self, request, view):
  #   return True

  def has_object_permission(self, request, view, obj):
    # print 'permissions: checking workspace: ', str(obj)
    if request.method in permissions.SAFE_METHODS:
      return request.user == request.user.has_perm('view_meta_workspace', obj) or request.user == obj.owner or request.user.is_superuser
    else:
      if request.method == "PUT":
        return request.user == obj.owner or request.user.is_superuser or request.user.has_perm('modify_meta_workspace', w)
      else:
        return True
