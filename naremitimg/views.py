from .naremitimg import NaremitIMG

def img(request):
    ni = NaremitIMG(request.GET)
    return ni.response()