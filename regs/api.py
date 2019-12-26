from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.models import User
from .models import *

def token_required(view):
    def wrapper(request, *args, **kwargs):
        if not 'HTTP_AUTHORIZATION' in request.META:
            return HttpResponse('Unauthorized', status=401)
        token = Token.objects.filter(token = request.META['HTTP_AUTHORIZATION']).first()
        if not token:
            return HttpResponse('Unauthorized', status=401)
        if token.role == 'guest' and request.method == 'POST':
            return HttpResponse('Your token is a guest token, you\'re only allowed to do GET requests', status = 405)
        return view(request, *args, **kwargs)
    return wrapper

@require_GET
@token_required
def NewsAPI(request):
    number = request.GET.get('number', 5)
    try:
        _number = int(number)
    except ValueError:
        return HttpResponse('Bad Request', status = 400)
    news = News.objects.all().order_by('-pk').values()[:_number]
    return JsonResponse({'status' : 1, 'news' : [n for n in news]}, json_dumps_params={'indent': 2})

@csrf_exempt
@require_POST
@token_required
def NewsEditAPI(request):
    _id = request.POST.get('id', None)
    _title = request.POST.get('title', None)
    _text = request.POST.get('text', None)
    if not _id:
        return HttpResponse('Bad Request', status = 400)
    try:
        _number = int(_id)
    except ValueError:
        return HttpResponse('Bad Request', status = 400)
    try:
        if not _title and not _text:
            return JsonResponse({'status' : 0, 'error' : 'No new title and no text is provided'}, json_dumps_params = {'indent' : 2})
        obj = News.objects.get(pk = _id)
        if _title and not _text:
            if _title == obj.title:
                return JsonResponse({'status' : 0, 'error' : 'Title has not changed'}, json_dumps_params = {'indent' : 2})
            obj.title = _title
            obj.save()
            return JsonResponse({'status' : 1, 'obj' : model_to_dict(obj)}, json_dumps_params = {'indent' : 2})
        elif _text and not _title:
            if _text == obj.text:
                return JsonResponse({'status' : 0, 'error' : 'Text has not changed'})
            obj.text = _text
            obj.save()
            return JsonResponse({'status' : 1, 'obj' : model_to_dict(obj)}, json_dumps_params = {'indent' : 2})
        else:
            if _title == obj.title and _text == obj.text:
                return JsonResponse({'status' : 0, 'error' : 'Title and Text haven\'t changed'}, json_dumps_params = {'indent' : 2})
            obj.title, obj.text = _title, _text
            obj.save()
            return JsonResponse({'status' : 1, 'obj' : model_to_dict(obj)}, json_dumps_params = {'indent' : 2})

    except News.DoesNotExist:
        return JsonResponse({'status' : 0, 'error' : 'No object with this id : {}'.format(_id)}, json_dumps_params = {'indent' : 2})

@require_GET
@token_required
def NewsByIdAPI(request):
    _id = request.GET.get('id', None)
    if not _id:
        return HttpResponse('Bad Request', status = 400)
    try:
        _number = int(_id)
    except ValueError:
        return HttpResponse('Bad Request', status = 400)
    try:
        obj = News.objects.get(pk = _id)
        return JsonResponse({'status' : 1, 'obj' : model_to_dict(obj)}, json_dumps_params = {'indent' : 2})
    except News.DoesNotExist:
        return JsonResponse({'status' : 0, 'error' : 'No object with this id : {}'.format(_id)}, json_dumps_params = {'indent' : 2})

@csrf_exempt
@require_POST
@token_required
def NewsCreateAPI(request):
    _title = request.POST.get('title', None)
    _text = request.POST.get('text', None)

    if not _title:
        return JsonResponse({'status' : 0, 'error' : 'No title is provided'}, json_dumps_params = {'indent' : 2})
    if not _text:
        return JsonResponse({'status' : 0, 'error' : 'No text is provided'}, json_dumps_params = {'indent' : 2})
    if not _title and not _text:
        return JsonResponse({'status' : 0, 'error' : 'Neither title or text is provided'}, json_dumps_params = {'indent' : 2})
    if len(_title) > 100:
        return JsonResponse({'status' : 0, 'error' : 'Title too long, title has to be less than 100 character'}, json_dumps_params = {'indent' : 2})
    obj = News(title = _title, text = _text)
    obj.save()
    return JsonResponse({'status' : 1, 'obj' : model_to_dict(obj)}, json_dumps_params = {'indent' : 2})

@require_GET
@token_required
def AdminsAPI(request):
    obj = User.objects.filter(is_staff = True, is_active = True)
    return JsonResponse({'status' : 1, 'admins' : [p.username for p in obj]}, json_dumps_params = {'indent' : 2})
