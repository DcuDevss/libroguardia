# comisarias/middleware.py

from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta

class NoCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

class RedirectAuthenticatedUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        restricted_urls = ['/', '/login/', '/no-permission/']
        if request.user.is_authenticated and request.path in restricted_urls:
            if request.user.groups.filter(name='comisariaprimera').exists():
                return redirect('comisaria_primera_list')
            elif request.user.groups.filter(name='comisariasegunda').exists():
                return redirect('comisaria_segunda_list')
            else:
                return redirect('no_permission')
        return None

class InactivityLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity:
                last_activity = timezone.datetime.fromisoformat(last_activity)
                if timezone.now() - last_activity > timedelta(hours=2):
                    from django.contrib.auth import logout
                    logout(request)
                    return redirect('login')

            request.session['last_activity'] = timezone.now().isoformat()
