<template>
  <div id="app">
    <router-view/>
  </div>
</template>


<script>
  import SideBar from "./views/sidebar/SideBar";
export default {
  name: 'App',
  components:{
    SideBar,
  }
}
</script>

<style>
@import "static/main.css";
</style>
