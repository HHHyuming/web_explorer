import Vue from 'vue'
import Router from 'vue-router'


Vue.use(Router)


let routes = [
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
]



export default new Router({
  routes
})
