from view.order_view import CartView, OrderView
from view.product_view import ProductView


def create_endpoints(app):
    app.add_url_rule('/cart', view_func=CartView.as_view('cart_view'))
    app.add_url_rule('/order', view_func=OrderView.as_view('order_view'))
    app.add_url_rule("/products", view_func=ProductView.as_view("product_view"))
