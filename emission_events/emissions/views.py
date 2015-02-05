import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from models import RegulatedEntity, EmissionEvent, ContaminantReleased, IssuedOrder

# validate len(q) > 2

def home_view(request):
    emission_events = EmissionEvent.emissions.filter(began_date__lte=datetime.date.today()).order_by('-began_date')[0:6]
    contaminants = ContaminantReleased.objects.distinct('tracking_number').all()[0:10]
    issued_orders = IssuedOrder.objects.order_by('-agended_at')[0:10]
    regulated_entities = RegulatedEntity.ranked.ranking_per_year()
    emissions_per_year = [
        EmissionEvent.emissions.emissions_per_year(2008),
        EmissionEvent.emissions.emissions_per_year(2009),
        EmissionEvent.emissions.emissions_per_year(2010),
        EmissionEvent.emissions.emissions_per_year(2011),
        EmissionEvent.emissions.emissions_per_year(2012),
        EmissionEvent.emissions.emissions_per_year(2013),
        EmissionEvent.emissions.emissions_per_year(2014),
        EmissionEvent.emissions.emissions_per_year(2015)
    ]
    emissions_per_year_and_month = EmissionEvent.emissions.emissions_per_year_and_month()

    return render(request, 'home.html', {
        'emission_events': emission_events,
        'contaminants': contaminants,
        'issued_orders': issued_orders,
        'regulated_entities': regulated_entities,
        'emissions_per_year': emissions_per_year,
        'emissions_count': emissions_per_year_and_month
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
