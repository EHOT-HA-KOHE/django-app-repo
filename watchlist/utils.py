from watchlist.models import UserCollections


def get_user_collections(request):
    if request.user.is_authenticated:
        return UserCollections.objects.filter(user=request.user).all()

    if not request.session.session_key:
        request.session.create()

    return UserCollections.objects.filter(session_key=request.session.session_key)
