<template>

  <div  style="background: white;height: 100vh">
    <el-row  >
      <el-col :offset="5" :span="15" style="margin-top: 20%; " >
        <el-form :model="form_data" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm"
                 style="box-shadow: 5px 5px 20px rgba(100,100,100,0.5);padding: 15px;border-radius: 10px"
        >
          <el-tabs v-model="active_tab_name" >
            <el-tab-pane label="立即登录" name="login_tab">
              <el-form-item label="用户账号" prop="account">
                <el-input v-model="form_data.account"></el-input>
              </el-form-item>
              <el-form-item label="用户密码" prop="password">
                <el-input v-model="form_data.password" show-password></el-input>
              </el-form-item>

              <el-form-item >
                <el-button type="primary" @click="user_login_action">登录</el-button>
              </el-form-item>
            </el-tab-pane>

            <el-tab-pane label="立即注册" name="register_tag">
              <el-form-item label="邮箱账号" prop="account">
                <el-input v-model="form_data.account"></el-input>
              </el-form-item>
              <el-form-item label="请输入密码" prop="password">
                <el-input v-model="form_data.password"></el-input>
              </el-form-item>
              <el-form-item label="请确认密码" prop="sec_password">
                <el-input v-model="form_data.sec_password"></el-input>
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
    export default {
        name: "Login",
      data(){
          return{
            form_data:{account:'123',password:'123',sec_password:''},
            rules:{
              account:[
                {require:true, message:'请输入账号',trigger:'blur'}
              ],
              password:[
                {require:true, message:'请输入密码',trigger:'blur'},
                {min: 6, max: 24, message: "密码长度在6 到 24位", trigger: 'blur'}
              ]
            },

            active_tab_name: 'login_tab'
          }
      },
      methods:{
        user_login_action(){

        },
        user_register_action(){

        }

      }
    }

</script>

<style scoped>
 *{
   background-color: black;
 }
</style>
