from django.shortcuts import render

<<<<<<< HEAD

def home(request):
    return render(request, 'blog/home.html', {
        'title': 'Hello Djangoblog'
    })

def about(request):
    return render(request, 'blog/about.html', {
        'content': 'This is the Djangoblog team.'
    })
def contact(request):
    return render(request, 'contact.html', {
        'content': 'This is the Djangoblog team.'
    })
=======
# Create your views here.
>>>>>>> dde8b07d1c247207e20b19dc852af07e613d2cd4
