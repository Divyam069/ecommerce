from django.contrib import admin
from .models import CategoryModel,ProductModel,Register,Cartmodel,OrderModel
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['categoryName','categoryImage']
admin.site.register(CategoryModel,CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['category','productName','productPrice','productImage']
admin.site.register(ProductModel,ProductAdmin)

admin.site.register(Register)
class CartAdmin(admin.ModelAdmin):
    list_display = ['orderId','userId','productId','quantity','price','totalprice']
admin.site.register(Cartmodel,CartAdmin)

admin.site.register(OrderModel)



admin.site.site_header = 'My Ecommerce'                    # default: "Django Administration"
admin.site.index_title = 'product area'                 # default: "Site administration"
admin.site.site_title = 'My Ecommerce adminsitration'