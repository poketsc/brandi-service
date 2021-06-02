from view.product_view        import ProductView
from view.order_view          import OrderView
from view.cart_view           import CartView
from view.order_complete_view import OrderCompleteView
from view.shipment_view       import ShipmentView
from view.product_detail_view import ProductDetailView
from view.user_view           import AccountView

def create_endpoints(app):
    app.add_url_rule("/carts", view_func=CartView.as_view("cart_view"))
    app.add_url_rule("/orders", view_func=OrderView.as_view("order_view"))
    app.add_url_rule("/products", view_func=ProductView.as_view("product_view"))
    app.add_url_rule("/shipments", view_func=ShipmentView.as_view("shipment_view"))
    app.add_url_rule("/login", view_func=AccountView.as_view("account_view"))
    app.add_url_rule("/products/<int:product_id>", view_func=ProductDetailView.as_view("product_detail_view"))
    app.add_url_rule("/orders/<int:order_id>", view_func=OrderCompleteView.as_view("order_complete_view"))
