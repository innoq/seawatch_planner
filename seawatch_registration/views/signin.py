from django.shortcuts import redirect


def login_success(request):
    """ The admin has no profile that could be displayed """
    if not hasattr(request.user, 'profile'):
        return redirect('index')
    else:
        return redirect('registration_process')
