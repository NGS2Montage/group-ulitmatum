from django.contrib.auth.decorators import login_required

from annoying.decorators import render_to


@render_to('state-mismatch.html')
@login_required
def state_mismatch(request):
    context = {}
    # fill in context dict with stuff to pass to template as needed
    return context
