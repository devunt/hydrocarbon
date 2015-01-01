from board.utils import UrlHelper


def current_url(request):
    full_path = request.get_full_path()
    return dict(current_url=UrlHelper(full_path))
