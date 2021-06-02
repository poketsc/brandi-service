from model          import ShipmentDao, OrderDao, SelectNowDao
from util.exception import *
from util.message   import *

class ShipmentService:
    
    def insert_address_information(self, connection, filters):

        shipment_dao = ShipmentDao()
        now_dao      = SelectNowDao()

        # 현재 시점 선언
        now            = now_dao.select_now(connection)
        filters["now"] = now

        shipment_information = shipment_dao.get_all_shipment_information(connection, filters)

        # 배송지 주소 정보가 5개 일때
        if len(shipment_information) >= 5:
            raise MaximumShipmentInformationError(MAXIMUM_SHIPMENT_INFORMATION_ERROR, 400)
        
        address_id            = shipment_dao.insert_address_information(connection, filters)
        filters["address_id"] = address_id

        # 기본 배송지로 설정할때
        if filters["is_defaulted"] is True:

            defaulted_true             = shipment_dao.get_defaulted_true_shipment_information(connection, filters)

            # 기존에 기본 배송지가 존재하지 않는 경우
            if not defaulted_true:
                insert_address_history = shipment_dao.insert_address_history_information(connection, filters)

                if not insert_address_history:
                    raise InsertAddressHistoryInformationError(INSERT_ADDRESS_HISTORY_INFORMATION_ERROR, 400)
            
            # 기존에 기본 배송지가 존재하는 경우
            else:
                defaulted_true["account_id"] = filters["account_id"]
                defaulted_true["now"]        = now

                update_address               = shipment_dao.update_address_history_end_time(connection, defaulted_true)

                if not update_address:
                    raise UpdateAddressHistoryEndTimeError(UPDATE_ADDRESS_HISTORY_END_TIME_ERROR, 400)
                
                defaulted_true["is_defaulted"] = False
                insert_address_history         = shipment_dao.insert_address_history_information(connection, defaulted_true)

                if not insert_address_history:
                    raise InsertAddressHistoryInformationError(INSERT_ADDRESS_HISTORY_INFORMATION_ERROR, 400)
                
                insert_address_history = shipment_dao.insert_address_history_information(connection, filters)

                if not insert_address_history:
                    raise InsertAddressHistoryInformationError(INSERT_ADDRESS_HISTORY_INFORMATION_ERROR, 400)
        
        # 기본 배송지로 설정하지 않을때
        else:
            # 이전에 주소를 설정한적이 없으면 기본 배송지로 자동 설정
            if len(shipment_information) == 0:
                filters['is_defaulted'] = True
                insert_address_history  = shipment_dao.insert_address_history_information(connection, filters)

                if not insert_address_history:
                    raise InsertAddressHistoryInformationError(INSERT_ADDRESS_HISTORY_INFORMATION_ERROR, 400)
            
            else:
                insert_address_history = shipment_dao.insert_address_history_information(connection, filters)

        return insert_address_history

    # 이미 등록된 배송지 정보 바꿀때
    def update_address_information(self, connection, filters):

        shipment_dao = ShipmentDao()
        now_dao      = SelectNowDao()

        # 현재 시점 선언
        now            = now_dao.select_now(connection)
        filters['now'] = now

        # 기본 배송지 가져오기
        defaulted_true = shipment_dao.get_defaulted_true_shipment_information(connection, filters)

        # is_defaulted == True 일때
        if filters["is_defaulted"] is True:
            
            # 기본 배송지에 정보 추가,수정
            defaulted_true["now"]        = now
            defaulted_true["account_id"] = filters["account_id"]

            # 기본 배송지 정보 바꿀때
            if defaulted_true["address_id"] == filters["address_id"]:

                # 기본 배송지 end_time 변경
                update_address_end_time = shipment_dao.update_address_history_end_time(connection, defaulted_true)
                if not update_address_end_time:
                    raise UpdateAddressHistoryEndTimeError(UPDATE_ADDRESS_HISTORY_END_TIME_ERROR, 400)
            
                insert_address_history = shipment_dao.insert_address_history_information(connection, filters)

                if not insert_address_history:
                    raise InsertAddressHistoryInformationError(INSERT_ADDRESS_HISTORY_INFORMATION_ERROR, 400)
            
            # 일반 배송지 기본 배송지로 바꿀때
            else:
                # 기본 배송지 end_time 변경
                update_address_end_time = shipment_dao.update_address_history_end_time(connection, defaulted_true)
                if not update_address_end_time:
                    raise UpdateAddressHistoryEndTimeError(UPDATE_ADDRESS_HISTORY_END_TIME_ERROR, 400)

                # 기본 배송지 -> 일반 배송지로 변경
                defaulted_true["is_defaulted"] = False
                insert_address_history = shipment_dao.insert_address_history_information(connection, defaulted_true)

                if not insert_address_history:
                    raise InsertAddressHistoryInformationError(INSERT_ADDRESS_HISTORY_INFORMATION_ERROR, 400)
                
                # 일반 배송지 end_time 변경
                update_address_end_time = shipment_dao.update_address_history_end_time(connection, filters)
                if not update_address_end_time:
                    raise UpdateAddressHistoryEndTimeError(UPDATE_ADDRESS_HISTORY_END_TIME_ERROR, 400)

                # 일반 배송지 -> 기본 배송지로 변경
                insert_address_history = shipment_dao.insert_address_history_information(connection, filters)

                if not insert_address_history:
                    raise InsertAddressHistoryInformationError(INSERT_ADDRESS_HISTORY_INFORMATION_ERROR, 400)

        # is_defaulted == False 일때
        else:
            # 일반 배송지 end_time 변경
            update_address_end_time = shipment_dao.update_address_history_end_time(connection, filters)
            if not update_address_end_time:
                raise UpdateAddressHistoryEndTimeError(UPDATE_ADDRESS_HISTORY_END_TIME_ERROR, 400)

            # 일반 배송지 정보 변경
            insert_address_history = shipment_dao.insert_address_history_information(connection, filters)
            if not insert_address_history:
                raise InsertAddressHistoryInformationError(INSERT_ADDRESS_HISTORY_INFORMATION_ERROR, 400)
        
        return insert_address_history

    def get_address_information(self, connection, filters):

        shipment_dao = ShipmentDao()

        # 배송지 정보 가져오기
        shipment_information = shipment_dao.get_all_shipment_information(connection, filters)

        return shipment_information
    
    def delete_address_information(self, connection, filters):

        shipment_dao = ShipmentDao()
        now_dao      = SelectNowDao()

        # 프론트로부터 받은 address_id 로 주소 정보 가져오기
        address_information = shipment_dao.get_one_shipment_information(connection, filters)

        # 프론트로부터 받은 address_id가 기본 배송지면 삭제 불가
        if address_information["is_defaulted"] == 1:
            raise DeleteAddressInformationError(DELETE_ADDRESS_INFORMATION_ERROR, 400)

        # 현재 시점 선언
        now                               = now_dao.select_now(connection)
        address_information["now"]        = now
        address_information["account_id"] = filters["account_id"]

        # 데이터 정보 시간 끊기
        update_address_end_time = shipment_dao.update_address_history_end_time(connection, address_information)
        if not update_address_end_time:
            raise UpdateAddressHistoryEndTimeError(UPDATE_ADDRESS_HISTORY_END_TIME_ERROR, 400)

        # 변경할 데이터 정보 insert
        address_information["is_deleted"] = True
        insert_address_history = shipment_dao.insert_address_history_information(connection, address_information)
        if not insert_address_history:
            raise InsertAddressHistoryInformationError(INSERT_ADDRESS_HISTORY_INFORMATION_ERROR, 400)
        
        return insert_address_history