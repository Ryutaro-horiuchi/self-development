from django.shortcuts import render
from django.utils import timezone

def time_test(request):
  now = timezone.now()
  print(now)
  return render(request, 'timezone.html', {'value': now})