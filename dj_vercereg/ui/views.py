from django.shortcuts import render
from django.template import RequestContext
from django.template import loader
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from vercereg.models import Workspace
from ui.models import FavouriteWorkspaces

from django.contrib.auth.models import Group
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from dj_vercereg.settings import LOGIN_URL
from django.contrib.auth import logout

from django.http import JsonResponse


import json

@login_required
def index(request):
    own_workspaces = Workspace.objects.filter(owner=request.user)
    fav_workspaces = []
    for f in FavouriteWorkspaces.objects.filter(user=request.user):
        fav_workspaces.append(f.workspace)

    context = {'own_workspaces': own_workspaces,
               'fav_workspaces': fav_workspaces}
    return render(request, 'ui/index.html', context)

@login_required
def view_workspace(request, workspace_id):
    try:
        w = Workspace.objects.get(pk=workspace_id)
        own_workspaces = Workspace.objects.filter(owner=request.user)
        fav_workspaces = []
        for f in FavouriteWorkspaces.objects.filter(user=request.user):
            fav_workspaces.append(f.workspace)
        context = {'own_workspaces': own_workspaces,
                   'fav_workspaces': fav_workspaces,
                   'workspace': w}
        return render(request, 'ui/index.html', context)
    except ObjectDoesNotExist as e:
        raise Http404('Workspace ' + str(workspace_id) +
                      ' not found.')
    # except Exception as e:
    #     raise Http404('Unknown error when retrieving workspace ' +
    #                   str(workspace_id))

@login_required
def flow(request, workspace_id):
    try:
        w = Workspace.objects.get(pk=workspace_id)
        context = {'workspace': w}
        return render(request, 'ui/flow.html', context)
    except ObjectDoesNotExist as e:
        raise Http404('Workspace ' + str(workspace_id) +
                      ' not found.')

@login_required
def toggle_workspace_fav(request, workspace_id):
    try:
        w = Workspace.objects.get(pk=workspace_id)
        f = FavouriteWorkspaces.objects.filter(workspace=w, user=request.user)
        if not f:
            newfav = FavouriteWorkspaces(workspace=w, user=request.user)
            newfav.save()
            return JsonResponse({'f': newfav.id})
        else:
            # FavouriteWorkspaces(workspace=w, user=request.user).delete()
            f.delete()
            return JsonResponse({'f': None})
    except ObjectDoesNotExist as e:
        raise Http404('Workspace ' + str(workspace_id) +
                      ' not found.')
    # except:
    #     pass
    
@login_required
def is_workspace_faved(request, workspace_id):
    try:
        w = Workspace.objects.get(pk=workspace_id)
        f = FavouriteWorkspaces.objects.filter(workspace=w, user=request.user)
        if not f:
            return JsonResponse({'faved': False})
        else:
            return JsonResponse({'faved': True})
    except ObjectDoesNotExist as e:
        raise Http404('Workspace ' + str(workspace_id) +
                      ' not found.')

# @login_required
# def get_workspace_contents(requests, workspace_id):
#     try:
#         w = Workspace.objects.get(pk=workspace_id)
#
#     except ObjectDoesNotExist as e:
#         raise Http404('Workspace ' + str(workspace_id) +
#                       ' not found.')
#
