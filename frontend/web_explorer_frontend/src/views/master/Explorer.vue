<template>
<div >
<!--  操作栏-->
  <div style="box-shadow: 5px 5px 3px rgba(100, 100, 100, .3); padding: 10px; line-height: 3em">
    <el-row >
      <el-col :span="20">
        <el-button type="primary" size="small" @click="add_file_dialog = true">新增文件夹</el-button>
        <el-button size="small" :disabled="edit_disabled" ref="edit_file_node">编辑文件夹</el-button>
        <el-button type="danger" size="mini">删除</el-button>
        <el-button  size="small" @click="up_load_file_dialog = true">上传文件</el-button>
        <el-dropdown>
          <el-button type="primary" size="small">
            更多操作<i class="el-icon-arrow-down el-icon--right"></i>
          </el-button>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item>移动</el-dropdown-item>
            <el-dropdown-item>下载</el-dropdown-item>
            <el-dropdown-item>权限</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </el-col>
      <el-col :span="4" align="right" >
        <i class="iconfont icon-qiehuan" style="font-size: 20px;color: deepskyblue"></i>
      </el-col>
    </el-row>
  </div>
  <!--  过滤栏-->

  <div>
    <el-row style="box-shadow: 5px 5px 3px rgba(100, 100, 100, .3); padding: 10px; line-height: 3em; margin-top: 10px">
      <el-col :span="14">
        <div class="block" >
<!--          <span class="demonstration">快速定位文件夹</span>-->
          <el-cascader
            v-model="filter_value"
            :options="this.$store.state.cascade_dir"
            :props="{ expandTrigger: 'hover' }"
            @change="filter_select_handler"
            style="width: 350px"
          ></el-cascader>
        </div>
      </el-col>
      <el-col :span="10" align="left">
        <div>
          <el-input placeholder="请输入内容"  class="input-with-select">

            <el-button slot="append" icon="el-icon-search"></el-button>
          </el-input>
        </div>
      </el-col>
    </el-row>
  </div>

<!--  table content-->
  <div style="box-shadow: 5px 5px 3px rgba(100, 100, 100, .3); padding: 10px; margin-top: 10px">

    <el-table
      ref="multipleTable"
      :data="tableData"
      tooltip-effect="dark"
      style="width: 100%"
      @selection-change="handleSelectionChange">
      <el-table-column
        type="selection"
        width="55">
      </el-table-column>
      <el-table-column
        label="日期"
        width="120">
        <template slot-scope="scope">{{ scope.row.date }}</template>
      </el-table-column>
      <el-table-column
        prop="name"
        label="姓名"
        width="120">
      </el-table-column>
      <el-table-column
        prop="address"
        label="地址"
        show-overflow-tooltip>
      </el-table-column>
    </el-table>



  </div>

<!--  新增文件 dialog-->
  <el-drawer

    :visible.sync="add_file_dialog"
    :with-header="false"
    :modal="false"
  >
    <el-card style="height: 100vh">
      <div slot="header" >
        <h3>新增文件夹</h3>
      </div>
    <el-form :model="add_file_form_data" label-position="top">
      <el-form-item label="文件路径">


        <div class="block">
          <el-cascader
            v-model="add_file_value"
            :options="this.$store.state.cascade_dir"
            @change="handleChangePath"></el-cascader>
        </div>


      </el-form-item>

      <el-form-item label="文件夹名称" required :rules="[{require:true,message:'此项必填'}]">
        <el-input v-model="add_file_form_data.file_name"></el-input>
      </el-form-item>

      <el-form-item label="备注说明" >
        <el-input
          type="textarea"
          :rows="2"
          placeholder="请输入内容"
          v-model="add_file_form_data.desc"></el-input>
      </el-form-item>
      <el-button type="primary" :loading="loading" @click="submit_add_file">提 交</el-button>
      <el-button @click="add_file_dialog = false">取 消</el-button>

    </el-form>

    </el-card>

  </el-drawer>


  <!--  上传文件 dialog-->
  <el-drawer

    :visible.sync="up_load_file_dialog"
    :with-header="false"
    :modal="false"
  >
    <el-card style="height: 100vh">
      <div slot="header" >
        <span>上传文件</span>
      </div>
      <el-form :model="up_load_file_dialog" label-position="top">
        <el-form-item label="文件路径">
          <el-input v-model="up_load_file_dialog.file_path"></el-input>
        </el-form-item>

        <el-form-item label="导入文件">
          <el-upload
            class="upload-demo"
            drag
            action="https://jsonplaceholder.typicode.com/posts/"
            multiple
          >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          </el-upload>
        </el-form-item>
        <el-button type="primary" :loading="loading">提 交</el-button>
        <el-button @click="up_load_file_dialog = false">取 消</el-button>
      </el-form>
    </el-card>

  </el-drawer>
</div>

</template>

<script>
  import {get_usr_dir_cascade, add_file} from "@/http/explorer";

  export default {
      name: "explorer",
      data(){
        return {
          filter_select_value:[],
          add_file_value:[],
          filter_value:[],
          up_load_form_data:{},
          up_load_file_dialog: false,
          loading:false,
          add_file_form_data:{file_path:'',
          file_name:'',desc:''},
          add_file_dialog:false,
          edit_disabled: true,
          value:null,
          options:null,
          login_form:{},
          register_form:{},
          path_options:[

          ],

          tableData: [{
            date: '2016-05-03',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1518 弄'
          }, {
            date: '2016-05-02',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1518 弄'
          }, {
            date: '2016-05-04',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1518 弄'
          }, {
            date: '2016-05-01',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1518 弄'
          }, {
            date: '2016-05-08',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1518 弄'
          }, {
            date: '2016-05-06',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1518 弄'
          }, {
            date: '2016-05-07',
            name: '王小虎',
            address: '上海市普陀区金沙江路 1518 弄'
          }],
          multipleSelection: []
        }
        },

      methods: {
        toggleSelection(rows) {
          if (rows) {
            rows.forEach(row => {
              this.$refs.multipleTable.toggleRowSelection(row);
            });
          } else {
            this.$refs.multipleTable.clearSelection();
          }
        },
        handleSelectionChange(val) {
          console.log(val)
          this.multipleSelection = val;
        },
        filter_select_handler(val){
          this.filter_select_value = val;
        },
        handleChangePath(cascade_path){
          console.log(cascade_path)

        },
        submit_add_file() {
        //  新增文件夹
          this.add_file_form_data.file_path = this.add_file_value
          const file_path = this.add_file_form_data.file_path
          const file_name = this.add_file_form_data.file_name
          const desc = this.add_file_form_data.desc
          add_file(file_path, file_name, desc).then( response =>{

          }).catch( error =>{
            console.log(error)
          })
        },
        get_cascade_data(){
          const user_name = window.sessionStorage.getItem('user_name')
          get_usr_dir_cascade(user_name).then( result => {
            const data = result.data

            this.$store.commit('change_cascade', data.data)
          }).catch( error => {
            console.log(error)
          })
        },
      },

      mounted() {

      //  获取首页数据
      //  获取级联目录
        this.get_cascade_data()
        // 过滤搜索

      },
      watch: {

      },
    }
</script>

<style scoped>


</style>
