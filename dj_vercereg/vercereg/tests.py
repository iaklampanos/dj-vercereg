from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from vercereg.models import RegistryUserGroup

class DefaultValuesTestCase(TestCase):
  fixtures = ['fixtures/def_group.json',]
  
  def test_read_all_group_exists(self):
    g = Group.objects.all().get(name='default_read_all_group')
    self.assertIsNotNone(g)

  def test_read_all_rug(self):
    g = Group.objects.all().get(name='default_read_all_group')
    rug = RegistryUserGroup.objects.all().get(group=g)
    self.assertIsNotNone(rug)

