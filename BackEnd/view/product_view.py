from flask import jsonify, request
from flask.views import MethodView
from flask_request_validator import GET, PATH, Param, validate_params, CompositeRule, Min, Max

from service    import ProductService
from connection import connect_db

class ProductView(MethodView):

    # 로그인 여부 데코레이터
    @validate_params(
        Param("offset", GET, int, required=False),
        Param("limit", GET, int, required=False, rules=CompositeRule(Min(1), Max(100)))
    )
    def get(*args):
        """메인 상품 리스트

        Author:
            이서진

        Returns:
            200: {
            }
        """

        filters = {
            "offset": int(request.args.get("offset", 0)),
            "limit": int(request.args.get("limit", 30))
        }

        if filters.get("offset") < 0:
            filters["offset"] = 0

        if filters.get("limit") < 1:
            filters["limit"] = 1

        product_service = ProductService()
        connection = None

        try:
            connection = connect_db()
            result = product_service.get_product_list(connection, filters)
            return jsonify({"data": result})

        except Exception as e:
            raise e

        finally:
            if connection is not None:
                connection.close()