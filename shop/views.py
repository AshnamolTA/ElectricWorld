from django.shortcuts import render,redirect,get_object_or_404

# from django.forms import BaseModelForm

# from django.http import HttpResponse

from django.urls import reverse_lazy

from django.views.generic import View,FormView,TemplateView,DetailView

from django.contrib.auth import authenticate,login,logout

from shop.forms import SignUpForm,SignInForm,UserProfileForm,OrderForm


from shop import views

from shop.models import Light,UserProfile,Category,WishListItem,Shape,WishList,LightColour,LightBodyColour,Order,OrderItem


class SignUpView(View):

    template_name="signup.html"

    form_class=SignUpForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            print("Account Created")

            return redirect("signin")
        
        else:

            print("Failed To Create Account")
            
            
            return render(request,"login.html",{"form":form_instance})

        

class SignInView(FormView):

    template_name="login.html"

    form_class=SignInForm

    def post(self,request,*args,**kwargs):
        
        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            uname=form_instance.cleaned_data.get("username")

            pwd=form_instance.cleaned_data.get("password")

            user_object=authenticate(username=uname,password=pwd)

            if user_object:

                login(request,user_object)

                return redirect("index")
            
        return render(request,self.template_name,{"form":form_instance})
    
class LogoutView(View):

    def get(self,request,*arga,**kwargs):
         
         logout(request)

         return redirect("signin")
    


class UserProfileEditView(View):

    template_name="profile_edit.html"

    form_class=UserProfileForm

    def get(self,request,*args,**kwargs):

        user_profile_instance=request.user.profile

        form_instance=self.form_class(instance=user_profile_instance)

        return render(request,self.template_name,{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        user_profile_instance=request.user.profile

        form_instance=self.form_class(request.POST,instance=user_profile_instance,files=request.FILES)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("index")

        return render(request,self.template_name,{"form":form_instance})
    
        
class IndexView(TemplateView):

    template_name="index.html"

    def get(self,request,*args,**kwargs):

        qs=Category.objects.all()

        return render(request,self.template_name,{"data":qs})



class CategoryDetailView(TemplateView):

    template_name="category_light.html"

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=Category.objects.get(id=id)
        light=qs.light_set.all()

        return render(request,self.template_name,{"category":qs,"light":light})
    

            


# class LightListView(TemplateView):

#     template_name="light.html"

#     def get(self,request,*args,**kwargs):

#         id=kwargs.get("pk")

#         qs=Light.objects.all()

#         return render(request,self.template_name,{"light":qs})
    
class LightDetailView(View):

    template_name="light_detail.html"

    def get(self,request,*args,**kwargs):
        

        id=kwargs.get("pk")

        
        qs=Light.objects.get(id=id)

        return render(request,self.template_name,{"data":qs})
    





class AddToWishlistItemView(View):

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        light_obj=Light.objects.get(id=id)


        shape_name=request.POST.get("name")
        print(shape_name)
        shape_obj=Shape.objects.get(name=shape_name)

        colour_name=request.POST.get("colour")
        colour_obj=LightColour.objects.get(colour=colour_name)

        body_name=request.POST.get("body")
        body_obj=LightBodyColour.objects.get(bodycolour=body_name)

        quantity=request.POST.get("quantity")



        basket_obj=request.user.basket

        WishListItem.objects.create(
            wishlist_object=basket_obj,
            light_object=light_obj,
            shape_object=shape_obj,
            colour_object=colour_obj,
            body_object=body_obj,
            quantity=quantity
            

        )
        
        
        print("item add to wishlist")

        return redirect("index")
    

class WishlistItemListView(View):

    def get(self,request,*args,**kwargs):

        qs=request.user.basket.basket_item.filter(is_order_placed=False)

        wishlist_item_count=qs.count()


        wishlist_total=sum([wi.item_total for wi in qs])

        return render(request,"my_wishlist.html",{"data":qs,"wishlisttotal":wishlist_total,"wishlistitem_count":wishlist_item_count})
    

class WishlistItemDeleteView(View):

    def get(self,request,*args,**kwargs):

        wishlist_item_object=WishListItem.objects.get(id=kwargs.get('pk'))

        wishlist_item_object.delete()

        return redirect('my_wishlist')
    
class PlaceOrderView(View):

    template_name="place_order.html"

    form_class=OrderForm

    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        qs=request.user.basket.basket_item.filter(is_order_placed=False)

        total=sum([bi.item_total  for bi in qs])


        return render(request,self.template_name,{"form":form_instance,"items":qs,"total":total})
    
    def post(self,request,*args,**kwargs):

        form_instance=self.form_class(request.POST)

        if form_instance.is_valid():

            form_instance.instance.customer=request.user

            order_instance=form_instance.save()

            #adding orderitems

            basket_item=request.user.basket.basket_item.filter(is_order_placed=False)

            for bi in basket_item:

                OrderItem.objects.create(
                    order_object=order_instance,
                    light_object=bi.light_object,
                    quantity=bi.quantity,
                    shape_object=bi.shape_object,
                    colour_object=bi.colour_object,
                    body_object=bi.body_object,
                    price=bi.light_object.price,

                    
                )

                bi.is_order_placed=True
                bi.save()

        return redirect("index")
    
class OrderSummeryView(View):

    template_name="order_summery.html"

    def get(self,request,*args,**kwargs):
        qs=request.user.orders.all()
        return render(request,self.template_name,{"orders":qs})

