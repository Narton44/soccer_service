from .models import Cover

def category_field(request):
    return {'categories': Cover.objects.all()}