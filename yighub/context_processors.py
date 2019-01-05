from .models_base import User
from .models import PublicBoard
import pdb

def users(request):
    active_fund=PublicBoard.objects.filter(active_fund=True)
    try:
        user = User.objects.get(user_id=request.session['user_id'])
    except:
        return {'useraccount': 'Anonymous', 'active_fund': active_fund[:3], 'rep_fund': active_fund[0].name}
    else:
        return {'useraccount': user, 'active_fund': active_fund[:3], 'rep_fund': active_fund[0].name}

