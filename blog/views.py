from django.shortcuts import render


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
