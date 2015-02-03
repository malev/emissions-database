import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from models import RegulatedEntity, EmissionEvent, ContaminantReleased, IssuedOrder

# validate len(q) > 2

def home_view(request):
    emission_events = EmissionEvent.emissions.filter(began_date__lte=datetime.date.today()).order_by('-began_date')[0:6]
    contaminants = ContaminantReleased.objects.all()[0:6]
    issued_orders = IssuedOrder.objects.order_by('-agended_at')[0:6]
    regulated_entities = RegulatedEntity.ranked.ranking_per_year()

    print len(regulated_entities)
    print regulated_entities[0]

    return render(request, 'home.html', {
        'emission_events': emission_events,
        'contaminants': contaminants,
        'issued_orders': issued_orders,
        'regulated_entities': regulated_entities
    })


def search_view(request):
    regulated_entities = RegulatedEntity.objects.filter(\
        Q(name__icontains=request.GET['q']) |\
        Q(county__icontains=request.GET['q']) |\
        Q(nearest_city__icontains=request.GET['q']) |\
        Q(regulated_entity_rn_number__icontains=request.GET['q']))

    return render(request, 'search.html', {
        'q': request.GET['q'],
        'regulated_entities': regulated_entities
    })


def regulated_entity_view(request, pk):
    regulated_entity = get_object_or_404(RegulatedEntity, pk=pk)

    return render(request, 'regulated_entity.html', {
        'regulated_entity': regulated_entity
    })


def county_view(request, county_name):
    regulated_entities = RegulatedEntity.objects.filter(county=county_name).order_by('name')
    emission_events = EmissionEvent.objects.filter(county=county_name.upper()).order_by('-tracking_number')
    paginator = Paginator(emission_events, 25)

    page = request.GET.get('page')
    try:
        emissions = paginator.page(page)
    except PageNotAnInteger:
        emissions = paginator.page(1)
    except EmptyPage:
        emissions = paginator.page(paginator.num_pages)

    return render(request, 'county.html', {
        'regulated_entities': regulated_entities,
        'emission_events': emissions
    })
