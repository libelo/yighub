from .models_base import User
from .models import PublicBoard
import pdb

def users(request):
    active_fund=PublicBoard.objects.filter(active_fund=True)

    if len(active_fund)==0:
        active_fund=PublicBoard.objects.filter(id=98)
        context={'rep_fund': active_fund[0]}
    else:
        context={'rep_fund': active_fund[0]}

    try:
        user = User.objects.get(user_id=request.session['user_id'])
    except:
        context.update({'useraccount': 'Anonymous', 'active_fund': active_fund[:3]})
        return context
    else:
        context.update({'useraccount': user, 'active_fund': active_fund[:3]})
        return context

