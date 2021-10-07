from django.shortcuts import render, HttpResponseRedirect, reverse
from .forms import SignUpUsers, AdditionalDetails
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.files.storage import FileSystemStorage
from .models import CustomerInfo, Products, Kart
from django.core.paginator import Paginator
from django.db.models import Q
import cloudinary


# Create your views here.


def homepage(request):
    products = Products.objects.all().order_by('id')
    paginator = Paginator(products, 3, orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # ----------------------
    all_items = Kart.objects.filter(user=request.user)
    # ----------------------
    # context items
    context = {
        "products": products,
        "page_obj": page_obj,
        "total_kart_items": len(all_items),
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
    all_items = Kart.objects.filter(user=request.user)
    # --------------
    # context items
    context = {
        "results": page_obj,
        "search_obj": search_obj,
        "total_kart_items": len(all_items),
    }
    # ------------------------
    return render(request, 'searchpage.html', context)


def view_product(request, slug):
    data = Products.objects.get(slug=slug)
    item = Kart.objects.filter(user=request.user, ordered=False, item=data).first()
    print(data.image.url, '------image')
    # -------------
    all_items = Kart.objects.filter(user=request.user)
    # -------------
    print(len(all_items))
    context = {
        "data": data,
        "kart": item,
        "total_kart_items": len(all_items),
    }
    return render(request, 'productpage.html', context)


def add_kart(request, pk):
    data = Products.objects.get(id=pk)
    kart_data = Kart.objects.get_or_create(
        user=request.user,
        ordered=False,
        item=data,
        quantity=1,
    )
    return HttpResponseRedirect(reverse("product", kwargs={"slug": data.slug}))


def remove_from_kart(request, pk):
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


def increase_cart(request, pk):
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


def decrease_cart(request, pk):
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


def open_cart(request):
    # -------------
    karts = Kart.objects.filter(user=request.user)
    # -------------
    kart_list = []
    total_kart_price = 0
    if karts:
        for kart in karts:

            if kart.item.discount_price:
                total_item_price = kart.item.discount_price * kart.quantity
                dict = {'id': kart.item.id, 'name': kart.item.name, 'quantity': kart.quantity,
                        'description': kart.item.description,
                        'price': kart.item.price, 'discount_price': kart.item.discount_price,
                        'image': kart.item.image.url,
                        'label': kart.item.label, 'total_price': total_item_price}
                total_kart_price = total_kart_price + total_item_price
            else:
                total_item_price = kart.item.price * kart.quantity
                dict = {'id': kart.item.id, 'name': kart.item.name, 'quantity': kart.quantity,
                        'description': kart.item.description,
                        'price': kart.item.price, 'discount_price': kart.item.discount_price,
                        'image': kart.item.image.url,
                        'label': kart.item.label, 'total_price': total_item_price}
                total_kart_price = total_kart_price + total_item_price
            kart_list.append(dict)
            print(dict)
    print('/n', total_kart_price, '------------total kat price')
    print('/n', kart_list, '------------kart LIST')
    print('')
    print('')
    print('')
    print('')
    # -------------
    context = {
        "total_kart_items": len(karts),
        "products": karts,
        "total_kart_price": total_kart_price,
        "kart_list": kart_list,
    }
    return render(request, 'cartpage.html', context)
