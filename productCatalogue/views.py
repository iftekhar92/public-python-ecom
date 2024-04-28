from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from productCatalogue.forms import ProductForm
from productCatalogue.models import Product
from categoryMgt.models import Category
from userCarts.models import UserCart
from shoppingCart.models import Cart


# Create your views here.
def queryProcess(request):
    filters = {}
    default_checked = {}
    category_id = []
    is_new = 1 if request.get("is_new") == "1" else 0
    is_featured = 1 if request.get("is_featured") == "1" else 0
    in_stock = 1 if request.get("in_stock") == "1" else 0
    categories = request.getlist("cat") if request.get("cat") else []

    for cat in categories:
        category_id.append(int(cat))
        default_checked[int(cat)] = "checked"
    if is_new:
        filters["is_new"] = is_new
        default_checked["is_new"] = "checked"
    if is_featured:
        filters["is_featured"] = is_featured
        default_checked["is_featured"] = "checked"
    if in_stock:
        filters["quantity__gt"] = 0
        default_checked["in_stock"] = "checked"

    if len(category_id):
        filters["category_id__in"] = category_id
    return {
        "products": Product.objects.filter(**filters),
        "default_checked": default_checked,
    }


def addToCartItems(cart_id, product_id, qty):
    msg = "Something went wrong while adding product into cart."
    severity = "error"
    if cart_id > 0:
        product = Product.objects.filter(id=product_id).first()
        check_existing_item = Cart.objects.filter(
            product_id=product_id, cart_id=cart_id
        ).first()

        if check_existing_item:
            if product and product.quantity >= qty:
                check_existing_item.quantity = qty + check_existing_item.quantity
                check_existing_item.save()
                product.quantity = product.quantity - qty
                product.save()
                msg = "Product quantity has been updated into cart successfully."
                severity = "success"
            else:
                msg = "Product quantity is insufficient."
                severity = "error"
        elif product and product.quantity >= qty:
            Cart.objects.create(cart_id=cart_id, quantity=qty, product=product)
            product.quantity = product.quantity - qty
            product.save()
            msg = "Product has been added into cart successfully."
            severity = "success"
    else:
        msg = "No cart found."
    return {"msg": msg, "severity": severity}


def addToCartProcessing(request, product_id, qty):
    cart_id = 0
    if "sessionid" in request.COOKIES:
        session_key = request.COOKIES["sessionid"]
        session = Session.objects.get(session_key=session_key)
        session_data = session.get_decoded()
        uid = session_data.get("_auth_user_id")
        user_detail = User.objects.get(id=uid)
        user_cart = UserCart.objects.filter(user_id=user_detail.id, guid="").first()
        if user_cart:
            cart_id = user_cart.id
    elif "guid" in request.COOKIES:
        user_cart = UserCart.objects.filter(
            guid=request.COOKIES["guid"], user_id=0
        ).first()
        if user_cart:
            cart_id = user_cart.id

    return addToCartItems(cart_id, product_id, qty)


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    default_checked = {}
    msg = ""
    severity = ""
    if request.method == "POST":
        response = queryProcess(request.POST)
        products = response.get("products")
        default_checked = response.get("default_checked")

        product_id = request.POST.get("product_id")
        qty = request.POST.get("qty")
        if product_id and qty:
            add_to_cart_res = addToCartProcessing(request, int(product_id), int(qty))
            msg = add_to_cart_res.get("msg")
            severity = add_to_cart_res.get("severity")

    return render(
        request,
        "productCatalogue/index.html",
        {
            "products": products,
            "categories": categories,
            "default_checked": default_checked,
            "msg": msg,
            "severity": severity,
        },
    )


def detail(request, slug):
    msg = ""
    severity = ""
    product = Product.objects.filter(slug=slug).first()
    if request.method == "POST":
        product_id = int(request.POST.get("product_id"))
        qty = int(request.POST.get("qty"))
        response = addToCartProcessing(request, product_id, qty)
        product = Product.objects.filter(slug=slug).first()
        msg = response.get("msg")
        severity = response.get("severity")

    return render(
        request,
        "productCatalogue/detail.html",
        {"product": product, "msg": msg, "severity": severity},
    )


def getProduct(request):
    products = Product.objects.all()
    return render(request, "productCatalogue/list.html", {"products": products})


def create(request):
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/product/list")

    return render(
        request, "productCatalogue/form.html", {"form": form, "title": "Create Product"}
    )


def update(request, id):
    product = Product.objects.get(id=id)
    form = ProductForm(instance=product)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            return redirect("/product/list")

    return render(
        request, "productCatalogue/form.html", {"form": form, "title": "Update Product"}
    )


def delete(request, id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        product.delete()
        return redirect("/product/list")

    return render(request, "productCatalogue/confirm.html", {"product": product})
