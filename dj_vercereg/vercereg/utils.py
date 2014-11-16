#from django.http import HttpRequest

# REST_PREFIX = 'rest'
REST_PREFIX = ''

def get_base_rest_uri(request):
  protocol = request.is_secure() and 'https' or 'http'
  host = request.get_host()
  return protocol + '://' + host + REST_PREFIX + '/'
  
def extract_id_from_url(url):
  parts = url.split('/')
  if parts[-1].isdigit(): return parts[-1]
  else: return parts[-2]
