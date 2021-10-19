from django.shortcuts import redirect

def redirect_ (request):
    response = redirect('/project_allocation/')
    return response