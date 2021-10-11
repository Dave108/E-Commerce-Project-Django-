from django.shortcuts import render, HttpResponseRedirect, reverse
from .forms import SignUpUsers, AdditionalDetails
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.files.storage import FileSystemStorage
from .models import CustomerInfo, Products, Kart, OrderPlaced, CheckoutAddress, Payment
from django.core.paginator import Paginator
from django.db.models import Q
import cloudinary
import datetime
from django.contrib import messages


# Create your views here.
def kart_items(request):
    if request.user.is_authenticated:
        all_items = Kart.objects.filter(user=request.user, is_deleted=False)
        return len(all_items)
    else:
        return 0


def homepage(request):
    products = Products.objects.all().order_by('id')
    paginator = Paginator(products, 3, orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # ----------------------
    items_in_kart = kart_items(request)  # calling function to get kart_total items
    # ----------------------
    # context items
    context = {
        "products": products,
        "page_obj": page_obj,
        "total_kart_items": items_in_kart,
    }
    return render(request, 'homepage.html', context)


def user_signup(request):
    if request.method == "POST":
        fm = SignUpUsers(request.POST)
        if fm.is_valid():
            fm.save()
            print("SUCCESS!!")
            fm = SignUpUsers()
            context = {
                "form": fm,
            }
            return render(request, 'signup.html', context)

    fm = SignUpUsers()
    context = {
        "form": fm,
    }
    return render(request, 'signup.html', context)


def user_login(request):
    if request.method == "POST":
        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                print(request.user, '------here')
                check = CustomerInfo.objects.filter(name=request.user).first()
                if check:
                    check_data = check.check_all_details()
                    print(check_data, '-------check')
                    if check_data:
                        messages.error(request, 'Welcome to MyShopE')
                        return HttpResponseRedirect(reverse('homepage'))  # reverse redirect
                    else:
                        messages.error(request, 'Add details first!')
                        return HttpResponseRedirect('/additionaldetails/')
                else:
                    print("else part")
                    messages.error(request, 'Add details first!')
                    return HttpResponseRedirect('/additionaldetails/')
    fm = AuthenticationForm()
    context = {
        "form": fm
    }
    return render(request, 'login.html', context)


def additional_details(request):
    if request.method == "POST":
        # image = request.FILES.get('image')
        image = cloudinary.uploader.upload(request.FILES['image'])

        print(image)
        gender = request.POST.get('gender')
        locality = request.POST.get('locality')
        pincode = request.POST.get('pincode')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        print(image, gender)
        if image is not None:
            # ----------------------------
            # fs = FileSystemStorage()
            # pic_obj = fs.save(image.name, image)
            # file_url = fs.url(pic_obj)
            # ----------------------------
            newuser = CustomerInfo.objects.create(
                name=request.user,
                gender=gender,
                user_image=image['url'],
                locality=locality,
                pincode=pincode,
                city=city,
                state=state,
                country=country,
            )
            messages.error(request, 'Welcome to MyShopE!')
            return HttpResponseRedirect(reverse('homepage'))
        else:
            newuser = CustomerInfo.objects.create(
                name=request.user,
                gender=gender,
                user_image="none",
                locality=locality,
                pincode=pincode,
                city=city,
                state=state,
                country=country,
            )
            messages.error(request, 'Welcome to MyShopE!')
            return HttpResponseRedirect(reverse('homepage'))
    fm = AdditionalDetails()
    context = {
        "form": fm
    }
    return render(request, 'additional_details.html', context)


def logout_user(request):
    logout(request)
    messages.error(request, 'Thanks for shopping with us ')
    return HttpResponseRedirect('/login/')


def search_items(request):
    print("-------", request.GET)
    search_obj = request.GET.get('q')
    # code for searching
    print(search_obj)
    search_result = Products.objects.filter(
        Q(name__icontains=search_obj) | Q(description__icontains=search_obj) | Q(label__icontains=search_obj))
    print(search_result)
    # ------------------------
    # paginating the search results
    paginator = Paginator(search_result, 3, orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # --------------
    items_in_kart = kart_items(request)  # calling function to get kart_total items
    # --------------
    # context items
    context = {
        "results": page_obj,
        "search_obj": search_obj,
        "total_kart_items": items_in_kart,
    }
    # ------------------------
    messages.error(request, 'You searched for! ' + ' " ' + search_obj + ' " ')
    return render(request, 'searchpage.html', context)


def view_product(request, slug):
    data = Products.objects.get(slug=slug)
    if request.user.is_authenticated:
        item = Kart.objects.filter(user=request.user, ordered=False, item=data, is_deleted=False).first()
    else:
        item = 0
    print(data.image.url, '------image')
    # -------------
    items_in_kart = kart_items(request)  # calling function to get kart_total items
    # -------------
    context = {
        "data": data,
        "kart": item,
        "total_kart_items": items_in_kart,
    }
    return render(request, 'productpage.html', context)


def add_kart(request, pk):
    if request.user.is_authenticated:
        data = Products.objects.get(id=pk)
        kart_data = Kart.objects.get_or_create(
            user=request.user,
            ordered=False,
            item=data,
            quantity=1,
        )
        messages.error(request, 'Added to cart')
        return HttpResponseRedirect(reverse("product", kwargs={"slug": data.slug}))
    else:
        messages.error(request, 'Login First!')
        return HttpResponseRedirect('/login/')


def remove_from_kart(request, pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = Products.objects.get(id=pk)
            item = Kart.objects.filter(user=request.user, ordered=False, item=data, is_deleted=False).first()
            if item:
                item.delete()
                messages.error(request, 'Item Removed')
            else:
                print("nothing in cart")
                messages.error(request, 'Nothing in cart')
            return HttpResponseRedirect(reverse("cart"))
        else:
            data = Products.objects.get(id=pk)
            item = Kart.objects.filter(user=request.user, ordered=False, item=data, is_deleted=False).first()
            if item:
                item.delete()
                messages.error(request, 'Item Removed')
            else:
                print("nothing in cart")
                messages.error(request, 'Nothing in cart')
            return HttpResponseRedirect(reverse("product", kwargs={"slug": data.slug}))
    else:
        messages.error(request, 'Login First!')
        return HttpResponseRedirect('/login/')


def increase_cart(request, pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = Products.objects.get(id=pk)
            item = Kart.objects.filter(user=request.user, ordered=False, item=data, is_deleted=False).first()
            if item:
                if item.quantity == 0:
                    pass
                else:
                    item.quantity = item.quantity + 1
                    item.save()
                    messages.error(request, 'Increased qunatity!')
            return HttpResponseRedirect(reverse("cart"))
        else:
            data = Products.objects.get(id=pk)
            item = Kart.objects.filter(user=request.user, ordered=False, item=data, is_deleted=False).first()
            if item:
                if item.quantity == 0:
                    pass
                else:
                    item.quantity = item.quantity + 1
                    item.save()
                    messages.error(request, 'Increased qunatity!')
            return HttpResponseRedirect(reverse("product", kwargs={"slug": data.slug}))
    else:
        messages.error(request, 'Login First!')
        return HttpResponseRedirect('/login/')


def decrease_cart(request, pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = Products.objects.get(id=pk)
            item = Kart.objects.filter(user=request.user, ordered=False, item=data, is_deleted=False).first()
            if item:
                if item.quantity == 1:
                    print("Can't remove anymore")
                elif item.quantity == 0:
                    print("Can't remove, 0 items in cart")
                else:
                    item.quantity = item.quantity - 1
                    item.save()
                    messages.error(request, 'Quantity Decreased!')
            return HttpResponseRedirect(reverse("cart"))
        else:
            data = Products.objects.get(id=pk)
            item = Kart.objects.filter(user=request.user, ordered=False, item=data, is_deleted=False).first()
            if item:
                if item.quantity == 1:
                    print("Can't remove anymore")
                elif item.quantity == 0:
                    print("Can't remove, 0 items in cart")
                else:
                    item.quantity = item.quantity - 1
                    item.save()
                    messages.error(request, 'Quantity Decreased!')
            return HttpResponseRedirect(reverse("product", kwargs={"slug": data.slug}))
    else:
        messages.error(request, 'Login First!')
        return HttpResponseRedirect('/login/')


def open_cart(request):
    if request.user.is_authenticated:
        # -------------
        karts = Kart.objects.filter(user=request.user, is_deleted=False)
        # -------------
        kart_list = []
        total_original_kart_price = 0
        total_kart_price = 0
        if karts:
            for kart in karts:
                total_item_price = kart.get_total_item_price()
                total_original_price = kart.get_total_original_price()
                dict = {'id': kart.item.id, 'name': kart.item.name, 'quantity': kart.quantity,
                        'description': kart.item.description,
                        'price': kart.item.price, 'discount_price': kart.item.discount_price,
                        'image': kart.item.image.url,
                        'label': kart.item.label, 'total_price': total_item_price,
                        'total_original_price': total_original_price,
                        'product_page_url': kart.item.get_product_url()}
                total_kart_price = total_kart_price + total_item_price
                total_original_kart_price = total_original_kart_price + total_original_price

                kart_list.append(dict)
                # print(dict)
        total_discount = total_original_kart_price - total_kart_price
        # -------------
        context = {
            "total_kart_items": len(karts),
            "discount": total_discount,
            "total_kart_price": total_kart_price,
            "total_original_kart_price": total_original_kart_price,
            "kart_list": sorted(kart_list, key=lambda i: i['id'], reverse=True),
        }
        return render(request, 'cartpage.html', context)
    else:
        messages.error(request, 'Login First!')
        return HttpResponseRedirect('/login/')


def open_checkout(request):
    if request.user.is_authenticated:
        # --------------
        karts = Kart.objects.filter(user=request.user, is_deleted=False)
        if karts:
            total_original_kart_price = 0
            total_kart_price = 0
            if karts:
                for kart in karts:
                    total_kart_price = total_kart_price + kart.get_total_item_price()
                    total_original_kart_price = total_original_kart_price + kart.get_total_original_price()
            # ---------------
            if request.method == "POST":
                street_address = request.POST.get('street_address')
                apartment_address = request.POST.get('apartment_address')
                country = request.POST.get('country')
                zip = request.POST.get('zip')
                payment_choice = request.POST.get('payment_choice')
                address = CheckoutAddress.objects.get_or_create(
                    user=request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip,
                )
                print("Added address")
                payment_obj = Payment.objects.create(
                    user=request.user,
                    amount=total_kart_price,
                    payment_choice=payment_choice,
                )
                print("payment created")
                obj = OrderPlaced.objects.create(
                    user=request.user,
                    ordered_date=datetime.date.today(),
                    ordered=True,
                    original_price=total_original_kart_price,
                    final_price=total_kart_price,
                    payment_id=payment_obj,
                )
                obj.items.set(karts)
                obj.save()
                print("Order placed")
                for kart in karts:
                    kart.ordered = True
                    kart.is_deleted = True
                    kart.save()

                address = CheckoutAddress.objects.filter(user=request.user).last()
                context = {
                    "address": address,
                    "total_items": len(karts),
                    "karts": karts,
                }
                messages.error(request, 'Congratulations! Order Placed...')
                return render(request, 'orderplaced.html', context)
            else:
                # -------------
                print(total_kart_price, 'price after discount')
                # -------------
                address = CheckoutAddress.objects.filter(user=request.user).first()
                context = {
                    "total_kart_price": total_kart_price,
                    "total_kart_items": len(karts),
                    "address": address,
                }
            return render(request, 'checkout.html', context)
        else:
            print("No items in cart")
            messages.error(request, 'No items in cart!')
            return HttpResponseRedirect('/product/cart/')
    else:
        messages.error(request, 'Login First!')
        return HttpResponseRedirect('/login/')


def my_orders(request):
    if request.user.is_authenticated:
        orders = OrderPlaced.objects.filter(user=request.user)
        context = {
            "orders": orders,
        }
        return render(request, 'myorders.html', context)
    else:
        return render(request, 'myorders.html')
