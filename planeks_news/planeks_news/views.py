from django.shortcuts import render
from django.conf import settings
import os

def home_view(request):
	with open(os.path.join(settings.BASE_DIR, 'welcome.txt'),
				mode='r',
				encoding="utf-8") as f:
		text = f.read()

	return render(request, 'home.html', context={'text': text})