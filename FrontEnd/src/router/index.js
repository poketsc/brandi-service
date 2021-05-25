import Vue from 'vue'
import Router from 'vue-router'

import Main from '@/service/Main/Main'
import Layout from '@/service/Layout'
import Detail from '@/service/Detail/Detail'
import Login from '@/service/Login/Login'
import SignUp from '@/service/SignUp/SignUp'
import CategoryMain from '@/service/Category/CategoryMain'
import CategoryProductList from '@/service/Category/ProductList'

// import VueAgile from "vue-agile";
// import AdminFrame from "../BrandiAdmin/Components/AdminFrame.vue";
// import ProductRegistration from "../BrandiAdmin/ProductRegistration/ProductRegistration.vue";
import Order from '@/service/Order/Order'
import Event from '@/service/Event/Event'
import EventDetail from '@/service/Event/EventDetail'
// import Footer from "@/service/Components/Footer.vue";
// import ProductManagement from "../BrandiAdmin/ProductManagemnet/ProductManagement.vue";
import Mypage from '@/service/Mypage/Mypage'
import OrderList from '@/service/Mypage/OrderList'
import Coupon from '@/service/Mypage/Coupon'
import Point from '@/service/Mypage/Point'
import QnAList from '@/service/Mypage/QnAList'
// import OrderManagement from "../BrandiAdmin/OrderManagement/OrderManagement.vue";
import OrderDetail from '@/service/OrderDetail/OrderDetail'
// import ProductDetail from "../BrandiAdmin/ProductDetail/ProductDetail.vue";
// import UserManagement from "../BrandiAdmin/UserManagement/UserManagement.vue";
import NetworkError from '@/service/Components/NetworkError'
import NotFound from '@/service/Components/NotFound'

// start
import Cart from '@/service/Cart/Cart'

Vue.use(Router)
export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      component: Layout,
      children: [
        {
          path: 'main',
          component: Main
        },
        {
          path: 'category',
          component: CategoryMain,
          children: [
            {
              path: '',
              component: CategoryProductList
            }
          ]
        },
        {
          path: '/detail/:id',
          component: Detail
        },
        {
          path: '/login',
          component: Login
        },
        {
          path: '/signup',
          component: SignUp
        },
        {
          path: '/order',
          component: Order
        },
        {
          path: '/event',
          component: Event,
          name: 'event'
        },
        {
          path: '/event/:no',
          component: EventDetail,
          name: 'eventDetail'
        },
        {
          path: '/cart',
          component: Cart,
          name: 'cart'
        },
        {
          path: '/mypage',
          redirect: '/mypage/orderList',
          component: Mypage,
          name: Mypage,
          children: [
            {
              path: '',
              redirect: '/mypage/orderList',
              component: OrderList,
              name: 'orderList'
            },
            {
              path: 'orderList',
              component: OrderList,
              name: 'orderList'
            },
            {
              path: 'point',
              component: Point,
              name: 'point'
            },
            {
              path: 'coupon',
              component: Coupon,
              name: 'coupon'
            },
            {
              path: 'qna',
              component: QnAList,
              name: 'qna'
            },
            {
              path: 'faq',
              component: Mypage,
              name: 'faq'
            }
          ]
        },
        {
          path: '/order/detail',
          component: OrderDetail
        },
        {
          path: '/order/detail/:no',
          component: OrderDetail
        },
        // 주문 상세 보기
        {
          path: '/mypage/orderDetail/:no',
          component: OrderDetail
        },
        {
          // 초기 url을 main으로 적용
          path: '/',
          redirect: '/main'
        },
        {
          path: '*',
          redirect: '/error/404'
        },
        {
          path: '/error/400',
          component: NetworkError
        },
        {
          path: '/error/404',
          component: NotFound
        }
      ]
    }
    // {
    //   path: '/main',
    //   component: Main
    // },
    // {
    //   path: '/detail/:id',
    //   component: Detail
    // },
    // {
    //   path: '/login',
    //   component: Login
    // },
    // {
    //   path: '/signup',
    //   component: SignUp
    // },
    // {
    //   path: '/order',
    //   component: Order
    // },
    // {
    //   path: '/event',
    //   component: Event,
    //   name: 'event'
    // },
    // {
    //   path: '/event/:no',
    //   component: EventDetail,
    //   name: 'eventDetail'
    // },
    // {
    //   path: '/mypage',
    //   redirect: '/mypage/orderList',
    //   component: Mypage,
    //   name: Mypage,
    //   children: [
    //     {
    //       path: '',
    //       redirect: '/mypage/orderList',
    //       component: OrderList,
    //       name: 'orderList'
    //     },
    //     {
    //       path: 'orderList',
    //       component: OrderList,
    //       name: 'orderList'
    //     },
    //     {
    //       path: 'point',
    //       component: Point,
    //       name: 'point'
    //     },
    //     {
    //       path: 'coupon',
    //       component: Coupon,
    //       name: 'coupon'
    //     },
    //     {
    //       path: 'qna',
    //       component: Mypage,
    //       name: 'qna'
    //     },
    //     {
    //       path: 'faq',
    //       component: Mypage,
    //       name: 'faq'
    //     }
    //   ]
    // },
    // {
    //   path: '/order/detail',
    //   component: OrderDetail
    // },
    // {
    //   // 초기 url을 main으로 적용
    //   path: '/',
    //   redirect: '/main'
    // },
    // {
    //   path: '*',
    //   redirect: '/error/404'
    // },
    // {
    //   path: '/error/400',
    //   component: NetworkError
    // },
    // {
    //   path: '/error/404',
    //   component: NotFound
    // },
    // 회원가입
    // 어드민 내부
  ]
})
