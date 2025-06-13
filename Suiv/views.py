from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required

def home_view(request):
    if request.user.is_authenticated:
        return redirect('/admin/')  # Redirige vers /admin/ si l'utilisateur est connecté
    return render(request, 'index.html')

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def print_view(request, object_id):
    # Remplacez cette logique par ce que vous voulez afficher pour l'impression
    # par exemple, récupérer un modèle ou une page spécifique
    context = {'object': some_model_object}  # Assurez-vous de définir le bon objet
    html = render_to_string('print_template.html', context)
    response = HttpResponse(html)
    response['Content-Type'] = 'application/pdf'  # Par exemple, pour imprimer en PDF
    response['Content-Disposition'] = 'inline; filename="page_a_imprimer.pdf"'
    return response

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Suiv.models import Enseignant

def print_enseignants_view(request):
    enseignants = Enseignant.objects.all().order_by('user__last_name')
    paginator = Paginator(enseignants, 10)  # 10 enseignants par page

    page = request.GET.get('page')
    try:
        enseignants_page = paginator.page(page)
    except PageNotAnInteger:
        enseignants_page = paginator.page(1)
    except EmptyPage:
        enseignants_page = paginator.page(paginator.num_pages)

    context = {'enseignants_page': enseignants_page}
    return render(request, 'admin/Suiv/enseignant/print_paginated.html', context)


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Notification

from django.shortcuts import redirect

@staff_member_required
def mark_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.read = True
    notification.save()
    return redirect('/admin/notifications/')  # Redirige vers la page des notifications
