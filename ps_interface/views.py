from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.template import loader


def index(request):
    return render(request, "index.html")


class PermissionDeniedView(TemplateView):

    template_name = "403_error.html"
    error_code = "403"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "error_code": self.error_code,
                "error_msg": "You have no permission to view the page.",
            }
        )
        return context

    def get(self, request, exception, *args, **kwargs):
        context = self.get_context_data()
        template = loader.get_template(self.template_name)
        return HttpResponseForbidden(template.render(request=request, context=context))


class PageNotFoundView(TemplateView):

    template_name = "404_error.html"
    error_code = "404"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "error_code": self.error_code,
                "error_msg": "Page not found.",
            }
        )
        return context

    def get(self, request, exception, *args, **kwargs):
        context = self.get_context_data()
        template = loader.get_template(self.template_name)
        return HttpResponseNotFound(template.render(request=request, context=context))
