# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic import TemplateView
#
#
# class ManagerDashboardView(
#     # LoginRequiredMixin,
#     TemplateView):
#     template_name = "users/dashboard.html"
#
#     def get_context_data(self, **kwargs):
#         ctx = super().get_context_data(**kwargs)
#         ctx["hotels"] = get_hotels_for_manager(self.request.user)
#         ctx["issues"] = get_issues_for_manager(self.request.user)
#         return ctx
