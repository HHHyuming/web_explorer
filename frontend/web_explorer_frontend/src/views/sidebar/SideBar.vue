<template>
<div>

  <el-container>
    <el-aside width="200px">
      <el-row>
      <el-col align="left">
          <el-menu
            default-active="1"
            @open="handleOpen"
            @close="handleClose"
            background-color="#545c64"
            active-text-color="#ffd04b"
            text-color="#fff"
            router
          >

            <el-menu-item index="1" route="explorer">
              <i class="el-icon-setting"></i>
              <span slot="title">资源管理器</span>
            </el-menu-item>

            <el-menu-item index="2" route="search">
              <i class="el-icon-setting"></i>
              <span slot="title">搜索引擎</span>
            </el-menu-item>

          </el-menu>
      </el-col>
      </el-row>

    </el-aside>
    <el-main>
      <router-view></router-view>
    </el-main>
  </el-container>


</div>
</template>

<script>
    export default {
        name: "SideBar",
        data(){
          return{

          }
        },
        methods:{
          handleOpen(key, keyPath) {
            console.log('open-----')
            console.log(key, keyPath);
          },
          handleClose(key, keyPath) {
            console.log('close----')
            console.log(key, keyPath);
          }
        }
    }
</script>

<style scoped>

  .el-aside {
    height: 100vh;
    text-align: center;
    background-color:#545c64;
  }

  .el-main {
    border: 1px solid red;
  }

</style>
