import uuid
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.http import HttpResponse

from userCarts.models import UserCart
from shoppingCart.models import Cart
from productCatalogue.models import Product


class CartHandler:
    def __init__(self, get_response):
        print("INIT")
        self.get_response = get_response

    def __call__(self, request):
        guid = {"key": "guid", "value": "", "age": -1}
        if "sessionid" in request.COOKIES:
            session_key = request.COOKIES["sessionid"]
            session = Session.objects.filter(session_key=session_key).first()
            session_data = session.get_decoded()
            uid = session_data.get("_auth_user_id")
            user_detail = User.objects.filter(id=uid).first()

            # Fetch existing user cart
            get_existing_user_cart = UserCart.objects.filter(
                user_id=user_detail.id, guid=""
            ).first()
            # Fetch anonymous user cart

            if "guid" in request.COOKIES:
                anonymous_cart = UserCart.objects.filter(
                    guid=request.COOKIES["guid"], user_id=0
                ).first()
                if get_existing_user_cart:
                    # Delete anonymous user cart
                    deleteAnonymous = UserCart.objects.filter(
                        guid=request.COOKIES["guid"], user_id=0
                    ).first()
                    if deleteAnonymous:
                        deleteAnonymous.delete()

                    # Merge new items into existing cart or add into existing cart
                    anonymous_cart_items = Cart.objects.filter(
                        cart_id=anonymous_cart.id
                    )
                    if anonymous_cart_items:
                        for item in anonymous_cart_items:
                            check_existing = Cart.objects.filter(
                                cart_id=get_existing_user_cart.id,
                                product_id=item.product_id,
                            ).first()
                            if check_existing:
                                check_existing.quantity = (
                                    check_existing.quantity + item.quantity
                                )
                                check_existing.save()
                            else:
                                product = Product.objects.filter(
                                    id=item.product_id
                                ).first()
                                Cart(
                                    cart_id=get_existing_user_cart.id,
                                    quantity=item.quantity,
                                    product=product,
                                ).save()
                            Cart(id=item.id).delete()
                else:
                    # Convert anonymous user cart to real cart
                    if anonymous_cart:
                        anonymous_cart.guid = ""
                        anonymous_cart.user_id = user_detail.id
                        anonymous_cart.save()
                    # Convert anonymous cart item to real cart
                    anonymous_cart_items = Cart.objects.filter(
                        cart_id=anonymous_cart.id
                    )
                    if anonymous_cart_items:
                        for item in anonymous_cart_items:
                            check_existing = Cart.objects.filter(id=item.id).first()
                            if check_existing:
                                check_existing.cart_id = anonymous_cart.id
                                check_existing.save()

                guid["value"] = ""
                guid["age"] = -1
            else:
                if not get_existing_user_cart:
                    UserCart.objects.create(user_id=user_detail.id, guid="")

        elif "guid" in request.COOKIES:
            get_anonymous_user_cart = UserCart.objects.filter(
                guid=request.COOKIES["guid"], user_id=0
            ).first()
            if not get_anonymous_user_cart:
                UserCart.objects.create(user_id=0, guid=request.COOKIES["guid"])
            guid["value"] = request.COOKIES["guid"]
            guid["age"] = 120
        else:
            generate_guid = str(uuid.uuid4())
            UserCart.objects.create(user_id=0, guid=generate_guid)
            guid["value"] = generate_guid
            guid["age"] = 120

        total_items = 0
        if "guid" in request.COOKIES:
            user_cart = UserCart.objects.filter(guid=request.COOKIES["guid"]).first()
            if user_cart:
                cart_items = Cart.objects.filter(cart_id=user_cart.id)
                if cart_items:
                    for x in cart_items:
                        total_items = total_items + x.quantity
        elif "sessionid" in request.COOKIES:
            session = Session.objects.filter(
                session_key=request.COOKIES["sessionid"]
            ).first()
            session_data = session.get_decoded()
            uid = session_data.get("_auth_user_id")
            user_detail = User.objects.filter(id=uid).first()
            user_cart = UserCart.objects.filter(user_id=user_detail.id).first()
            if user_cart:
                cart_items = Cart.objects.filter(cart_id=user_cart.id)
                if cart_items:
                    for x in cart_items:
                        total_items = total_items + x.quantity
        request.total_items = total_items
        response = self.get_response(request)
        response.set_cookie(guid["key"], guid["value"], guid["age"])
        return response


class ExceptionHandler:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        print(exception.__class__.__name__)
        print(exception)
        return HttpResponse(
            "<b>Currently, we are facing some issue. Please tyy again</b>"
        )
