from BackEnd.view.user_view import TestView

def create_endpoints(app, services):
    
######################초기세팅########################
    test_service = services.test_service
    user_service = services.user_service

    app.add_url_rule('/test', view_func=TestView.as_view('post_test_view', test_service), methods=['POST'])
    app.add_url_rule('/test', view_func=TestView.as_view('get_test_view', user_service), methods=['GET'])
######################초기세팅########################