# Copyright 2014 The University of Edinburgh
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from vercereg.models import FnImplementation
from vercereg.models import FunctionSig
from vercereg.models import FunctionParameter
from vercereg.models import LiteralSig
from vercereg.models import PEImplementation
from vercereg.models import PESig
from vercereg.models import Workspace
from vercereg.models import Connection

from django.utils import timezone

import serializers

# from django.db import transaction


class WorkspaceCloner:
    
    # The package suffix for copying over dependent entities, such as 
    # implementations, when the `target_name` parameter for the parent entity 
    # has been specified.
    COPY_IMPL_PCKG_SUFFIX = 'implementations'

    """Implements a deep cloner for vercereg workspaces."""

    def __init__(self,
                 original_workspace,
                 name,
                 user,
                 target_workspace=None,
                 context=None):
        self.original_workspace = original_workspace
        self.target_workspace = target_workspace
        self.name = name
        self.user = user
        self.context = context
        # dictionary fromWorkspaceItem:toWorkspaceItem, when cloned
        self.dic = {}

    def clone_pe(self, pe, target_pckg=None, target_name=None):
        if pe in self.dic:
            return self.dic[pe]
        
        ser = serializers.PESigSerializer(pe,
                                          context=self.context)
        url = ser.data['url']
        textdat = str(ser.data)
        
        ret = PESig()
        ret.description = pe.description
        ret.kind = pe.kind
        ret.workspace = self.target_workspace
        ret.pckg = target_pckg or pe.pckg
        ret.name = target_name or pe.name
        ret.creation_date = timezone.now()  # Update the creation date/time;
        ret.user = self.user
        ret.clone_of = url
        ret.clone_of_ser = textdat
        
        ret.save()  # Initial save
        for c in pe.connections.all():
            newconn = Connection()
            newconn.kind = c.kind
            newconn.name = c.name
            newconn.s_type = c.s_type
            newconn.d_type = c.d_type
            newconn.comment = c.comment
            newconn.is_array = c.is_array
            newconn.modifiers = c.modifiers
            newconn.pesig = ret
            
            newconn.save()
        for p in pe.peimpls.all():
            self.clone_peimpl(p, ret,
                              target_pckg=ret.pckg + '.' +\
                              WorkspaceCloner.COPY_IMPL_PCKG_SUFFIX)
        self.dic[pe] = ret
        return ret

    def clone_peimpl(self, peimpl, newparent=None,
                     target_pckg=None, target_name=None):
        if peimpl in self.dic:
            return self.dic[peimpl]
        ser = serializers.PEImplementationSerializer(peimpl,
                                                     context=self.context)
        url = ser.data['url']
        textdat = str(ser.data)
        
        ret = PEImplementation()
        ret.workspace = self.target_workspace
        ret.pckg = target_pckg or peimpl.pckg
        ret.name = target_name or peimpl.name
        ret.creation_date = timezone.now()
        ret.description = peimpl.description
        ret.code = peimpl.code
        ret.user = self.user
        if newparent:
            ret.parent_sig = newparent
        ret.clone_of = url
        ret.clone_of_ser = textdat
        
        ret.save()
        self.dic[peimpl] = ret
        return ret

    def clone_literal(self, lit,
                      target_pckg=None, target_name=None):
        if lit in self.dic:
            return self.dic[lit]
        ser = serializers.LiteralSigSerializer(lit,
                                               context=self.context)
        url = ser.data['url']
        textdat = str(ser.data)
        ret = LiteralSig()
        ret.workspace = self.target_workspace
        ret.pckg = target_pckg or lit.pckg
        ret.name = target_name or lit.name
        ret.creation_date = timezone.now()
        ret.description = lit.description
        ret.value = lit.value
        ret.user = self.user
        ret.clone_of = url
        ret.clone_of_ser = textdat
        
        ret.save()
        self.dic[lit] = ret
        return ret

    def clone_function(self, fun,
                       target_pckg=None, target_name=None):
        if fun in self.dic:
            return self.dic[fun]
        
        ser = serializers.FunctionSigSerializer(fun,
                                                context=self.context)
        url = ser.data['url']
        textdat = str(ser.data)
        
        ret = FunctionSig()
        ret.workspace = self.target_workspace
        ret.pckg = target_pckg or fun.pckg
        ret.name = target_name or fun.name
        ret.creation_date = timezone.now()
        ret.description = fun.description
        ret.return_type = fun.return_type
        ret.user = self.user
        ret.clone_of = url
        ret.clone_of_ser = textdat

        ret.save()
        for param in fun.parameters.all():
            newparam = FunctionParameter()
            newparam.param_name = param.param_name
            newparam.param_type = param.param_type
            newparam.parent_function = ret
            newparam.save()
        for fnimpl in fun.fnimpls.all():
            self.clone_fnimpl(fnimpl, ret, 
                              target_pckg=ret.pckg + '.' +\
                              WorkspaceCloner.COPY_IMPL_PCKG_SUFFIX)

        # ret.save()
        self.dic[fun] = ret
        return ret

    def clone_fnimpl(self, fnimpl, newparent=None,
                     target_pckg=None, target_name=None):
        if fnimpl in self.dic:
            return self.dic[fnimpl]
        
        ser = serializers.FnImplementationSerializer(fnimpl,
                                                     context=self.context)
        url = ser.data['url']
        textdat = str(ser.data)
        
        ret = FnImplementation()
        ret.workspace = self.target_workspace
        ret.pckg = target_pckg or fnimpl.pckg
        ret.name = target_name or fnimpl.name
        ret.creation_date = timezone.now()
        ret.description = fnimpl.description
        ret.code = fnimpl.code
        if newparent:
            ret.parent_sig = newparent
        ret.user = self.user
        ret.clone_of = url
        ret.clone_of_ser = textdat

        ret.save()
        self.dic[fnimpl] = ret
        return ret

    def clone(self):
        """Deep clone the original workspace into the target and return it."""
        # print 'Cloning ' + str(self.original_workspace)

        ser = serializers.WorkspaceSerializer(self.original_workspace,
                                              context=self.context)
        url = ser.data['url']
        textdat = str(ser.data)
        self.target_workspace = Workspace(
            name=self.name,
            owner=self.user,
            creation_date=timezone.now(),
            clone_of=url,
            clone_of_ser=textdat,
            description=self.original_workspace.description)

        self.target_workspace.save()

        for pe in self.original_workspace.get_pesigs():
            self.dic[pe] = self.clone_pe(pe)
        for lit in self.original_workspace.get_literalsigs():
            self.dic[lit] = self.clone_literal(lit)
        for fn in self.original_workspace.get_fnsigs():
            self.dic[fn] = self.clone_function(fn)
        for peimpl in self.original_workspace.get_peimplementations():
            self.dic[peimpl] = self.clone_peimpl(peimpl)
        for fnimpl in self.original_workspace.get_fnimplementations():
            self.dic[fnimpl] = self.clone_fnimpl(fnimpl)

        return self.target_workspace
