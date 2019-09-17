import base64

from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
# from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone

from django.contrib.auth.models import User # django's builtin User model
from . models import Upload

def basicauth(view):
    def wrap(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2 and auth[0].lower() == "basic":
                uname, passwd = base64.b64decode(auth[1]).decode('utf-8').split(':')
                user = authenticate(username=uname, password=passwd)
                if user is not None and user.is_active:
                    request.user = user
                    return view(request, *args, **kwargs)

        response = JsonResponse({"error": "no auth no good"}, status=401)
        response['WWW-Authenticate'] = 'Basic realm="User Visible Realm"'
        return response
    return wrap


@csrf_exempt
@basicauth
def upload(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    
    if "file" not in request.FILES:
        return JsonResponse({"error": "missing file parameter!"}, status=422)

    ul = Upload(f=request.FILES.get("file"), date=timezone.now(), u=request.user)
    ul.save()

    return JsonResponse({"uuid": ul.uuid}) #"url": request.build_absolute_uri(ul.f.url),


@basicauth
def grab(request, fuuid):
    if request.method != "GET":
        return JsonResponse({"error": "GET only"}, status=405)

    #return FileResponse(open(ul.f.url, 'rb'), as_attachment=True)
    return FileResponse(get_object_or_404(Upload, uuid=fuuid).f.open('rb'), as_attachment=True)


@csrf_exempt
def deleteall(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    qs = Upload.objects.all()
    for o in qs:
        o.f.delete()

    qs.delete()
    return JsonResponse({"info": "poof"})


@csrf_exempt
def signup(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    if "username" not in request.POST or "password" not in request.POST:
        return JsonResponse({"error": "missing username/password parameter!"}, status=422)

    if User.objects.filter(username=request.POST.get("username")).exists():
        return JsonResponse({"error": "username exists"}, status=422)
    
    User.objects.create_user(request.POST['username'], password=request.POST['password']) #creates user with the password
    return JsonResponse({"info": "ok"})
