from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def game_initial(request):
    context = {}
    # fill in context dict with stuff to pass to template as needed
    return render(request, 'groupultimatum_initial.html', context)


@login_required
def game_voting(request):
    context = {}
    # fill in context dict with stuff to pass to template as needed
    return render(request, 'groupultimatum_voting.html', context)


@login_required
def game_final(request):
    context = {}
    # fill in context dict with stuff to pass to template as needed
    return render(request, 'groupultimatum_final.html', context)


@login_required
def waiting_room(request):
    context = {}
    # fill in context dict with stuff to pass to template as needed
    return render(request, 'groupultimatum_waiting.html', context)
