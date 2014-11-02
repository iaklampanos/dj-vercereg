#from django.http import HttpRequest

REST_PREFIX = 'rest'

def get_base_rest_uri(request):
  protocol = request.is_secure() and 'https' or 'http'
  host = request.get_host()
  return protocol + '://' + host + '/' + REST_PREFIX + '/'