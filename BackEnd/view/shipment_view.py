from flask       import jsonify, g
from flask.views import MethodView

from util.decorator          import login_required
from service                 import ShipmentService
from connection              import connect_db
from flask_request_validator import *

from util.exception import *
from util.message   import *

class ShipmentView(MethodView):

    @login_required
    @validate_params(
        Param("name", JSON, str, required=True), 
        Param("phone_number", JSON, str, required=True),
        Param("is_defaulted", JSON, bool, required=True),
        Param("address", JSON, str, required=True),
        Param("additional_address", JSON, str, required=True),
        Param("zip_code", JSON, int, required=True),
        Param("is_deleted", JSON, bool, required=True)
    )
    def post(self, valid: ValidRequest):
        """배송지 추가하기

        Author:
            백승찬

        Args:
            {
                "name"               : 수령인
                "phone_number        : 수령인 전화번호
                "is_defaulted        : 기본 배송지 선택 여부
                "address"            : 주소
                "additional_address" : 추가 주소 정보
                "zip_code"           : 우편번호
                "is_deleted"         : 삭제 여부
            }

        Raises:

        Returns:
            { "data": 1 }
        """

        shipment_service = ShipmentService()
        connection       = None

        try:
            filters               = valid.get_json()
            filters["account_id"] = g.account_info["account_id"]

            connection = connect_db()
            
            result     = shipment_service.insert_address_information(connection, filters)
            
            connection.commit()
            
            return jsonify({"data" : result})

        except Exception as e:
                connection.rollback()       
                raise e
        
        finally:
            if connection is not None:
                connection.close()

    @login_required
    @validate_params(
        Param("address_id", JSON, int, required=True),
        Param("name", JSON, str, required=True), 
        Param("phone_number", JSON, str, required=True),
        Param("is_defaulted", JSON, bool, required=True),
        Param("is_deleted", JSON, bool, required=True),
        Param("address", JSON, str, required=True),
        Param("additional_address", JSON, str, required=True),
        Param("zip_code", JSON, int, required=True)
    )
    def patch(self, valid: ValidRequest):
        """배송지 수정하기

        Author:
            백승찬

        Args:
            {
                "address_id"         : 주소 아이디
                "name"               : 수령인
                "phone_number        : 수령인 전화번호
                "is_defaulted        : 기본 배송지 선택 여부
                "address"            : 주소
                "additional_address" : 추가 주소 정보
                "zip_code"           : 우편번호
                "is_deleted"         : 삭제 여부
            }

        Raises:

        Returns:
            { "data": 1 }
        """

        shipment_service = ShipmentService()
        connection       = None

        try:
            filters               = valid.get_json()
            filters["account_id"] = g.account_info["account_id"]

            connection = connect_db()
            
            result     = shipment_service.update_address_information(connection, filters)
            
            connection.commit()
            
            return jsonify({"data" : result})

        except Exception as e:
            connection.rollback()       
            raise e
        
        finally:
            if connection is not None:
                connection.close()
    
    @login_required
    def get(self):
        """배송지 수정하기

        Author:
            백승찬

        Args:

        Raises:

        Returns:
            {
                "data": [
                    {
                        "additional_address" : 추가 주소 정보
                        "address"            : 주소
                        "address_history_id" : 주소 히스토리 아이디
                        "address_id"         : 주소 아이디
                        "end_time"           : 종료 시간
                        "is_defaulted"       : 기본 배송지 여부
                        "is_deleted"         : 삭제 여부
                        "name"               : 수령인 이름
                        "phone_number"       : 수령인 핸드폰 번호
                        "start_time"         : 시작 시간
                        "zip_code"           : 우편번호
                    }
                ]
            }
        """

        shipment_service = ShipmentService()
        connection       = None

        try:
            filters = {
                "account_id" : g.account_info["account_id"]
            }

            connection = connect_db()

            result     = shipment_service.get_address_information(connection, filters)
            
            connection.commit()

            return jsonify({"data" : result})

        except Exception as e:
            connection.rollback()       
            raise e

        finally:
            if connection is not None:
                connection.close()
    
    @login_required
    @validate_params(
        Param("address_id", JSON, int, required=True)
    )
    def delete(self, valid: ValidRequest):
        """배송지 삭제하기

        Author:
            백승찬

        Args:
            data (dict) : {
                "address_id" : 주소 아이디
                }

        Raises:

        Returns:
            {
                "data": 1
            }
        """
        
        shipment_service = ShipmentService()
        connection       = None

        try:
            filters               = valid.get_json()
            filters["account_id"] = g.account_info["account_id"]

            connection = connect_db()

            result     = shipment_service.delete_address_information(connection, filters)

            connection.commit()

            return jsonify({"data" : result})

        except Exception as e:
            connection.rollback()       
            raise e

        finally:
            if connection is not None:
                connection.close()