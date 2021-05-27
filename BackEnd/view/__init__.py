from view.product_view import ProductView, ProductDetailView
from view.order_view   import CartView, OrderView, ShipmentView
from view.user_view    import AccountView

def create_endpoints(app):
    app.add_url_rule("/carts", view_func=CartView.as_view("cart_view"))
    app.add_url_rule("/orders", view_func=OrderView.as_view("order_view"))
    app.add_url_rule("/products", view_func=ProductView.as_view("product_view"))
    app.add_url_rule('/shipments', view_func=ShipmentView.as_view('shipment_view'))
    app.add_url_rule("/login", view_func=AccountView.as_view("account_view"))
    app.add_url_rule("/productdetails", view_func=ProductDetailView.as_view("product_detail_view"))
