from django.shortcuts import render, redirect
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from shoppingCart.models import Cart
from userCarts.models import UserCart
from productCatalogue.models import Product
from shoppingCart.forms import OrderForm
from shoppingCart.models import Order
from shoppingCart.models import OrderItems
from django.contrib.auth.decorators import login_required

# Create your views here.


def getCartId(request):
    cart_id = 0
    if "sessionid" in request.COOKIES:
        session_key = request.COOKIES["sessionid"]
        session = Session.objects.get(session_key=session_key)
        session_data = session.get_decoded()
        uid = session_data.get("_auth_user_id")
        user_detail = User.objects.filter(id=uid).first()
        user_cart = UserCart.objects.filter(user_id=user_detail.id, guid="").first()
        if user_cart:
            cart_id = user_cart.id
    elif "guid" in request.COOKIES:
        user_cart = UserCart.objects.filter(
            guid=request.COOKIES["guid"], user_id=0
        ).first()
        if user_cart:
            cart_id = user_cart.id
    return cart_id


def cartView(request):
    cart_id = getCartId(request)
    items = {}
    msg = ""
    severity = ""
    common_msg = "Cart has been updated successfully."
    if cart_id > 0:
        items = Cart.objects.filter(cart_id=cart_id)
    else:
        msg = "Sorry, Your cart does not exist."
        severity = "error"
    if request.method == "POST":
        product = ""
        req_type = request.POST.get("type")
        item_id = request.POST.get("item_id")
        cart_item = Cart.objects.filter(id=int(item_id)).first()
        if cart_item:
            product = Product.objects.filter(id=cart_item.product_id).first()
        # Remove item from cart
        if req_type == "remove_item":
            if product:
                product.quantity = product.quantity + cart_item.quantity
                product.save()
                cart_item.delete()
                items = Cart.objects.filter(cart_id=cart_id)
                msg = "Product has been removed from cart successfully."
                severity = "success"
        elif req_type == "cart_update":
            quantity = int(request.POST.get("quantity"))
            if product:
                if quantity > cart_item.quantity and product.quantity >= (
                    quantity - cart_item.quantity
                ):
                    product.quantity = product.quantity - (
                        quantity - cart_item.quantity
                    )
                    product.save()
                    cart_item.quantity = quantity
                    cart_item.save()
                    items = Cart.objects.filter(cart_id=cart_id)
                    msg = common_msg
                    severity = "success"
                elif cart_item.quantity > quantity:
                    product.quantity = product.quantity + (
                        cart_item.quantity - quantity
                    )
                    product.save()
                    cart_item.quantity = quantity
                    cart_item.save()
                    items = Cart.objects.filter(cart_id=cart_id)
                    msg = common_msg
                    severity = "success"
                elif cart_item.quantity == quantity:
                    msg = common_msg
                    severity = "success"
                else:
                    msg = "Product quantity is insufficient."
                    severity = "error"
    return render(
        request,
        "shoppingCart/cart.html",
        {"items": items, "msg": msg, "severity": severity},
    )


def placeOrder(request, cart_items):
    order_no = 0
    author = User.objects.get(id=request.user.id)
    full_name = request.POST.get("full_name")
    phone_number = request.POST.get("phone_number")
    email = request.POST.get("email")
    pin_code = request.POST.get("pin_code")
    full_address = request.POST.get("full_address")
    payment_mode = request.POST.get("payment_mode")
    total_amount = request.POST.get("total_amount")

    order_inst = Order(
        author=author,
        full_name=full_name,
        phone_number=phone_number,
        email=email,
        pin_code=pin_code,
        full_address=full_address,
        payment_mode=payment_mode,
        total_amount=total_amount,
        status="Order Placed",
    )
    order_inst.save()
    if order_inst.id:
        for item in cart_items:
            order_item = OrderItems(
                product=Product.objects.get(id=item.product_id),
                quantity=item.quantity,
                price=item.product.price,
            )
            order_item.save()
            order_inst.order_items.add(order_item)

        UserCart.objects.get(id=cart_items[0].cart_id).delete()
        cart_items.delete()
        msg = "Your order has been placed successfully."
        severity = "success"
        order_no = order_inst.id
    else:
        msg = "Something went wrong, during order placing. Please try later."
        severity = "error"
    return {"msg": msg, "severity": severity, "order_no": order_no}


@login_required
def checkout(request):
    if request.user.is_authenticated:
        total = 0
        cart_items = ""
        msg = ""
        severity = ""
        user_cart = UserCart.objects.filter(user_id=request.user.id, guid="").first()
        form = OrderForm()
        if user_cart:
            cart_items = Cart.objects.filter(cart_id=user_cart.id)
            if cart_items:
                for item in cart_items:
                    total = total + (item.quantity * item.product.price)
            else:
                msg = "There is not item into cart. Are you want to shopping now?"
                severity = "warning"
        else:
            msg = "Cart does not exist. Please logout and login again."
            severity = "warning"

        if request.method == "POST":
            form = OrderForm(request.POST)
            if form.is_valid():
                response = placeOrder(request, cart_items)
                if (
                    response.get("order_no") > 0
                    and response.get("severity") == "success"
                ):
                    request.session["msg"] = response.get("msg")
                    request.session["severity"] = response.get("severity")
                    request.session["order_no"] = response.get("order_no")
                    return redirect("/order-confirmation/")
            else:
                msg = "Invalid entry. Please fill the form properly."
                severity = "error"

        return render(
            request,
            "shoppingCart/checkout.html",
            {"form": form, "total": total, "msg": msg, "severity": severity},
        )

    else:
        return redirect("/accounts/login/")


@login_required
def orderConfirmation(request):
    order_no = 3
    msg = ""
    severity = ""
    response = {"items": []}
    if "msg" in request.session:
        msg = request.session["msg"]
        request.session["msg"] = ""
    if "severity" in request.session:
        severity = request.session["severity"]
        request.session["severity"] = ""
    if "order_no" in request.session and request.session["order_no"] > 0:
        order_no = request.session["order_no"]
        request.session["order_no"] = 0

    if order_no:
        order_details = Order.objects.filter(id=order_no).first()
        if order_details:
            items = order_details.order_items.all()
            if items:
                response["order_no"] = order_details.id
                response["payment_mode"] = order_details.payment_mode
                response["total_items"] = len(items)
                subtotal = 0
                for item in items:
                    subtotal = subtotal + (item.quantity * item.price)
                    response["items"].append(
                        {
                            "image": item.product.image,
                            "name": item.product.name,
                            "slug": item.product.slug,
                            "quantity": item.quantity,
                            "price": item.price,
                            "subtotal": item.quantity * item.price,
                        }
                    )
                response["subtotal"] = subtotal
    if len(response.get("items")) > 0:
        return render(
            request,
            "shoppingCart/order-confirmation.html",
            {"msg": msg, "severity": severity, "response": response},
        )
    return redirect("/orders/")


@login_required
def orders(request):
    if request.user.is_authenticated:
        msg = "There is no order"
        severity = "warning"
        response = []
        if request.method == "POST":
            status = request.POST.get("status")
            if status:
                get_order = Order.objects.filter(
                    id=int(request.POST.get("order_id"))
                ).first()
                if get_order:
                    get_order.status = status
                    get_order.save()

        order_details = Order.objects.filter(author_id=request.user.id)
        if len(order_details) > 0:
            msg = ""
            severity = ""
            for order in order_details:
                items = order.order_items.all()
                if items:
                    tmp_order = {"items": []}
                    tmp_order["order_no"] = order.id
                    tmp_order["order_date"] = order.order_date
                    tmp_order["payment_mode"] = order.payment_mode
                    tmp_order["status"] = order.status
                    tmp_order["total_items"] = len(items)
                    tmp_order["subtotal"] = order.total_amount
                    for item in items:
                        tmp_order["items"].append(
                            {
                                "image": item.product.image,
                                "name": item.product.name,
                                "slug": item.product.slug,
                                "quantity": item.quantity,
                                "price": item.price,
                                "subtotal": item.quantity * item.price,
                            }
                        )
                    response.append(tmp_order)
        return render(
            request,
            "shoppingCart/orders.html",
            {"msg": msg, "severity": severity, "response": response},
        )

    else:
        return redirect("/accounts/login/")
