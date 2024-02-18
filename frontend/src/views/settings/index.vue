<template>
  <div class="index">
    <div :class="{ disabled: isDisabled }" :style="{ 'pointer-events': isDisabled ? 'none' : 'auto' }">
      <el-form ref="ruleFormRef" :model="ruleForm" :rules="rules" label-width="120px" class="demo-ruleForm" :size="formSize"
        status-icon v-loading="loading" element-loading-text="正在更新..." :element-loading-spinner="svg"
        element-loading-svg-view-box="-10, -10, 50, 50">
        <el-form-item label="人设设定" prop="personal_setting">
          <el-input v-model="ruleForm.personal_setting" :rows="2" type="textarea" placeholder="请设置答复时的人设设定(感情)" />
          <el-tag class="ml-2" type="info" style="margin-top: 5px;">{{ personal_setting }}</el-tag>
        </el-form-item>
        <el-form-item label="严谨与想象" prop="imagination">
          <el-slider v-model="ruleForm.imagination" :min="0" :max="1" :step="0.1" :marks="marks" show-input style="width: 600px; margin-left: 10px;" />
        </el-form-item>
        <el-form-item label="Top P" prop="top_p">
          <el-slider v-model="ruleForm.top_p" :min="0" :max="1" :step="0.1" show-input style="width: 600px; margin-left: 10px;" />
        </el-form-item>
        <el-form-item style="margin-top: 50px;">
          <el-button type="primary" @click="updateConfig">保存</el-button>
          <el-button @click="reset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
    <el-result
      icon="info"
      title="允许开启本地数据缓存"
      sub-title="当开启本地数据缓存时, 才能定义配置并实时缓存数据"
      v-show="isDisabled"
    >
      <template #extra>
        <el-button type="primary" @click="openDB">开启</el-button>
      </template>
    </el-result>
  </div>
</template>

<script>
import { notify_warning, notify_success, notify_error } from '../../utils/message'
export default {
  name: 'Settings',
  data() {
    return {
      formSize: 'default',
      personal_setting: '默认: 我希望你是一个老师的角色, 回答我时可以温柔一点, 带点凶凶的, 说话干净利索',
      ruleForm: {
        personal_setting: '',
        imagination: 1,
        top_p: 1
      },
      rules: {
        personal_setting: [
          { required: false, message: '请设定人设', trigger: 'blur' },
          { min: 1, max: 200, message: 'Length should be 1 to 200', trigger: 'blur' },
        ],
        imagination: [
          { required: false, message: 'imagination', trigger: 'blur' }
        ],
        top_p: [
          { required: false, message: 'top_p', trigger: 'blur' }
        ]
      },
      marks: {
        0.2: {
          style: {
            color: '#bdc3c7',
          },
          label: '严谨细致'
        },
        0.8: {
          style: {
            color: '#3498db',
          },
          label: '想象发散'
        }
      },
      loading: false,
      svg: `
        <path class="path" d="
          M 30 15
          L 28 17
          M 25.61 25.61
          A 15 15, 0, 0, 1, 15 30
          A 15 15, 0, 1, 1, 27.99 7.5
          L 15 15
        " style="stroke-width: 4px; fill: rgba(0, 0, 0, 0)"/>
      `,
      dbExist: false,
      isDisabled: false
    }
  },
  methods: {
    updateConfig () {
      this.loading = true
      console.log(this.ruleForm)
      pywebview.api.api_db_update(this.ruleForm).then(response => {
        if (response.ok) {
          notify_success('配置已更新!')
        } else {
          notify_error('配置更新失败!')
        }
      }).finally(() => {
        this.loading = false
      })
    },
    reset () {
      notify_success('已重置配置!')
    },
    isDBExist () {
      pywebview.api.api_db_exist().then(response => {
        if (!response.db) {
          this.isDisabled = true
          notify_warning('请允许开启本地数据缓存.')
        } else {
          this.isDisabled = false
        }
      })
    },
    openDB () {
      pywebview.api.api_open_db().then(response => {
        if (response.ok) {
          notify_success('开启本地缓存成功, 您的数据将被实时保存.')
          this.getConfig()
          this.isDisabled = false
        } else {
          notify_error('开启本地缓存失败, 请联系开发人员.')
        }
      })
    },
    getConfig () {
      pywebview.api.api_db_query().then(response => {
        if (response) {
          this.ruleForm = {
            personal_setting: response.personal_setting,
            imagination: Number(response.imagination),
            top_p: Number(response.top_p)
          }
        }
      })
    }
  },
  created () {
    this.isDBExist()
  },
  mounted () {
    this.getConfig()
  }
}
</script>

<style scoped>
.disabled {
  cursor: not-allowed;
  opacity: 0.6;
  height: 100%;
  width: 100%;
}
</style>
