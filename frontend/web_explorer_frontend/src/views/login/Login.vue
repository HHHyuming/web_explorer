<template>
  <div  style="background: white;height: 100vh">
    <el-row  >
      <el-col :offset="7" :span="10" style="margin-top: 15%; " >
        <el-form :model="form_data" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm"
                 style="box-shadow: 5px 5px 20px rgba(100,100,100,0.5);padding: 15px;border-radius: 10px"
        >
          <el-tabs v-model="active_tab_name" >
            <el-tab-pane label="立即登录" name="login_tab">
              <el-form-item label="用户账号" prop="account">
                <el-input v-model="form_data.login_form_data.account"></el-input>
              </el-form-item>
              <el-form-item label="用户密码" prop="password">
                <el-input v-model="form_data.login_form_data.password" show-password></el-input>
              </el-form-item>

              <el-form-item >
                <el-button type="primary" @click="user_login_action" @keyup.enter.native="user_login_action">登录</el-button>
              </el-form-item>
            </el-tab-pane>

            <el-tab-pane label="立即注册" name="register_tag">
              <el-form-item label="邮箱账号" prop="account">
                <el-input v-model="form_data.register_form_data.account"></el-input>
              </el-form-item>
              <el-form-item label="请输入密码" prop="password">
                <el-input v-model="form_data.register_form_data.password"></el-input>
              </el-form-item>
              <el-form-item label="请确认密码" prop="sec_password">
                <el-input v-model="form_data.register_form_data.sec_password"></el-input>
              </el-form-item>

              <el-form-item >
                <el-button type="primary" @click="user_register_action">注册</el-button>
              </el-form-item>
            </el-tab-pane>

          </el-tabs>
        </el-form>
      </el-col>
    </el-row>

  </div>
</template>

<script>
  import {user_login, user_register} from '@/http/user'
  import axios from 'axios'
    export default {
        name: "Login",
      data(){
          return {
            active_tab_name: 'login_tab',
            form_data:{login_form_data:{account:'',password:''},
              register_form_data : {account: '', password:'', sec_password:''},},
            rules:{
              account:[
                {require:true, message:'请输入账号',trigger:'blur'}
              ],
              password:[
                {require:true, message:'请输入密码',trigger:'blur'},
                {min: 6, max: 24, message: "密码长度在6 到 24位", trigger: 'blur'}
              ]
            },
          }
      },
      methods:{
        user_login_action(){
          console.log('xxx')
          let user_name = this.form_data.login_form_data.account;
          let user_password = this.form_data.login_form_data.password;
          // 参数校验
          // 登录请求

          if (user_name === "" || user_password === ""){
            return
          }
          user_login(user_name, user_password).then(result => {
            let data = result.data
            let token = data.data.token
            console.log('设置')
            window.sessionStorage.setItem('token',token)
            console.log('跳')
            this.$router.replace({name: 'Explorer'})
          }).catch( error =>{
            console.log(error)
          })

        },
        user_register_action(){

          let user_name = this.form_data.register_form_data.account;
          let user_password = this.form_data.register_form_data.password;
          let sec_password = this.form_data.register_form_data.sec_password;
          // 参数校验
          if (user_password !== sec_password){
            this.$message({
              message: '密码不一致，请重新输入',
              type: 'error'
            });
            return
          }
          // 注册请求
          user_register(user_name, user_password, sec_password).then((response) => {
            console.log(response)
          }).catch((reason => {
            console.log(reason)
          }))
        },
      },
      mounted() {

      }
    }
</script>

<style scoped>

</style>
