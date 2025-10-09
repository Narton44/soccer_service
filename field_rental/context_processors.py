from .models import Cover, IndoorSign

def category_field(request):
    return {'categories': Cover.objects.all()}

def category_sign_field(request):
    return {'signcategories': IndoorSign.objects.all()}