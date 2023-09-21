from django.shortcuts import render
from . models import ShippingAddress, Order, OrderItem

from cart.cart import Cart

from django.http import JsonResponse

from django.core.mail import send_mail

from django.conf import settings

# Create your views here.

def checkout(request):

    # users with accounts -- pre-fill the form

    if request.user.is_authenticated:

        try:
            #authenticated users with shipping information
            shipping_address = ShippingAddress.objects.get(user=request.user.id)
            context = {'shipping': shipping_address}

            return render(request, 'payment/checkout.html', context=context)
        
        except:

            #authenticated uers with no shipping information

            return render(request, 'payment/checkout.html')


    else:
    
     # guest users

      return render(request, 'payment/checkout.html')
    





def payment_success(request):

    # clear shopping cart

    for key in list(request.session.keys()):

        if key == 'session_key':

            del request.session[key]

    return render(request, 'payment/payment-success.html')


def payment_failed(request):

    return render(request, 'payment/payment-failed.html')


def complete_order(request):

    if request.POST.get('action') == 'post':

        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')

        city = request.POST.get('city')

        zipcode = request.POST.get('zipcode')

        state = request.POST.get('state')

        shipping_address = (address +"\n" + zipcode + "\n" + state + "\n" + city)

        #shopping cart information

        cart = Cart(request)

        total_cost = cart.get_total()

        '''
            Order variations
            1) Create order -> account users WITH + WITHOUT shipping info
            2) create order -> guest users without account
        
        '''
        #  1) Create order -> account users WITH + WITHOUT shipping info

        if request.user.is_authenticated:

            order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address, 
                                         
                amount_paid=total_cost, user=request.user)
            
            order_id = order.pk

            for item in cart:

                OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'], price=item['price'], user=request.user)

                send_mail('Order received', 'Hey, ' + '\n' + 'Danke für Ihre Bestellung' + str(all_products) + '\n' + 'Gesamtsumme: €' + 
                
                    str(cart.get_total()), settings.EMAIL_HOST_USER, [email] , failed_silently=False)

       #  2) create order -> guest users without account


        else:
           

                order = Order.objects.create(full_name=name, email=email, shipping_address=shipping_address, 
                                         
                amount_paid=total_cost)
            
                order_id = order.pk

                product_list = []

                for item in cart:

                    OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'], price=item['price'])

                    product_list.append(item['product'])

                all_products = product_list

                #email order

                send_mail('Order received', 'Hey, ' + '\n' + 'Danke für Ihre Bestellung' + str(all_products) + '\n' + 'Gesamtsumme: €' + 
                
                    str(cart.get_total()), settings.EMAIL_HOST_USER, [email] , failed_silently=False)

        order_success = True

        response = JsonResponse({'success':order_success})   

        return response       







