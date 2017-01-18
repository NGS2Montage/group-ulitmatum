from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def game(request):
    context = {}
    # fill in context dict with stuff to pass to template as needed
    return render(request, 'publicgoods.html', context)


@login_required
def waiting_room(request):
    context = {}
    # fill in context dict with stuff to pass to template as needed
    return render(request, 'publicgoods_waiting.html', context)
