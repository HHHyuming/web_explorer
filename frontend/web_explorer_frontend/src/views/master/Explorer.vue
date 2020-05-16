<template>
<div>
    <el-row>
      <el-col :span="20">
        <el-button size="small">默认按钮</el-button>
        <el-button type="primary" size="small">主要按钮</el-button>
        <el-button type="success" size="small">成功按钮</el-button>
        <el-button type="info" size="small">信息按钮</el-button>
        <el-button type="warning" size="small">警告按钮</el-button>
        <el-button type="danger" size="small">危险按钮</el-button>
      </el-col>
    </el-row>

</div>
</template>

<script>
    export default {
        name: "explorer"
    }
</script>

<style scoped>

</style>
