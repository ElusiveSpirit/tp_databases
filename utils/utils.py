from rest_framework.parsers import JSONParser
from django.core.exceptions import PermissionDenied


def parse_json_or_error(request):
    try:
        return JSONParser().parse(request)
    except:
        raise PermissionDenied()
