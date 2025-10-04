from django.shortcuts import render
from django.http import JsonResponse
from .models import EnergyData
import random
from datetime import date, timedelta
from django.shortcuts import render
from .models import EnergyData
import random
from datetime import date
from .forms import EnergyDataForm
from django.shortcuts import render, redirect
from .models import EnergyData
from .forms import EnergyDataForm
from django.utils.timezone import now
from django.db.models import Avg

def generate_data():
    """Simulate random energy and CO2 data for the last 7 days"""
    EnergyData.objects.all().delete()
    for i in range(7):
        energy = random.uniform(100, 500)  # in kWh
        co2 = energy * 0.4
        EnergyData.objects.create(
            date=date.today() - timedelta(days=(6 - i)),
            energy_used=energy,
            co2_emission=co2
        )

def dashboard(request):
    if EnergyData.objects.count() == 0:
        generate_data()
    return render(request, "dashboard.html")

def get_data(request):
    data = EnergyData.objects.order_by("date")
    labels = [d.date.strftime("%Y-%m-%d") for d in data]
    emissions = [round(d.co2_emission, 2) for d in data]
    total = sum(emissions)
    target = 2000  # target emission limit (example)
    progress = (total / target) * 100

    return JsonResponse({
        "labels": labels,
        "emissions": emissions,
        "progress": progress,
        "total": total
    })


# Create your views here.
def dashboard(request):
    if request.method == "POST":
        form = EnergyDataForm(request.POST)
        if form.is_valid():
            steps = form.cleaned_data['steps']

            # Convert steps → energy (kWh)
            # Example: assume 100 steps save 0.01 kWh
            energy_consumed = steps * 0.0001  # kWh
            emission = energy_consumed * 0.4  # 0.4 kg CO₂ per kWh

            EnergyData.objects.create(
                steps=steps,
                energy_consumed=energy_consumed,
                emission=emission
            )
            return redirect("dashboard")
    else:
        form = EnergyDataForm()

    today = now().date()
    today_emissions = EnergyData.objects.filter(date=today).aggregate(avg=Avg("emission"))["avg"] or 0
    avg_emission = EnergyData.objects.aggregate(avg=Avg("emission"))["avg"] or 0

    # Pass latest data to template
    context = {
        "form": form,
        "today_emission": round(today_emissions, 2),
        "avg_emission": round(avg_emission, 2),
        "target_reduction": -20,  # example fixed target
        "history": EnergyData.objects.all().order_by("date"),
    }
    return render(request, "dashboard.html", context)