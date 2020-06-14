import Vue from 'vue'
import Router from 'vue-router'


Vue.use(Router);


let routes = [
  {
    path: '/login',
    name: 'login',
    component: resolve => require(['@/views/login/Login'], resolve)
  },
  {
    path: '/',
    component: resolve => require(['@/views/sidebar/SideBar'], resolve),
    children:[
      {
        path: '/',
        redirect: '/explorer',
      },
      {
        path:'explorer',
        name: 'Explorer',
        component: resolve => require(['@/views/master/Explorer'] ,resolve)

      },
      {
        path:'search',
        name: 'Search',
        component: resolve => require(['@/views/master/Search'], resolve)

      }
    ]
  }
];

const router = new Router({
  routes
});

router.beforeEach((to, from ,next) => {

  if (to.path.indexOf("explorer") >= 0){
    if (window.sessionStorage.getItem("token")){
      next()
    }else{
      next('login');

    }
  }else{

    next()

  }
});

export default router
