<template xmlns="http://www.w3.org/1999/html">
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
            :options="cascade_data"
            @change="filter_select_handler"
            :props="{ checkStrictly: true }"
            :clearable="true"
            style="width: 350px"
          ></el-cascader>
        </div>

      </el-col>
      <el-col :span="10" align="left">
        <div>
          <el-input placeholder="请输入内容" v-model="search_value" class="input-with-select">

            <el-button slot="append" icon="el-icon-search" @click="start_search"></el-button>
          </el-input>
        </div>
      </el-col>
    </el-row>
  </div>

<!--  table content-->
  <div style="box-shadow: 5px 5px 3px rgba(100, 100, 100, .3); padding: 10px; margin-top: 10px">

    <el-table
      v-loading="table_loading"
      ref="multipleTable"
      :data="tableData"
      tooltip-effect="dark"
      style="width: 100%"
      border
      @selection-change="handleSelectionChange">
      <el-table-column
        type="selection"
        width="55" align="center">
      </el-table-column>
      <el-table-column
        label="序号"
        width="55"
      prop="no" align="center">
<!--        <template slot-scope="scope">{{ scope.row.date }}</template>-->
      </el-table-column>
      <el-table-column
        prop="file_name"
        label="名称"
        width="120"
        align="center"
        show-overflow-tooltip>
        <template slot-scope="scope">
          <div>
            <i :class="'iconfont ' + file_type_map[scope.row.file_type]"  ></i>

            <a v-if="scope.row.file_type !== 'dir' " :href="current_ip + '/' + current_user+ '/' +scope.row.hash_name " class="text-style" v-html="filter_data(scope.row.file_name)"></a>
            <span v-else class="text-style" style="cursor: pointer" @click="change_table_data(scope.row.path)" v-html="filter_data(scope.row.file_name)"></span>
          </div>
        </template>
      </el-table-column >
      <el-table-column
        prop="update_time"
        label="修改日期"
        align="center"
        >
      </el-table-column>

      <el-table-column
        prop="file_type"
        label="类型"
        align="center"
      >
        <template slot-scope="scope">
          {{scope.row.file_type === 'dir' ? '文件夹' : scope.row.file_type}}
        </template>
      </el-table-column>
      <el-table-column
        prop="file_size"
        label="大小"
        align="center"
      >
        <template slot-scope="scope">{{scope.row.file_type === 'dir' ? ('-') : size_convert(scope.row.file_size) }}</template>
      </el-table-column>
      <el-table-column
        prop="create_time"
        label="创建日期"
        align="center"
      >
      </el-table-column>
      <el-table-column
        prop="author_name"
        label="作者"
        align="center"
      >
      </el-table-column>
      <el-table-column
        prop="desc_content"
        label="描述"
        show-overflow-tooltip
        align="center"
        width="50"
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
            :options="cascade_data"
            @change="filter_select_handler"
            :props="{ checkStrictly: true }"
            :clearable="true"
          ></el-cascader>
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
      <el-button type="primary"  @click="submit_add_file"
                 element-loading-text="加载中..."
                 element-loading-spinner="el-icon-loading"
                 v-loading="submit_loading">提 交</el-button>
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
              :options="cascade_data"
              @change="handleChangePath"
              :props="{ checkStrictly: true }"
              :clearable="true"
            ></el-cascader>

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
        <el-button type="primary" :loading="loading"
                   @click="upload_file"
                   element-loading-text="加载中..."
                   element-loading-spinner="el-icon-loading"
                   v-loading="upload_loading">提 交</el-button>
        <el-button @click="up_load_file_dialog = false">取 消</el-button>
      </el-form>
    </el-card>

  </el-drawer>
</div>

</template>

<script>
  import {get_usr_dir_cascade, add_file, index_data,
    delete_file, upload_file, download_file,new_cascade,change_directory,search_content
  } from "@/http/explorer";
  import {dateFormat} from "@/common/date"
  export default {
      name: "explorer",
      data(){
        return {
          upload_loading:false,
          submit_loading:false,
          table_loading:false,
          search_value:'',
          current_user:window.sessionStorage.getItem('user_name'),
          current_ip:'http://127.0.0.1:5000/static/',
          file_type_map: {dir:'icon-wenjianjia dir',txt:'icon-txt1 txt', mp3:
          'icon-Music mp3', mp4: 'icon-avi mp4',md:'icon-MD md',js:'icon-js js',sql:'icon-SQLshengjiwenjian sql'},
          cascade_data:[],
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

          change_path:[],

          tableData: [],
          multipleSelection: [],

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
            this.change_table_data(val)
            console.log(this.tableData)
        },
        handleChangePath(cascade_path){
          // console.log(cascade_path)
          this.change_path = cascade_path

        },
        submit_add_file() {
          this.submit_loading = true;
        //  新增文件夹
          this.add_file_form_data.file_path = this.add_file_value;
          const file_path = this.add_file_form_data.file_path;
          const file_name = this.add_file_form_data.file_name;
          const desc = this.add_file_form_data.desc;
          console.log(file_path)
          add_file(file_path, file_name, desc).then( result => {
            this.get_index_data()
            this.submit_loading = false
            this.add_file_dialog = false;
            this.$message.success('新增文件夹成功，请刷新')
          }).catch(reason => {
            console.log(reason)
          })

        },
        get_cascade_data(){
          // 获取选项卡级联数据

          new_cascade().then( result => {
            const data = result.data;
            this.$store.commit('change_cascade', data.data);
            this.cascade_data = this.$store.state.cascade_dir
            // console.log(this.cascade_data)
          }).catch( error => {
            console.log(error)
          })
        },
        get_index_data(){
          this.table_loading = true;
          const user_name = window.sessionStorage.getItem('user_name')
          index_data(user_name).then( result => {
            if (result.data.code !== 200){
              this.$message.warning(result.data.msg);
              this.table_loading = false;
            }
            else{
              let response_data = result.data.data;
              for (let index in response_data){
                response_data[index]['no'] = parseInt(index) + 1
              }
              this.tableData = response_data
              this.table_loading = false;
              console.log(this.tableData)

            }

          }).catch( reason => {
            console.log(reason)
          })
          // this.get_cascade_data()
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
            this.$router.go(0)
          }).catch( reason => {
            console.log(reason)
          })

        },
        size_convert(size){
          let actual_size = parseInt(size) / 1024;
          return actual_size.toFixed(2) + 'KB'
        },
        upload_file(){
          this.upload_loading = true;
          this.upload_headers.Authorization = window.sessionStorage.getItem('token');
          if(this.upload_headers.Authorization){

            let formData = new FormData();
            // console.log(this.upload_file_list);

            this.upload_file_list.forEach( file =>{
              formData.append('file', file.raw)
              formData.append('size', file.size)
            });

            formData.append('path',this.change_path);
            upload_file(formData).then( result => {
              console.log(result)
              this.upload_loading = false;
              this.$message.success('上传文件成功，请刷新')
              this.up_load_file_dialog = false;
            }).catch(reason => {
              console.log(reason)
            })
          }
          else{
            console.log('上传失败')
          }

        },
        drop_down_command(command){
          // console.log('xxxxxxx');
          if(command === 'b'){
            this.download_file()
          }
        },
        download_file(){

          download_file(this.multipleSelection).then( result => {
            // console.log(result,'==')
            const content = result.data;
            // throw new Error(result)
            // console.log('=============================',content)
            // TODO 待修改名称等问题
            if ('download' in document.createElement('a')) { // 支持a标签download的浏览器
              const link = document.createElement('a'); // 创建a标签
              let config_data = JSON.parse(result.config.data);
              let file_name = new Date();
              file_name = dateFormat("YYYY-mm-dd HH:MM:SS", file_name) + '.zip';
              if(config_data.length === 1){
                 file_name = config_data[0]['file_name'] + '.zip'
              }
              link.download = file_name; // a标签添加属性
              link.style.display = 'none';
              link.href = URL.createObjectURL(new Blob([content]));
              document.body.appendChild(link);
              link.click() // 执行下载
              URL.revokeObjectURL(link.href) ;// 释放url
              document.body.removeChild(link) // 释放标签
            }
            console.log(result)
          }).catch( reason => {
            console.log(reason)
          })
        },

        change_table_data(arg){
          // TODO
          change_directory(arg).then(result => {
            if(result.data.code!==200){
              throw new Error(result.data.msg)
            }
            this.tableData = result.data.data
          }).catch(reason => {
            console.log(reason)
          })
        },
        start_search(){
        //  搜索
          search_content(this.search_value).then(result => {
            console.log(result)
            this.tableData = result.data.data

          }).catch(reason => {
            console.log(reason)
          })
        },
        filter_data(file_name){
          if(this.search_value && file_name.indexOf(this.search_value) > -1){
            // console.log(file_name, this.search_value)
            return file_name.replace(this.search_value, '<font color="#adff2f">' + this.search_value + '</font>')

          }else{
            return file_name
          }

        }
      },

      mounted() {

      // //  获取首页数据
        this.get_index_data();
      // //  获取级联目录 // 过滤搜索
        this.get_cascade_data()

      },
      watch: {

      },
    filters:{

    }
    }
</script>

<style scoped>

  .dir{
    color: #f9ca06;
    font-size: 22px;

  }
  .md {
    font-size: 25px;
    color: #da40dd;
  }
  .sql{
    color: #00ccff;
    font-size: 25px;
  }
  .mp3{
    color: green;
  }
  .txt{
    color: #f8b84e;
    font-size: 23px;
  }
  .text-style{
    text-decoration: none;
    color: #736279;
  }
  .text-style:hover{
    color: #00ccff;
  }

</style>
