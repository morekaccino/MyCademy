from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request=request, template_name='homepage/index.html', context={})
