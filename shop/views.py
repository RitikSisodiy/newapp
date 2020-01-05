
from django.shortcuts import render,redirect
from .models import Product,order,OrderUpdate
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from math import ceil
import ast,json
from django.views.decorators.csrf import csrf_exempt
from paytm import Checksum 
MERCHANT_KEY = 'aaT1Xj@F_oEnHA2m'

def index(request):
	
	allprod=[]
	catprod=Product.objects.values('category')
	cats={item['category'] for item in catprod}
	for cat in cats:
			prod=Product.objects.filter(category=cat)
			n=len(prod)
			nslide=n//4 + ceil((n/4)-(n//4))
			print(nslide)
			allprod.append([prod,range(0,nslide),nslide])
	
	#params={'no_of_slides':nslide, 'range':range(0,nslide), 'product':products}
	params={'allprod':allprod}
	return render(request, 'shop/index.html', params)

def about(request):
    return render(request, 'shop/about.html', {})

def contact(request):
    return render(request, 'shop/contact.html', {})

def tracker(request):
    return HttpResponse("We are at tracker")

def search(request):
    return HttpResponse("We are at search")

def productView(request,myid):
	prod=Product.objects.filter(id=myid)
	myprod={'product':prod}
	print(prod)
	return render(request, 'shop/product.html', myprod)

def checkout(request):
	if request.method=="POST":
		jsonitem=request.POST['jsonitem']
		fname=request.POST['fname']
		lname=request.POST['lname']
		email=request.POST['email']
		address1=request.POST['address1']
		address2=request.POST['address2']
		city=request.POST['city']
		state=request.POST['state']
		zip_code=request.POST['zip_code']
		prod= json.loads(jsonitem)
		sum=0
		for item in prod:
				print("product: ",item, "qty:-",prod[item][0])
				item=item[2:]
				print("product: ",item)
				prize=Product.objects.filter(id=item)
				p=int(prize[0].price) * int(prod['pr'+item][0])
				sum=sum+p
		ammount1=sum
		Order=order(json_item=jsonitem, fname=fname,ammount=ammount1, lname=lname, email=email,address1=address1,address2=address2, city=city,state=state,zipcode=zip_code)
		Order.save()
		update = OrderUpdate(order_id=Order.order_id, update_desc="The order has been placed")
		update.save()
		thank=True
		#id=Order.order_id
		#return render(request, 'shop/checkout.html',{'thank':thank,'orderid':id})
		param_dict = {
            'MID':'bEtzWe72963291709602',
            'ORDER_ID': str(Order.order_id),
            'TXN_AMOUNT':str(ammount1),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/shop/hendlerequest/',}
		param_dict['CHECKSUMHASH']=Checksum.generate_checksum(param_dict,MERCHANT_KEY)   	
		return render(request,'shop/paytm.html', {'param_dict':param_dict })


#	jsonitem=request.GET.get('jsonitem')
#	prod=json.loads(jsonitem)
#	plist=[]
#	for p in prod:
#		a=int(p[1])
#		q=int(p[0])
#		b=Product.objects.filter(id=a)
#		plist.append(b)
#	print("plist",plist)
#	params={'prizes':plist}
##requset to paytm to transvet=r the ammount to your account by user
	return render(request, 'shop/checkout.html',{})

def signup(request):
	if request.method=='POST':
		username=request.POST['name']
		email=request.POST['email']
		phone=request.POST['phone']
		pass1=request.POST['password']
		fname=request.POST['fname']
		lname=request.POST['lname']

		myuser = User.objects.create_user(username,email,pass1)
		myuser.phone= phone
		myuser.first_name= fname
		myuser.last_name= lname
		myuser.save()
		messages.success(request,"your shoppercart account is successfully created")
		return redirect('ShopHome')
	else:
		return HttpResponse("not found")

def login1(request):
	if request.method=='POST':
		name=request.POST['email']
		pass1=request.POST['pass']
		user = authenticate(username=name,password=pass1)

		if user is not None:
			login(request,user)
			messages.success(request,"your shoppercart account is successfully login")
			return redirect('ShopHome')
		else:
			messages.error(request,"your shoppercart account is not successfully login")
			return redirect('ShopHome')
		
	else:
		return HttpResponse("not found")
def logout1(request):
	logout(request)
	messages.success(request,"your shoppercart account is  successfully logout")
	return redirect('ShopHome')

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email1', '')
        try:
        	print("email",email)
        	print("id",orderId)
        	Order=order.objects.filter(order_id=orderId,email=email)
        	print(Order)
        	if len(Order)>0:
        		updates=[]
        		data=OrderUpdate.objects.filter(order_id=orderId)
        		for item in data:
        			updates.append({'text':item.update_desc,'date':item.timestamp})
        		responce=json.dumps(updates,default=str)
        		return HttpResponse(responce)
        	else:
        		return HttpResponse("{}")
        except Exception as e:
        	return HttpResponse("{}")
    return render(request,'shop/tracker.html')

@csrf_exempt
def hendlerequest(request):
 #paytm will send payment reques
 #paytm will send payment reques
	form = request.POST
	response_dict= {}
	for i in form.keys():
		response_dict[i]=form[i]
		if i == 'CHECKSUMHASH':
			checksum = form[i]
	print("res:====",response_dict)
	verify = Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
	if verify:
		if response_dict['RESPCODE'] == '01':
			print('order successful')
		else:
			try:
				Order=order.objects.get(order_id=int(response_dict['ORDERID']))
				update=OrderUpdate.objects.filter(order_id=int(response_dict['ORDERID']))
				Order.delete()
				update.delete()
				print('order unsuccessfull because',response_dict['RESPMSG'])
			except Exception as e:
				pass	
	else:
		print("order unsuccessful because",response_dict['RESPMSG'])
	return render(request,'shop/paymentstatus.html',{'response': response_dict})
