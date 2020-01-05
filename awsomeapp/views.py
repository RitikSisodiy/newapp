from django.http import HttpResponse
from django.shortcuts import render
from math import ceil
def home(request):
	products=products.objects.all
	print(products)
	return render(request,'index.html',{})
	n=len(products)
	nslide = n//4 + ceil((n/4) - (n//4))
