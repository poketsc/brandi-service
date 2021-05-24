from view.user_view  import TestView
from view.order_view import CartView

def create_endpoints(app):

######################초기세팅########################
    app.add_url_rule('/test', view_func=TestView.as_view('test_view'))
######################초기세팅########################

    app.add_url_rule('/carts', view_func=CartView.as_view('cart_view'))
    app.add_url_rule('/getcarts', view_func=CartView.as_view('get_cart'))