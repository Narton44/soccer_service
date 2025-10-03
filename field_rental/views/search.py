from django.db.models import Q
from django.db.models.functions import Upper, Lower
from django.views.generic import ListView
from field_rental.models import Fields


class SearchView(ListView):
    model = Fields
    template_name = "index.html"
    context_object_name = "fields"

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            # Экранируем специальные символы regex
            import re
            escaped_query = re.escape(query)
            return Fields.objects.filter(adress__iregex=escaped_query)
        return Fields.objects.all()
        