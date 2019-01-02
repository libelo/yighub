from .models_base import User

def users(request):
    try:
        user = User.objects.get(user_id=request.session['user_id'])
    except:
        return {'useraccount': 'Anonymous'}
    else:
        return {'useraccount': user}
