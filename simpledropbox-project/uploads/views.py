import base64

from django.shortcuts import render

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.conf import settings

from . models import Upload

def basicauth(view):
    def wrap(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == "basic":
                    uname, passwd = base64.b64decode(auth[1]).split(':')
                    user = authenticate(username=uname, password=passwd)
                    if user is not None and user.is_active:
                        request.user = user
                        return view(request, *args, **kwargs)

        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="{}"'.format(
            settings.BASIC_AUTH_REALM
        )
        return response
    return wrap


@csrf_exempt
def upload(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    
    if "file" not in request.FILES:
        return JsonResponse({"error": "missing file parameter!"}, status=422)

    ul = Upload(f=request.FILES.get("file"))
    ul.save()

    return JsonResponse({"info": "ok", "url": request.build_absolute_uri(ul.f.url)})
