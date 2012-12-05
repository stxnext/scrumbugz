from django.views.generic import View
from django.http import HttpResponse

from scrum.tasks import update_products

class HardRefreshView(View):
    def get(self, request, *args, **kwargs):
        update_products.delay()
        return HttpResponse('ok')

