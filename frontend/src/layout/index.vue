<template>
  <el-menu
    :default-active="activeIndex"
    class="el-menu-demo"
    mode="horizontal"
    :router="true"
    style="padding: 0 10px;"
  >
    <el-sub-menu>
      <template #title>便利工具</template>
      <el-menu-item index="dashboard">基本问答</el-menu-item>
      <el-menu-item index="magnet">磁力搜索</el-menu-item>
    </el-sub-menu>
    <el-menu-item index="settings">全局配置</el-menu-item>
    <el-menu-item index="about">关于我</el-menu-item>
  </el-menu>
  <div class="container">
    <el-card class="box-card">
      <router-view />
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Layout',
  data () {
    return {
      activeIndex: 'dashboard'
    }
  }
}
</script>

<style scoped>
.layout-container-demo .el-header {
  position: relative;
  background-color: var(--el-color-primary-light-7);
  color: var(--el-text-color-primary);
}
.layout-container-demo .el-aside {
  color: var(--el-text-color-primary);
  background: var(--el-color-primary-light-8);
}
.layout-container-demo .el-menu {
  border-right: none;
}
.layout-container-demo .el-main {
  padding: 0;
}
.layout-container-demo .toolbar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  right: 20px;
}
.container {
  margin: 10px;
}
.box-card {
  height: calc(100vh - 100px);
}
</style>
