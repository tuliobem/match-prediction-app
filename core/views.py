from django.shortcuts import render, get_object_or_404
from core.models import Fixture, Prediction
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST 
from django.http import HttpResponse
from render_block import render_block_to_string

# Create your views here.
@login_required
def index(request):
    fixtures = Fixture.objects.all()
    predictions = [f.predictions.filter(user=request.user).first() for f in fixtures]
    context = {
        'fixtures_and_predictions': zip(fixtures, predictions),
    }
    return render(request, 'index.html', context)

@login_required
@require_POST
def submit_prediction(request, fixture_pk):
    fixture = get_object_or_404(Fixture, pk=fixture_pk) 
    home_goals = int(request. POST.get('home_goals')) 
    away_goals = int(request.POST.get('away_goals'))

    prediction = Prediction.objects.filter(fixture=fixture, user=request.user).first()
    if prediction: 
        prediction.home_goals = home_goals
        prediction.away_goals = away_goals
        prediction.save()
    else:
        prediction = Prediction.objects.create(
            user=request.user, 
            fixture=fixture,
            home_goals=home_goals, 
            away_goals=away_goals
        )

    context = { 
        'prediction': prediction, 'fixture': fixture
    } 
    html = render_block_to_string('index.html', 'fixture-container', context)
    return HttpResponse(html)

@login_required
@require_POST
def delete_prediction (request, prediction_pk): 
    prediction = get_object_or_404(Prediction, pk=prediction_pk)
    fixture = prediction.fixture
    prediction.delete() 
    context = {'prediction': None, 'fixture': fixture}
    
    html = render_block_to_string('index.html', 'fixture-container', context)
    return HttpResponse(html)
