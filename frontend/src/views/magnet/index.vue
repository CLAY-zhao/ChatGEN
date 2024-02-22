<template>
  <div class="index">
    <div class="search-bar">
      <div>
        <el-input
          v-model="source"
          placeholder="资源名称"
          class="input-with-select"
          v-on:keyup.enter="onSearch"
        >
          <template #append>
            <el-button :icon="Search" @click="onSearch" />
          </template>
        </el-input>
      </div>
    </div>
    <el-divider>
      <el-icon><Files /></el-icon>
    </el-divider>
    <div class="list" v-loading="loading"  element-loading-text="正在搜索中...">
      <div class="empty" v-if="!searchList.length">
        <el-empty :image-size="200" />
      </div>
      <div v-else>
        <el-card class="box-card" v-for="(item, index) in searchList" :key="index">
          <template #header>
            <div class="card-header">
              <div class="title" v-html="item.title" @click="onQueryInfo(item)"></div>
            </div>
          </template>
          <em style="display: inline-block; color: #666;">
            <el-icon><Download /></el-icon>
            下载量：
          </em>
          <div class="text item info" v-html="item.info"></div>
        </el-card>
        <div class="page">
          <el-button type="primary" @click="goHomePage">首页</el-button>
          <el-button type="primary" @click="prevPage" v-if="page !== 1">上一页</el-button>
          <el-button type="primary" @click="nextPage" v-if="page >= 1 && !end">下一页</el-button>
        </div>
      </div>
    </div>
    <el-divider>
      <el-icon><Files /></el-icon>
    </el-divider>
    <el-drawer v-model="drawer" :direction="direction" size="60%" style="text-align: left;">
      <template #title>
        <div v-html="info.title" class="info-title" />
      </template>
      <div>
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span><el-icon style="margin-right: 5px;"><Download /></el-icon>磁链地址复制</span>
            </div>
          </template>
          <el-link type="primary" :href="info.downUrl">{{ info.downUrl }}</el-link>
          <el-button type="primary" size="small" style="margin-left: 20px;" @click="copy(info.downUrl)">复制链接</el-button>
        </el-card>
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span><el-icon style="margin-right: 5px;"><Menu /></el-icon>磁链详情</span>
            </div>
          </template>
          <em style="display: inline-block; color: #666; font-size: 14px;">
            下载量：
          </em>
          <el-text class="mx-1"><div class="info" v-html="info.desc"></div></el-text>
        </el-card>
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span><el-icon style="margin-right: 5px;"><Histogram /></el-icon>文件meta</span>
            </div>
          </template>
          <el-table :data="info.meta" style="width: 100%">
            <el-table-column prop="title" label="文件名" width="800" />
            <el-table-column label="大小" width="120">
              <template #default="scope">
                <el-tag>
                  {{ scope.row.size }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </div>
    </el-drawer>
  </div>
</template>

<script>
import {
  Search, Files, Download, Menu, Histogram
} from '@element-plus/icons-vue'
import { success_msg, error_msg } from '../../utils/message'
export default {
  name: 'Magnet',
  components: {
    Files,
    Download,
    Menu,
    Histogram
  },
  data () {
    return {
      source: '迪迦奥特曼',
      Search,
      searchList: [],
      loading: false,
      drawer: false,
      direction: 'ltr',
      info: {
        title: '',
        downUrl: '',
        desc: '',
        meta: []
      },
      page: 1,
      end: false,
      checkLen: 0
    }
  },
  methods: {
    onSearch () {
      this.loading = true
      this.searchList = []
      pywebview.api.api_magnet_search(this.source, this.page).then(response => {
        if (response.ok) {
          this.searchList = response.list
          if (this.checkLen === 0) {
            this.checkLen = response.list.length
          } else if (this.checkLen !== response.list.length) {
            this.end = true
          }
        }
      }).catch(() => {
        error_msg('搜索失败! 请联系开发者.')
      }).finally(() => {
        this.loading = false
      })
    },
    onQueryInfo (item) {
      this.loading = true
      pywebview.api.api_magnet_info(item.link).then(response => {
        this.drawer = true
        this.info.title = item.title
        this.info.desc = item.info
        this.info.downUrl = response.info.down_url
        this.info.meta = response.info.meta
      }).finally(() => {
        this.loading = false
      })
    },
    prevPage () {
      this.page -= 1
      this.end = false
      this.onSearch()
    },
    nextPage () {
      this.page += 1
      this.onSearch()
    },
    goHomePage () {
      this.page = 1
      this.end = false
      this.onSearch()
    },
    copy (text) {
      if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
          success_msg('复制成功!')
        })
      } else {
        this.$copyText(text).then(() => {
          success_msg('复制成功!')
        }).catch(() => {
          const textField = document.createElement('textarea')
          textField.innerText = text
          document.body.appendChild(textField)
          textField.select()
          document.execCommand('copy') // 兼容性不稳定
          textField.remove()
        })
      }
    }
  }
}
</script>

<style scoped>
.search-bar {
  height: 100px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.input-with-select {
  height: 50px;
  width: calc(100vh - 400px);
}
.list {
  overflow-y: auto;
  height: calc(100vh - 350px);
}
.box-card {
  max-width: 1000px;
  margin: 10px auto;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
/deep/ em {
  color: #cc0000;
}
.title {
  color: rgba(41, 128, 185, 1.0);
}
/deep/ .info {
  display: inline-block;
}
/deep/ .info em {
  margin-left: 10px;
  color: #666;
}
.info-title {
  color: #34495e;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-top: 20px;
}
.page {
  margin: 20px 0;
  text-align: center;
}
</style>
