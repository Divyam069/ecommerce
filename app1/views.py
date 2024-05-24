from django.shortcuts import render,redirect
from .models import CategoryModel,ProductModel,Register,Cartmodel,OrderModel
from .forms import UserRegisterForm
from django.db.models import Q
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


# Create your views here.
def productNavView():
    productData = ProductModel.objects.all()
    return productData

def sessionDataView(request):
    email_1 = request.session['user']    
    dictData = {'email':email_1}
    return dictData

def CategoryView(request):  
    if 'user' in request.session:
        categoryData = CategoryModel.objects.all()
        sessionDataView1=sessionDataView(request)
        productNavData = productNavView()
        return render(request,'index.html',{'categoryKey':categoryData,'productAllKey':productNavData,'sessionDataView1':sessionDataView1})
    else:
        categoryData = CategoryModel.objects.all()
        productNavData = productNavView()
        return render(request,'index.html',{'categoryKey':categoryData,'productAllKey':productNavData})

# def register(request):
#     if request.method=='POST':
#         model=Register()
#         model.name=request.POST['name']
#         model.email=request.POST['username']
#         model.contact=request.POST['contact']
#         model.password=request.POST['password']
#         model.save()
#         return redirect('Category')
#     return render(request,'register.html')

def register(request):
    obj=UserRegisterForm(request.POST) 
    if obj.is_valid():
        data=Register.objects.all().filter(email=request.POST['email'])
        if len(data)<=0:
            obj.save()
            return redirect('Category')
        else:
            return render(request,'register.html',{'message':'alredy exist'})
    return render(request,'register.html')

def login(request):
    if request.POST:
        email_1=request.POST['email']
        password_1=request.POST['password']
        try:
            data=Register.objects.get(email=email_1,password=password_1) 
            if data:
                request.session['user'] = email_1
                request.session['userId']=data.pk
                print(request.session['user'])
                return redirect('Category')
        except:
            return redirect('login')
        # print(email,password)
    return render(request,'login.html')
def logout(request):
    if 'user' in request.session:
        del request.session['user']
        return redirect('Category')
    return redirect('login')

def productall(request):
    if 'user' in request.session:
        sessionDataView1=sessionDataView(request)
        a=ProductModel.objects.all()
        return render(request,'productall.html',{'a':a,'sessionDataView1':sessionDataView1})
    else:
        return redirect('login')

def productcatwise(request,id):
    if 'user' in request.session:
        sessionDataView1=sessionDataView(request)
        a=ProductModel.objects.filter(category=id)
        return render(request,'productall.html',{'a':a,'sessionDataView1':sessionDataView1})
    else:
        return redirect('login')

def profile(request):
    if 'user' in request.session:
        data=Register.objects.get(email=request.session['user'])
        print(data)
        if request.method=='POST':
            data.name=request.POST['name']
            data.password=request.POST['password']
            data.save()
        return render(request,'profile.html',{'abc':data})
    else:
        return redirect('login')


def productdetailes(request,id):
    if 'user' in request.session:
        sessionDataView1=sessionDataView(request)
        a=ProductModel.objects.get(pk=id)
        if request.POST:
            model=Cartmodel()
            model.orderId="0"
            model.userId=request.session['userId']
            model.productId=id
            model.quantity="5"
            model.price=a.productPrice
            model.totalprice=str(int(model.quantity)*a.productPrice)
            model.save()
        return render(request,'productdetails.html',{'abc':a,'sessionDataView1':sessionDataView1})
    else:
        return redirect('login')

def cart(request):
    if 'user' in request.session:
        sessionDataView1=sessionDataView(request)
        cartdata=Cartmodel.objects.filter(userId=request.session['userId']) & Cartmodel.objects.filter(orderId="0")
        totalamt=0
        cartlist=[]
        for i in cartdata:
            pk_id=i.pk
            totalamt+=int(i.totalprice)
            producttotalprice=i.totalprice
            productdata=ProductModel.objects.get(pk=i.productId)
            productimage=productdata.productImage
            productname=productdata.productName
            productquantity=i.quantity
            productprice=productdata.productPrice
            cartdict={'id':pk_id,'productquantity':productquantity,'productimage':productimage,'productname':productname,'productprice':productprice,'producttotalprice':producttotalprice}
            cartlist.append(cartdict)
        print(cartdata,len(cartdata),totalamt)
        
        return render(request,'cart.html',{'sessionDataView1':sessionDataView1,'cart':cartdata,'noitem':len(cartlist),'cartlist':cartlist,'totalamt':totalamt,})
    else:
        return redirect('login')
def delete_cartitem(request,id):
    if 'user' in request.session:
        a=Cartmodel.objects.filter(id=id)
        a.delete()
        return redirect('cart')
    else:
        return redirect('login') 

def orderSuccessView(request):
    if 'user' in request.session:
        sessionDataView1=sessionDataView(request)
        return render(request,'order_sucess.html',{'sessionDataView1':sessionDataView1})
    else:
        return redirect('login')

def MyorderView(request):
    if 'user' in request.session:
        sessionDataView1=sessionDataView(request)
        if request.method == 'POST':
            request.session['orderId'] = request.POST['orderId']
            print("Order Id : ",request.POST['orderId'])
            return redirect('MyorderdetaislView')
        else:
            orderdata=OrderModel.objects.filter(userId=request.session['userId']).order_by('-id')
            return render(request,'myorder.html',{'sessionDataView1':sessionDataView1,'orderdata':orderdata})
    else:
        return redirect('login')

def MyorderdetaislView(request):
    if 'user' in request.session:
        sessionDataView1=sessionDataView(request)
        orderIdValue = request.session['orderId']
        orderData = OrderModel.objects.get(id=orderIdValue)
        addressData = orderData.address+","+orderData.city+","+orderData.state+","+str(orderData.pincode)
        orderDict = {
            "name":orderData.userName,
            "contact":orderData.userContact,
            "address":addressData,
            'orderAmount':orderData.orderAmount,
            'paymentVia':orderData.paymentVia,
            'paymentMethod':orderData.paymentMethod,
            'transactionId':orderData.transactionId
            }
        print(orderDict)
        cartQuery = Cartmodel.objects.filter(orderId=orderIdValue)
        cartDataArray = []
        for i in cartQuery:
            productNameQuery = ProductModel.objects.get(id=i.productId)
            cartDict = {
                'productId':i.productId,
                'productName':productNameQuery.productName,
                'productImage':productNameQuery.productImage.url,
                'qty':i.quantity,
                'price':i.price,
                'totalPrice':i.totalprice
                }
            cartDataArray.append(cartDict)
        

        return render(request,'orderdetails.html',{'sessionDataView1':sessionDataView1,'OrderDetailData':orderDict,'CartData':cartDataArray})
    else:
        return redirect('login')

def search(request):
    if 'user' in request.session:
        sessionDataView1=sessionDataView(request)
        query = request.GET.get('search')
        qset = query.split(' ')
        print(qset)
        for q in qset:
            b = ProductModel.objects.filter(Q(category__categoryName__icontains=q) | Q(
                productName__icontains=q) | Q(productPrice__icontains=q)).distinct()
        return render(request, 'productall.html', {'a': b,'sessionDataView1':sessionDataView1})
    else:
        return redirect('login')

def shiping(request):
    if 'user' in request.session:
        sessionDataView1=sessionDataView(request)
        data=Register.objects.get(email=request.session['user'])
        cartdata=Cartmodel.objects.filter(userId=request.session['userId']) & Cartmodel.objects.filter(orderId="0")
        sessionId=request.session['userId']
        totalamt=0
        for i in cartdata:
            totalamt+=int(i.totalprice)        
        razorpay_amount=totalamt*100
        if request.method == "POST":
            model=OrderModel()
            model.userId=request.session['userId']
            model.userName=request.POST['userName']
            model.userEmail=request.POST['userEmail']
            model.userContact=request.POST['userContact']
            model.address=request.POST['address']
            model.city=request.POST['city']
            model.state=request.POST['state']
            model.pincode=request.POST['pincode']
            model.orderAmount=request.POST['orderAmount']
            model.paymentVia = request.POST['paymentVia']
            if model.paymentVia=="Cash":
                model.paymentMethod = ""
                model.transactionId = ""
                model.save()
                orderId = OrderModel.objects.latest('id')
                for i in cartdata:
                    cartData = Cartmodel.objects.get(id=i.pk)
                    cartData.orderId = str(orderId)
                    cartData.save()
                return redirect('orderSuccessView')     
            else:
                request.session['shippingUserId'] = sessionId
                request.session['shippingName'] = request.POST['userName']
                request.session['shippingEmail'] = request.POST['userEmail']
                request.session['shippingContact'] = request.POST['userContact']
                request.session['shippingAddress'] = request.POST['address']
                request.session['shippingCity'] = request.POST['city']
                request.session['shippingState'] = request.POST['state']
                request.session['shippingPincode'] = request.POST['pincode']
                request.session['shippingOrderAmount'] = str(totalamt)
                request.session['shippingPaymentVia'] = "Online"
                request.session['shippingPaymentMethod'] = "Razorpay"
                request.session['shippingTransactionId'] = ""
                return redirect('razorpayView')                   
        return render(request,'shiping.html',{'abc':data,'totalamt':totalamt,'sessionDataView1':sessionDataView1,'razor':razorpay_amount})
    else:
        return redirect('login') 

RAZOR_KEY_ID = 'rzp_test_8iwTTjUECLclBG'
RAZOR_KEY_SECRET = '0q8iXqBL1vonQGVQn4hK1tYg'
client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))

def razorpayView(request):
    currency = 'INR'
    amount = int(request.session['shippingOrderAmount'])*100
    # Create a Razorpay Order
    razorpay_order = client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'http://127.0.0.1:8000/paymenthandler/'    
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url    
    return render(request,'razorpayDemo.html',context=context)
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = client.utility.verify_payment_signature(
                params_dict)
            
            amount = int(request.session['shippingOrderAmount'])*100  # Rs. 200
            # capture the payemt
            client.payment.capture(payment_id, amount)

            #Order Save Code
            orderModel = OrderModel()
            orderModel.userId = request.session['shippingUserId']
            orderModel.userName = request.session['shippingName']
            orderModel.userEmail = request.session['shippingEmail']
            orderModel.userContact = request.session['shippingContact']
            orderModel.address = request.session['shippingAddress']
            orderModel.city = request.session['shippingCity']
            orderModel.state = request.session['shippingState']
            orderModel.pincode = request.session['shippingPincode']
            orderModel.orderAmount = request.session['shippingOrderAmount']
            orderModel.paymentVia = request.session['shippingPaymentVia']
            orderModel.paymentMethod = request.session['shippingPaymentMethod']
            orderModel.transactionId = payment_id
            orderModel.save()
            orderId = OrderModel.objects.latest('id')
        
            cartdata=Cartmodel.objects.filter(userId=request.session['userId']) & Cartmodel.objects.filter(orderId="0")
            for i in cartdata:
                cartData = Cartmodel.objects.get(id=i.pk)
                cartData.orderId = str(orderId)
                cartData.save()
            # render success page on successful caputre of payment
            return redirect('orderSuccessView')
        except:
            print("Hello")
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        print("Hello1")
       # if other than POST request is made.
        return HttpResponseBadRequest()