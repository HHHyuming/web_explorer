<template>
<<<<<<< HEAD
<div class="login-demo">
  <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
    <el-form-item label="活动名称" prop="name">
      <el-input v-model="ruleForm.name"></el-input>
    </el-form-item>
    <el-form-item label="活动区域" prop="region">
      <el-select v-model="ruleForm.region" placeholder="请选择活动区域">
        <el-option label="区域一" value="shanghai"></el-option>
        <el-option label="区域二" value="beijing"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="活动时间" required>
      <el-col :span="11">
        <el-form-item prop="date1">
          <el-date-picker type="date" placeholder="选择日期" v-model="ruleForm.date1" style="width: 100%;"></el-date-picker>
        </el-form-item>
      </el-col>
      <el-col class="line" :span="2">-</el-col>
      <el-col :span="11">
        <el-form-item prop="date2">
          <el-time-picker placeholder="选择时间" v-model="ruleForm.date2" style="width: 100%;"></el-time-picker>
        </el-form-item>
      </el-col>
    </el-form-item>
    <el-form-item label="即时配送" prop="delivery">
      <el-switch v-model="ruleForm.delivery"></el-switch>
    </el-form-item>
    <el-form-item label="活动性质" prop="type">
      <el-checkbox-group v-model="ruleForm.type">
        <el-checkbox label="美食/餐厅线上活动" name="type"></el-checkbox>
        <el-checkbox label="地推活动" name="type"></el-checkbox>
        <el-checkbox label="线下主题活动" name="type"></el-checkbox>
        <el-checkbox label="单纯品牌曝光" name="type"></el-checkbox>
      </el-checkbox-group>
    </el-form-item>
    <el-form-item label="特殊资源" prop="resource">
      <el-radio-group v-model="ruleForm.resource">
        <el-radio label="线上品牌商赞助"></el-radio>
        <el-radio label="线下场地免费"></el-radio>
      </el-radio-group>
    </el-form-item>
    <el-form-item label="活动形式" prop="desc">
      <el-input type="textarea" v-model="ruleForm.desc"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>
      <el-button @click="resetForm('ruleForm')">重置</el-button>
    </el-form-item>
  </el-form>
</div>
</template>

<script>
  export default {
    name: 'login',
    data() {
      return {
        ruleForm: {
          name: '',
          region: '',
          date1: '',
          date2: '',
          delivery: false,
          type: [],
          resource: '',
          desc: ''
        },
        rules: {
          name: [
            { required: true, message: '请输入活动名称', trigger: 'blur' },
            { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
          ],
          region: [
            { required: true, message: '请选择活动区域', trigger: 'change' }
          ],
          date1: [
            { type: 'date', required: true, message: '请选择日期', trigger: 'change' }
          ],
          date2: [
            { type: 'date', required: true, message: '请选择时间', trigger: 'change' }
          ],
          type: [
            { type: 'array', required: true, message: '请至少选择一个活动性质', trigger: 'change' }
          ],
          resource: [
            { required: true, message: '请选择活动资源', trigger: 'change' }
          ],
          desc: [
            { required: true, message: '请填写活动形式', trigger: 'blur' }
          ]
        }
      };
    },
    methods: {
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            alert('submit!');
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
=======
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
>>>>>>> afa026a40f7caebc98954ccf23faef836f470adb
      }
    }
  }
</script>

<style scoped>
 *{
   background-color: black;
 }
</style>
