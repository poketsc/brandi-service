from BackEnd.view.user_view import TestView

def create_endpoints(app):

######################초기세팅########################
    app.add_url_rule('/test', view_func=TestView.as_view('test_view'))
######################초기세팅########################