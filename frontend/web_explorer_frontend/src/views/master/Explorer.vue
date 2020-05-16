<template>
<div >
<!--  操作栏-->
  <div style="box-shadow: 5px 5px 3px rgba(100, 100, 100, .3); padding: 10px; line-height: 3em">
    <el-row >
      <el-col :span="20">
        <el-button type="primary" size="small">新增文件夹</el-button>
        <el-button size="small" :disabled="edit_disabled" ref="edit_file_node">编辑文件夹</el-button>
        <el-button type="danger" size="mini">删除</el-button>
        <el-button  size="small">上传文件</el-button>
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
            v-model="value"
            :options="options"
            :props="{ expandTrigger: 'hover' }"
            @change="handleChange"
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
      :data="tableData"
      border
      style="width: 100%">
      <el-table-column
        prop="date"
        label="replace"
        width="180">
      </el-table-column>
      <el-table-column
        prop="name"
        label="序号"
        width="180">
      </el-table-column>
      <el-table-column
        prop="address"
        label="名称">
      </el-table-column>

      <el-table-column
        prop="address"
        label="修改日期">
      </el-table-column>

      <el-table-column
        prop="address"
        label="类型">
      </el-table-column>

      <el-table-column
        prop="address"
        label="大小">
      </el-table-column>
      <el-table-column
        prop="address"
        label="创建日期">
      </el-table-column>
      <el-table-column
        prop="address"
        label="作者">
      </el-table-column>
      <el-table-column
        prop="address"
        label="描述">
      </el-table-column>
    </el-table>



  </div>

</div>

</template>

<script>
    export default {
      name: "explorer",
      data(){
        return {
          edit_disabled: true,

        }
      },
      methods:{

      }

    }
</script>

<style scoped>


</style>
