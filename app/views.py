from django.shortcuts import render, HttpResponseRedirect, reverse
from .forms import SignUpUsers, AdditionalDetails
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.files.storage import FileSystemStorage
from .models import CustomerInfo, Products, Kart, OrderPlaced, CheckoutAddress, Payment, OrderedItems
from django.core.paginator import Paginator
from django.db.models import Q
import cloudinary
import datetime


# Create your views here.
def kart_items(request):
    if request.user.is_authenticated:
        all_items = Kart.objects.filter(user=request.user)
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
                        return HttpResponseRedirect(reverse('homepage'))  # reverse redirect
                    else:
                        return HttpResponseRedirect('/additionaldetails/')
                else:
                    print("else part")
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
            return HttpResponseRedirect(reverse('homepage'))
    fm = AdditionalDetails()
    context = {
        "form": fm
    }
    return render(request, 'additional_details.html', context)


def logout_user(request):
    logout(request)
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
    return render(request, 'searchpage.html', context)


def view_product(request, slug):
    data = Products.objects.get(slug=slug)
    if request.user.is_authenticated:
        item = Kart.objects.filter(user=request.user, ordered=False, item=data).first()
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
        return HttpResponseRedirect(reverse("product", kwargs={"slug": data.slug}))
    else:
        return HttpResponseRedirect('/login/')


def remove_from_kart(request, pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = Products.objects.get(id=pk)
            item = Kart.objects.filter(user=request.user, ordered=False, item=data).first()
            if item:
                item.delete()
            else:
                print("nothing in cart")
            return HttpResponseRedirect(reverse("cart"))
        else:
            data = Products.objects.get(id=pk)
            item = Kart.objects.filter(user=request.user, ordered=False, item=data).first()
            if item:
                item.delete()
            else:
                print("nothing in cart")
            return HttpResponseRedirect(reverse("product", kwargs={"slug": data.slug}))
    else:
        return HttpResponseRedirect('/login/')


def increase_cart(request, pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = Products.objects.get(id=pk)
            item = Kart.objects.filter(user=request.user, ordered=False, item=data).first()
            if item:
                if item.quantity == 0:
                    pass
                else:
                    item.quantity = item.quantity + 1
                    item.save()
            return HttpResponseRedirect(reverse("cart"))
        else:
            data = Products.objects.get(id=pk)
            item = Kart.objects.filter(user=request.user, ordered=False, item=data).first()
            if item:
                if item.quantity == 0:
                    pass
                else:
                    item.quantity = item.quantity + 1
                    item.save()
            return HttpResponseRedirect(reverse("product", kwargs={"slug": data.slug}))
    else:
        return HttpResponseRedirect('/login/')


def decrease_cart(request, pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = Products.objects.get(id=pk)
            item = Kart.objects.filter(user=request.user, ordered=False, item=data).first()
            if item:
                if item.quantity == 1:
                    print("Can't remove anymore")
                elif item.quantity == 0:
                    print("Can't remove, 0 items in cart")
                else:
                    item.quantity = item.quantity - 1
                    item.save()
            return HttpResponseRedirect(reverse("cart"))
        else:
            data = Products.objects.get(id=pk)
            item = Kart.objects.filter(user=request.user, ordered=False, item=data).first()
            if item:
                if item.quantity == 1:
                    print("Can't remove anymore")
                elif item.quantity == 0:
                    print("Can't remove, 0 items in cart")
                else:
                    item.quantity = item.quantity - 1
                    item.save()
            return HttpResponseRedirect(reverse("product", kwargs={"slug": data.slug}))
    else:
        return HttpResponseRedirect('/login/')


def open_cart(request):
    if request.user.is_authenticated:
        # -------------
        karts = Kart.objects.filter(user=request.user)
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
        return HttpResponseRedirect('/login/')


def open_checkout(request):
    if request.user.is_authenticated:
        # --------------
        karts = Kart.objects.filter(user=request.user)
        total_original_kart_price = 0
        total_kart_price = 0
        if karts:
            for kart in karts:
                total_kart_price = total_kart_price + kart.get_total_item_price()
                total_original_kart_price = total_original_kart_price + kart.get_total_original_price()
        # ---------------
        if request.method == "POST":
            # ---------------

            ordered_list = []
            for kart in karts:
                ord_items = OrderedItems.objects.create(
                    user=request.user,
                    ordered=True,
                    item=kart.item,
                    quantity=kart.quantity,
                )
                ordered_list.append(ord_items)
            print(ordered_list)
            # ---------------
            street_address = request.POST.get('street_address')
            apartment_address = request.POST.get('apartment_address')
            country = request.POST.get('country')
            zip = request.POST.get('zip')
            payment_choice = request.POST.get('payment_choice')
            address = CheckoutAddress.objects.create(
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
            obj.items.set(ordered_list)
            obj.save()
            print("Order placed")
            karts.delete()
            print("kart deleted")
            return HttpResponseRedirect(reverse('homepage'))
        else:
            # -------------
            print(total_kart_price, 'price after discount')
            # -------------
            context = {
                "total_kart_price": total_kart_price,
                "total_kart_items": len(karts)
            }
        return render(request, 'checkout.html', context)
    else:
        return HttpResponseRedirect('/login/')
