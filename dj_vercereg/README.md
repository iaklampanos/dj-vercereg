dj-vercereg
===========

*dj-vercereg* is the [dispel4py](https://github.com/akrause2014/dispel4py) Registry reference implementation in [django](https://www.djangoproject.com). The dispel4py registry is being developed as part of the [VERCE](http://verce.eu) project (FP7-INFRASTRUCTURES-2011-2, Project no. 283543).

The dispel4py Registry is a RESTful Web service providing functionality for registering workflow entities, such as processing elements (PEs), functions and literals, while encouraging sharing and collaboration via groups and workspaces.

Permissions
-----------
* _VMW_: View metadata of workspace
* _VCW_: View contents of workspace
* _MMW_: Modify metadata of workspace
* _MCW_: Modify content of workspace
* _VG_: View user group
* _MG_: Modify user group
* _AUG_: Add user to group
* _RUG_: Remove user from group
* _AU_: Add user
* _MU_: Modify user

_All permissions are granted to **staff** and **superuser**_.

| Objects \ Action  | list  | retrieve | create | update | partial_update | destroy |
|-------------------|-------|----------|--------|--------|----------------|---------|
| **Workspace**     | *W    |          |        |        |                |         |
| **Workspace item**|       |          |        |
| **User**          |
| **Group**         |
