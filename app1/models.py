from django.db import models

# Create your models here.

class CategoryModel(models.Model):
    categoryName = models.CharField(max_length=100)
    categoryImage = models.ImageField(upload_to='category')

    def __str__(self) -> str:
        return self.categoryName

class ProductModel(models.Model):
    category = models.ForeignKey(CategoryModel,on_delete=models.CASCADE)
    productName = models.CharField(max_length=100)
    productPrice = models.IntegerField(max_length=5,default=0)
    productDescription = models.TextField(default="")
    productImage = models.ImageField(upload_to='product')

    def __str__(self) -> str:
        return self.productName

class Register(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField()
    contact=models.PositiveIntegerField()
    password=models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Cartmodel(models.Model):
    orderId=models.CharField(max_length=200)
    userId=models.CharField(max_length=200)
    productId=models.CharField(max_length=200)
    quantity=models.CharField(max_length=200)
    price=models.CharField(max_length=200)
    totalprice=models.CharField(max_length=200)

    def __str__(self):
        return self.orderId

class OrderModel(models.Model):
    userId = models.CharField(max_length=20)
    userName = models.CharField(max_length=100)
    userEmail = models.CharField(max_length=100)
    userContact = models.BigIntegerField()
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.BigIntegerField()
    orderAmount = models.CharField(max_length=50)
    paymentVia = models.CharField(max_length=50 ,default="")
    paymentMethod = models.CharField(default=None,max_length=50)
    transactionId = models.TextField(default=None)
    orderDate = models.DateTimeField(auto_created=True,auto_now=True)
    
    def __str__(self) -> str:
        orderId = self.pk
        return str(orderId)