<template>
<div >
<!--  操作栏-->
  <div style="box-shadow: 5px 5px 3px rgba(100, 100, 100, .3); padding: 10px; line-height: 3em">
    <el-row >
      <el-col :span="20">
        <el-button type="primary" size="small" @click="add_file_dialog = true">新增文件夹</el-button>
        <el-button size="small" :disabled="edit_disabled" ref="edit_file_node">编辑文件夹</el-button>
        <el-button type="danger" size="mini" @click="delete_file">删除</el-button>
        <el-button  size="small" @click="up_load_file_dialog = true">上传文件</el-button>

        <el-dropdown @command="drop_down_command">
          <el-button type="primary" size="small">
            更多操作<i class="el-icon-arrow-down el-icon--right"></i>
          </el-button>
          <el-dropdown-menu slot="dropdown" >
            <el-dropdown-item command="a">移动</el-dropdown-item>
            <el-dropdown-item command="b">下载</el-dropdown-item>
            <el-dropdown-item command="c">权限</el-dropdown-item>
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
      border
      @selection-change="handleSelectionChange">
      <el-table-column
        type="selection"
        width="55">
      </el-table-column>
      <el-table-column
        label="序号"
        width="120"
      prop="no">
<!--        <template slot-scope="scope">{{ scope.row.date }}</template>-->
      </el-table-column>
      <el-table-column
        prop="file_name"
        label="名称"
        width="120"

        show-overflow-tooltip>
      </el-table-column>
      <el-table-column
        prop="update_time"
        label="修改日期"
        >
      </el-table-column>

      <el-table-column
        prop="file_type"
        label="类型"
      >
      </el-table-column>
      <el-table-column
        prop="file_size"
        label="大小"
      >
        <template slot-scope="scope">{{scope.row.file_size | size_convert}}</template>
      </el-table-column>
      <el-table-column
        prop="create_time"
        label="创建日期"
      >
      </el-table-column>
      <el-table-column
        prop="author_name"
        label="作者"
      >
      </el-table-column>
      <el-table-column
        prop="desc_content"
        label="描述"
        show-overflow-tooltip
      >
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
      <el-button type="primary"  @click="submit_add_file">提 交</el-button>
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
      <el-form :model="up_load_form_data" label-position="top">
        <el-form-item label="文件路径">

          <div class="block">
            <el-cascader
              v-model="up_load_form_data.file_path"
              :options="this.$store.state.cascade_dir"
              @change="handleChangePath"></el-cascader>
          </div>

        </el-form-item>

        <el-form-item label="导入文件">
          <el-upload
            class="upload-demo"
            ref="upload"
            drag
            action="http://127.0.0.1:5000/explorer/upload_file"
            multiple
            :auto-upload="false"
            :headers="upload_headers"
            :file-list="upload_file_list"
            :on-change="upload_change"
            :on-remove="upload_remove"
            :data="{path:multipleSelection}"
          >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          </el-upload>
        </el-form-item>
        <el-button type="primary" :loading="loading" @click="upload_file">提 交</el-button>
        <el-button @click="up_load_file_dialog = false">取 消</el-button>
      </el-form>
    </el-card>

  </el-drawer>
</div>

</template>

<script>
  import {get_usr_dir_cascade, add_file, index_data,
    delete_file, upload_file, download_file
  } from "@/http/explorer";

  export default {
      name: "explorer",
      data(){
        return {
          filter_select_value:[],
          add_file_value:[],
          filter_value:[],

          upload_file_list:[],
          upload_headers:{Authorization: ''},
          up_load_form_data:{file_path:''},
          up_load_file_dialog: false,
          loading:false,

          add_file_form_data:
            {file_path:'', file_name:'',desc:''},
          add_file_dialog:false,

          edit_disabled: true,

          change_path:null,

          tableData: [],
          multipleSelection: []
        }
        },

      methods: {
        upload_remove(file, fileList){
          this.upload_file_list = fileList
        },
        upload_change(file, fileList){
          this.upload_file_list = fileList
        },
        handleSelectionChange(val) {
          // table 选中条目
          // console.log(val);
          this.multipleSelection = val;
        },
        filter_select_handler(val){
          // 过滤条
          // console.log(val)
          this.filter_select_value = val;
        },
        handleChangePath(cascade_path){
          // console.log(cascade_path)
          this.change_path = cascade_path

        },
        submit_add_file() {
        //  新增文件夹
          this.add_file_form_data.file_path = this.add_file_value;
          const file_path = this.add_file_form_data.file_path;
          const file_name = this.add_file_form_data.file_name;
          const desc = this.add_file_form_data.desc;
          console.log(file_path)
          add_file(file_path, file_name, desc).then( result => {
            this.get_index_data()
          }).catch(reason => {
            console.log(reason)
          })

        },
        get_cascade_data(){
          // 获取选项卡级联数据
          const user_name = window.sessionStorage.getItem('user_name')
          get_usr_dir_cascade(user_name).then( result => {
            const data = result.data
            this.$store.commit('change_cascade', data.data)


          }).catch( error => {
            console.log(error)
          })
        },
        get_index_data(){
          index_data().then( result => {
            console.log(result)
            if (result.data.code !== 200){
              this.$message.error(result.data.msg)
            }
            else{
              let response_data = result.data.data;
              for (let index in response_data){
                response_data[index]['no'] = parseInt(index) + 1
              }
              this.tableData = response_data
              console.log(this.tableData)
            }

          }).catch( reason => {
            console.log(reason)
          })
          this.get_cascade_data()
        },
        delete_file(){
          let delete_list = this.multipleSelection;
          if(delete_file.length === 0){
            return
          }
          delete_file(delete_list).then( result => {

            if (result.data.code !== 200){
              console.log(result);
            }
            this.get_index_data()
          }).catch( reason => {
            console.log(reason)
          })

        },

        upload_file(){

          this.upload_headers.Authorization = window.sessionStorage.getItem('token');
          if(this.upload_headers.Authorization){

            let formData = new FormData();
            // console.log(this.upload_file_list);

            this.upload_file_list.forEach( file =>{
              formData.append('file', file.raw)
            });

            formData.append('path',this.change_path);
            upload_file(formData).then( result => {
              console.log(result)
            }).catch(reason => {
              console.log(reason)
            })
          }
          else{
            console.log('上传失败')
          }

        },
        drop_down_command(command){
          console.log('xxxxxxx');
          if(command === 'b'){
            this.download_file()
          }
        },
        download_file(){

          download_file(this.multipleSelection).then( result => {
            console.log(result)
          }).catch( reason => {
            console.log(reason)
          })
        },
      },

      mounted() {

      //  获取首页数据
        this.get_index_data();
      //  获取级联目录 // 过滤搜索
        this.get_cascade_data()

      },
      watch: {

      },
    filters:{
        size_convert(size){
          let actual_size = parseInt(size) / 1024;
          return actual_size + 'KB'
        }
    }
    }
</script>

<style scoped>


</style>
