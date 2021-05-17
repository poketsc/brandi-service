create table account_type
(
    Id           int auto_increment
        primary key,
    account_type varchar(45) not null comment '계정 타입'
)
    comment '계정 분류';

create table accounts
(
    Id              int auto_increment
        primary key,
    nickname        varchar(20) not null comment 'u,a,m 계정 관리',
    created_at      datetime    not null comment '계정 생성 날짜',
    account_type_id int         not null comment '계정 타입',
    constraint FK_accounts_account_type_id_account_type_Id
        foreign key (account_type_id) references account_type (Id)
)
    comment '계정';

create table action_status
(
    Id     int auto_increment
        primary key,
    status varchar(10) not null comment '상태'
)
    comment '셀러 상품 판매상태';

create table colors
(
    Id    int auto_increment
        primary key,
    color varchar(10) not null comment '색상'
)
    comment '상품색상';

create table masters
(
    Id int not null
        primary key,
    constraint FK_masters_Id_accounts_Id
        foreign key (Id) references accounts (Id)
)
    comment '마스터계정';

create table master_histories
(
    Id         int auto_increment
        primary key,
    master_id  int         not null comment '마스터',
    is_deleted tinyint     not null comment '삭제 여부',
    start_time datetime    not null comment '변경 시작일',
    end_time   datetime    not null comment '변경 종료일',
    password   varchar(60) not null comment '비밀번호',
    constraint FK_master_histories_master_id_masters_Id
        foreign key (master_id) references masters (Id)
)
    comment '마스터 히스토리';

create table order_status
(
    Id           int auto_increment
        primary key,
    order_status varchar(10) not null comment '주문 상태'
)
    comment '주문 상태';

create table payment_status
(
    Id             int auto_increment
        primary key,
    payment_status varchar(45) not null comment '결제 상태'
)
    comment '결제 상태';

create table question_categories
(
    Id   int auto_increment
        primary key,
    name varchar(10) null comment '분류 이름'
)
    comment 'Q&A 분류';

create table seller_categories
(
    Id   int auto_increment
        primary key,
    name varchar(8) not null comment '1차 카테고리 명'
)
    comment '셀러_1차분류';

create table seller_subcategories
(
    Id                 int auto_increment
        primary key,
    seller_category_id int        not null comment '1차 카테고리',
    name               varchar(8) not null comment '2차 카테고리 명',
    constraint FK_seller_subcategories_seller_category_id_seller_categories_Id
        foreign key (seller_category_id) references seller_categories (Id)
)
    comment '셀러_2차분류';

create table sellers
(
    Id                    int not null
        primary key,
    seller_subcategory_id int not null comment '셀러정보',
    constraint FK_sellers_Id_accounts_Id
        foreign key (Id) references accounts (Id),
    constraint FK_sellers_seller_subcategory_id_seller_subcategories_Id
        foreign key (seller_subcategory_id) references seller_subcategories (Id)
)
    comment '셀러계정';

create table products
(
    Id         int auto_increment
        primary key,
    account_id int      not null comment '최초 등록자',
    seller_id  int      not null comment '셀러',
    created_at datetime not null comment '최초 등록일',
    constraint FK_products_account_id_accounts_Id
        foreign key (account_id) references accounts (Id),
    constraint FK_products_seller_id_sellers_Id
        foreign key (seller_id) references sellers (Id)
)
    comment '상품';

create table product_histories
(
    Id                    int auto_increment
        primary key,
    account_id            int            not null comment '수정자',
    product_id            int            not null comment '상품',
    name                  varchar(40)    not null comment '상품 이름',
    shipment_information  varchar(10)    not null comment '배송정보',
    price                 decimal(10, 2) not null comment '가격',
    detail_page_html      text           not null comment '상품상세페이지 HTML',
    discount_rate         decimal(5, 2)  null comment '할인률',
    discount_start_time   datetime       null comment '할인 시작일',
    discount_end_time     datetime       null comment '할인 종료일',
    is_sold               tinyint        not null comment '판매 여부',
    is_displayed          tinyint        not null comment '진열 여부',
    minimum_sell_quantity int            null comment '최소 판매수량',
    maximum_sell_quantity int            null comment '최대 판매수량',
    comment               varchar(50)    null comment '한줄 상품 설명',
    start_time            datetime       not null comment '변경 시작일',
    end_time              datetime       not null comment '변경 종료일',
    is_deleted            tinyint        not null comment '삭제 여부',
    constraint FK_product_histories_account_id_accounts_Id
        foreign key (account_id) references accounts (Id),
    constraint FK_product_histories_product_id_products_Id
        foreign key (product_id) references products (Id)
)
    comment '상품 히스토리';

create table product_images
(
    Id         int auto_increment
        primary key,
    product_id int           not null comment '상품',
    image_url  varchar(2000) not null comment '이미지 URL',
    is_main    tinyint       not null comment '대표이미지 여부',
    constraint FK_product_images_product_id_products_Id
        foreign key (product_id) references products (Id)
)
    comment '상품이미지';

create table seller_histories
(
    Id                   int auto_increment
        primary key,
    account_id           int           not null comment '수정자',
    action_status_id     int           not null comment '셀러 상태',
    seller_id            int           not null comment '셀러',
    start_time           datetime      not null comment '변경 시작일',
    end_time             datetime      not null comment '변경 종료일',
    password             varchar(60)   not null comment '비밀번호',
    seller_phone_number  varchar(11)   not null comment '셀러 전화번호',
    korean_name          varchar(23)   not null comment '상호 한글 이름',
    english_name         varchar(39)   not null comment '상호 영문 이름',
    header_office_number varchar(11)   not null comment '고객센터 전화번호',
    cs_office_hour       varchar(11)   not null comment '고객센터 운영시간',
    refund_information   text          not null comment '교환 환불 정보',
    is_deleted           tinyint       not null comment '삭제 여부',
    profile_image_url    varchar(2000) not null comment '셀러 프로필 사진 URL',
    shipment_information text          not null comment '배송정보',
    background_image_url varchar(2000) not null comment '셀러 배경 이미지 URL',
    comment              text          null comment '셀러 한줄 소개',
    detail_comment       text          not null comment '셀러 상세 소개',
    cs_nickname          varchar(20)   not null comment '고객센터 카카오톡 아이디',
    address              varchar(34)   not null comment '상호 택배 주소',
    constraint FK_seller_histories_account_id_accounts_Id
        foreign key (account_id) references accounts (Id),
    constraint FK_seller_histories_action_status_id_action_status_Id
        foreign key (action_status_id) references action_status (Id),
    constraint FK_seller_histories_seller_id_sellers_Id
        foreign key (seller_id) references sellers (Id)
)
    comment '셀러 히스토리';

create table seller_clerks
(
    Id                int auto_increment
        primary key,
    seller_id         int          not null comment '셀러',
    seller_history_id int          not null comment '셀러 히스토리',
    name              varchar(20)  not null comment '담당자 이름',
    email             varchar(320) not null comment '담당자 이메일',
    phone_number      varchar(11)  not null comment '담당자 핸드폰 번호',
    is_deleted        tinyint      not null comment '삭제 여부',
    constraint FK_seller_clerks_seller_history_id_seller_histories_Id
        foreign key (seller_history_id) references seller_histories (Id),
    constraint FK_seller_clerks_seller_id_sellers_Id
        foreign key (seller_id) references sellers (Id)
)
    comment '담당자 정보';

create table shipment_memo
(
    Id      int auto_increment
        primary key,
    content varchar(20) not null comment '내용'
)
    comment '배송 메세지';

create table shipment_status
(
    Id              int auto_increment
        primary key,
    shipment_status varchar(45) not null comment '배송 상태'
)
    comment '배송 상태';

create table sizes
(
    Id   int auto_increment
        primary key,
    size varchar(5) not null comment '크기'
)
    comment '상품사이즈';

create table product_options
(
    Id          int auto_increment
        primary key,
    product_id  int     not null comment '상품',
    size_id     int     not null comment '크기',
    color_id    int     not null comment '색상',
    is_sold_out tinyint not null comment '품절 여부',
    stock       int     null comment '재고량',
    constraint FK_product_options_color_id_colors_Id
        foreign key (color_id) references colors (Id),
    constraint FK_product_options_product_id_products_Id
        foreign key (product_id) references products (Id),
    constraint FK_product_options_size_id_sizes_Id
        foreign key (size_id) references sizes (Id)
)
    comment '상품옵션';

create table users
(
    Id    int          not null
        primary key,
    email varchar(320) not null comment '이메일',
    constraint FK_users_Id_accounts_Id
        foreign key (Id) references accounts (Id)
)
    comment '일반유저계정';

create table addresses
(
    Id      int auto_increment
        primary key,
    user_id int not null comment '유저',
    constraint FK_addresses_user_id_users_Id
        foreign key (user_id) references users (Id)
)
    comment '배송주소';

create table address_histories
(
    Id           int auto_increment
        primary key,
    address_id   int         not null comment '주소',
    start_time   datetime    not null comment '변경 시작일',
    end_time     datetime    not null comment '변경 종료일',
    name         varchar(20) not null comment '수령인',
    phone_number varchar(11) not null comment '수령인 전화번호',
    is_deleted   tinyint     not null comment '삭제 여부',
    is_defaulted tinyint     not null comment '기본 배송지 여부',
    address      varchar(34) not null comment '배송지 주소',
    constraint FK_address_histories_address_id_addresses_Id
        foreign key (address_id) references addresses (Id)
)
    comment '배송지 히스토리';

create table carts
(
    Id                int auto_increment
        primary key,
    user_id           int not null comment '유저',
    product_id        int not null comment '상품',
    product_option_id int not null comment '상품 옵션',
    constraint FK_carts_product_id_products_Id
        foreign key (product_id) references products (Id),
    constraint FK_carts_product_option_id_product_options_Id
        foreign key (product_option_id) references product_options (Id),
    constraint FK_carts_user_id_users_Id
        foreign key (user_id) references users (Id)
)
    comment '카트에 담긴 상품';

create table cart_histories
(
    Id         int auto_increment
        primary key,
    cart_id    int      not null comment '카트',
    start_time datetime not null comment '변경 시작일',
    end_time   datetime not null comment '변경 종료일',
    quantity   int      not null comment '수량',
    is_deleted tinyint  not null comment '삭제 여부',
    constraint FK_cart_histories_cart_id_carts_Id
        foreign key (cart_id) references carts (Id)
)
    comment '카트 히스토리';

create table orders
(
    Id         int auto_increment
        primary key,
    user_id    int      not null comment '유저',
    created_at datetime not null comment '주문 날짜',
    constraint FK_orders_user_id_users_Id
        foreign key (user_id) references users (Id)
)
    comment '주문';

create table order_histories
(
    Id                int auto_increment
        primary key,
    payment_status_id int            not null comment '결제 상태',
    order_id          int            not null comment '주문 번호',
    start_time        datetime       not null comment '변경 시작일',
    end_time          datetime       not null comment '변경 종료일',
    total_price       decimal(10, 2) not null comment '최종 금액',
    is_canceled       tinyint        not null comment '취소 여부',
    constraint FK_order_histories_order_id_orders_Id
        foreign key (order_id) references orders (Id),
    constraint FK_order_histories_payment_status_id_payment_status_Id
        foreign key (payment_status_id) references payment_status (Id)
)
    comment '주문 히스토리';

create table order_products
(
    Id                int auto_increment
        primary key,
    order_id          int not null comment '주문 번호',
    product_option_id int not null comment '상품 옵션',
    product_id        int not null comment '상품',
    constraint FK_order_products_order_id_orders_Id
        foreign key (order_id) references orders (Id),
    constraint FK_order_products_product_id_products_Id
        foreign key (product_id) references products (Id),
    constraint FK_order_products_product_option_id_product_options_Id
        foreign key (product_option_id) references product_options (Id)
)
    comment '주문 상품';

create table order_product_histories
(
    Id               int auto_increment
        primary key,
    order_status_id  int            not null comment '주문 상태',
    order_product_id int            not null comment '주문 상품',
    start_time       datetime       not null comment '변경 시작일',
    end_time         datetime       not null comment '변경 종료일',
    is_canceled      tinyint        not null comment '취소 여부',
    price            decimal(10, 2) not null comment '가격',
    quantity         int            not null comment '수량',
    constraint FK_order_product_histories_order_product_id_order_products_Id
        foreign key (order_product_id) references order_products (Id),
    constraint FK_order_product_histories_order_status_id_order_status_Id
        foreign key (order_status_id) references order_status (Id)
)
    comment '주문 상품 히스토리';

create table questions
(
    Id         int auto_increment
        primary key,
    product_id int      not null comment '상품',
    user_id    int      not null comment '유저',
    created_at datetime not null comment '최초 작성 날짜',
    constraint FK_questions_product_id_products_Id
        foreign key (product_id) references products (Id),
    constraint FK_questions_user_id_users_Id
        foreign key (user_id) references users (Id)
)
    comment 'Q&A 질문';

create table question_answers
(
    Id          int auto_increment
        primary key,
    question_id int      not null comment 'Q&A 질문',
    account_id  int      not null comment '최초 답변자',
    created_at  datetime not null comment '최초 작성 날짜',
    constraint FK_question_answers_account_id_accounts_Id
        foreign key (account_id) references accounts (Id),
    constraint FK_question_answers_question_id_questions_Id
        foreign key (question_id) references questions (Id)
)
    comment 'Q&A 답변';

create table question_answer_histories
(
    Id                 int auto_increment
        primary key,
    account_id         int      not null comment '답변 수정자',
    question_answer_id int      not null comment 'Q&A 답변',
    comment            text     not null comment '답변',
    start_time         datetime not null comment '변경 시작일',
    end_time           datetime not null comment '변경 종료일',
    is_deleted         tinyint  not null comment '삭제여부',
    constraint FK_question_answer_histories_account_id_accounts_Id
        foreign key (account_id) references accounts (Id),
    constraint FK_question_answer_histories_question_answer_id_question_answers
        foreign key (question_answer_id) references question_answers (Id)
)
    comment '답변 히스토리';

create table question_histories
(
    Id                   int auto_increment
        primary key,
    question_category_id int      not null comment 'Q&A 분류',
    question_id          int      not null comment 'Q&A 질문',
    start_time           datetime not null comment '변경 시작일',
    end_time             datetime not null comment '변경 종료일',
    content              text     not null comment '내용',
    is_answered          tinyint  not null comment '처리 상태',
    is_deleted           tinyint  not null comment '삭제 여부',
    constraint FK_question_histories_question_category_id_question_categories_I
        foreign key (question_category_id) references question_categories (Id),
    constraint FK_question_histories_question_id_questions_Id
        foreign key (question_id) references questions (Id)
)
    comment 'Q&A 히스토리';

create table shipments
(
    Id                 int auto_increment
        primary key,
    order_id           int         not null comment '주문 번호',
    order_product_id   int         not null comment '주문 상품',
    address_id         int         not null comment '배송지 주소',
    shipment_status_id int         not null comment '배송 상태',
    shipment_memo_id   int         not null comment '배송 메세지',
    message            varchar(20) null comment '배송메세지 직접입력',
    start_time         datetime    null comment '배송 시작',
    end_time           datetime    null comment '배송 종료',
    constraint FK_shipments_address_id_addresses_Id
        foreign key (address_id) references addresses (Id),
    constraint FK_shipments_order_id_orders_Id
        foreign key (order_id) references orders (Id),
    constraint FK_shipments_order_product_id_order_products_Id
        foreign key (order_product_id) references order_products (Id),
    constraint FK_shipments_shipment_memo_id_shipment_memo_Id
        foreign key (shipment_memo_id) references shipment_memo (Id),
    constraint FK_shipments_shipment_status_id_shipment_status_Id
        foreign key (shipment_status_id) references shipment_status (Id)
)
    comment '배송 정보';

create table social_user
(
    Id            int auto_increment
        primary key,
    user_id       int         not null comment '유저',
    name          varchar(10) not null comment '소셜 이름',
    social_number int         not null comment '소셜 회원번호',
    constraint FK_social_user_user_id_users_Id
        foreign key (user_id) references users (Id)
)
    comment '소셜 유저';

create table social_user_histories
(
    Id             int auto_increment
        primary key,
    social_user_id int         not null comment '소셜 유저',
    start_time     datetime    not null comment '변경 시작일',
    end_time       datetime    not null comment '변경 종료일',
    is_deleted     tinyint     not null comment '삭제 여부',
    phone_number   varchar(11) not null comment '핸드폰 번호',
    constraint FK_social_user_histories_social_user_id_social_user_Id
        foreign key (social_user_id) references social_user (Id)
)
    comment '소셜 유저 히스토리';

create table user_histories
(
    Id         int auto_increment
        primary key,
    user_id    int         not null comment '유저',
    start_time datetime    not null comment '변경 시작일',
    end_time   datetime    not null comment '변경 종료일',
    is_deleted tinyint     not null comment '삭제 여부',
    password   varchar(60) not null comment '비밀번호',
    constraint FK_user_histories_user_id_users_Id
        foreign key (user_id) references users (Id)
)
    comment '일반 유저 히스토리';


