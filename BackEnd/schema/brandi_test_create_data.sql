-- 계정 타입 테스트 데이터
INSERT INTO account_type (account_type)
VALUES ('master'), ('seller'), ('user');

-- 셀러 상태 테스트 데이터
INSERT INTO action_status (status)
VALUES ('입점'), ('입점대기'), ('퇴점'), ('퇴점대기'), ('휴점');

-- 셀러 카테고리 테스트 데이터
INSERT INTO seller_categories (name)
VALUES ('카테고리1'), ('카테고리2');

-- 셀러 서브카테고리 테스트 데이터
INSERT INTO seller_subcategories (seller_category_id, name)
VALUES (1, '쇼핑몰'), (1, '로드샵'), (1, '핸드메이드');

-- 질문 카테고리 테스트 데이터
INSERT INTO question_categories (name)
VALUES ('배송'), ('결제'), ('환불');

-- 결제 상태 테스트 데이터
INSERT INTO payment_status (payment_status)
VALUES ('결제대기'), ('결제완료');

-- 주문 상태 테스트 데이터
INSERT INTO order_status (order_status)
VALUES ('주문완료'), ('환불'), ('교환'), ('구매확정');


-- 배송 상태 테스트 데이터
INSERT INTO shipment_status (shipment_status)
VALUES ('배송준비중'), ('배송중'), ('배송완료');

-- 배송 메세지 테스트 데이터
INSERT INTO shipment_memo (content)
VALUES ('문 앞'), ('경비실'), ('올 때 전화'), ('직접입력');

-- 계정 테스트 데이터
INSERT INTO accounts (nickname, created_at, account_type_id)
VALUES ('TEST_MASTER', NOW(), 1), ('TEST_SELLER_1', NOW(), 2), ('TEST_SELLER_2', NOW(), 2), ('TEST_USER_1', NOW(), 3), ('TEST_USER_2', NOW(), 3);

-- 마스터 계정 테스트 데이터
INSERT INTO masters (Id)
VALUES (1);

-- 셀러 계정 테스트 데이터
insert into sellers (Id, seller_subcategory_id)
values (2, 1), (3, 2);

-- 셀러 계정 히스토리 테스트 데이터
insert into seller_histories (account_id, action_status_id, seller_id, start_time, end_time, password, seller_phone_number, korean_name, english_name, header_office_number, cs_office_hour, refund_information, is_deleted, profile_image_url, shipment_information, background_image_url, comment, detail_comment, cs_nickname, address)
values (1, 1, 2, now(), '9999-12-31 23:59:59', 'test_password', '01011112222', '테스트샵', 'testshop', '021113333', '09001800', '교환/환불 불가', 0, 'http://test.com/image', '당일배송', 'http://test.com/bgimage', 'test comment', 'test detail comment', 'kakao test', '강남구 테헤란로');
insert into seller_histories (account_id, action_status_id, seller_id, start_time, end_time, password, seller_phone_number, korean_name, english_name, header_office_number, cs_office_hour, refund_information, is_deleted, profile_image_url, shipment_information, background_image_url, comment, detail_comment, cs_nickname, address)
values (1, 1, 3, now(), '9999-12-31 23:59:59', 'test_password_2', '01011113333', '브랜디', 'brandi', '0312223333', '09001800', '교환/환불 불가', 0, 'http://brandi.com/image', '당일배송', 'http://brandi.com/bgimage', 'test comment2', 'test detail comment2', 'cacao test', '강남구 언주로');

-- 유저 계정 테스트 데이터
INSERT INTO users(Id, email)
VALUES (4, 'aaa123@naver.com'), (5, 'bbb234@gmail.com');

-- 유저 계정 히스토리 테스트 데이터
INSERT INTO user_histories(user_id, start_time, end_time, is_deleted, password)
VALUES (4, NOW(), '9999-12-31 23:59:59', 0, 'user123'), (5, NOW(), '9999-12-31 23:59:59', 0, 'user456');

-- 상품 테스트 데이터
INSERT INTO products(account_id, seller_id, created_at)
VALUES (1, 2, NOW()), (2, 2, NOW()),(2, 2, NOW()), (3, 3, NOW());

-- 상품 히스토리 테스트 데이터
INSERT INTO product_histories(account_id, product_id, name, shipment_information, price, detail_page_html, discount_rate, discount_start_time, discount_end_time, is_sold, is_displayed, minimum_sell_quantity, maximum_sell_quantity, comment, start_time, end_time, is_deleted)
VALUES (1, 1, '롱슬리브', '브랜디 배송', 30000, 'test_html', 10, '2021-04-01 23:59:59', '2021-05-31 23:59:59', 1, 1, 1, 5, '여름에 입기 좋은 긴팔티', now(), '9999-12-31 23:59:59', 0);
INSERT INTO product_histories(account_id, product_id, name, shipment_information, price, detail_page_html, discount_rate, discount_start_time, discount_end_time, is_sold, is_displayed, minimum_sell_quantity, maximum_sell_quantity, comment, start_time, end_time, is_deleted)
VALUES (2, 2, '숏슬리브', '직접 배송', 20000, 'test_html2',  null, null, null, 1, 1, 1, 10, '시원한 반팔티', now(), '9999-12-31 23:59:59', 0);

-- 상품 이미지 테스트 데이터
INSERT INTO product_images(product_id, image_url, is_main)
VALUES (1, 'test_url_1', TRUE), (1, 'test_url_2', FALSE), (2, 'test_url_3', TRUE);

-- 상품 사이즈 테스트 데이터
INSERT INTO sizes(size)
VALUES ('XS'), ('S'), ('M'), ('L'), ('XL');

-- 상품 색상 테스트 데이터
INSERT INTO colors(color)
VALUES ('red'), ('green'), ('blue'), ('black'), ('white');

-- 상품 옵션 테스트 데이터
INSERT INTO product_options(product_id, size_id, color_id, is_sold_out, stock)
VALUES (1, 1, 1, FALSE, 10), (1, 2, 1, FALSE, 10), (1, 3, 1, FALSE, 10), (1, 4, 1, FALSE, 10), (1, 5, 1, FALSE, 10);

-- 상품 질문 테스트 데이터
INSERT INTO questions(product_id, user_id, created_at)
VALUES (1, 4, NOW()), (1, 5, NOW()), (2, 4, NOW());

-- 상품 질문 히스토리 테스트 데이터
INSERT INTO question_histories(question_category_id, question_id, start_time, end_time, content, is_answered, is_deleted)
VALUES (1, 3, NOW(), '9999-12-31 23:59:59', '짊문 내용입니다.', FALSE, FALSE);

-- 상품 질문 답변 테스트 데이터
INSERT INTO question_answers(question_id, account_id, created_at)
VALUES (3, 1, NOW());

-- 상품 질문 답변 히스토리 테스트 데이터
INSERT INTO question_answer_histories(account_id, question_answer_id, comment, start_time, end_time, is_deleted)
VALUES (1, 1, '답변 내용입니다.', NOW(), '9999-12-31 23:59:59', FALSE);

