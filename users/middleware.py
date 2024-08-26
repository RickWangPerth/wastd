from django.shortcuts import redirect
from django.urls import reverse

class TermsAndConditionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.has_agreed_to_terms:
            if request.path != reverse('users:terms_and_conditions'):
                return redirect(reverse('users:terms_and_conditions'))

        response = self.get_response(request)
        return response
