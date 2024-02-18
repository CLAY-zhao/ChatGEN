<template>
  <div class="index">
    <div class="header">
      <el-page-header :icon="null">
        <template #title>
          Chat
        </template>
        <template #content>
          <div class="flex items-center">
            <el-avatar
              :size="32" class="mr-3"
              src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
            />
            <span class="text-sm mr-2" style="color: var(--el-text-color-regular)">
              Just Chat
            </span>
            <el-tag style="margin-left: 5px;">你是个乐于助人的助手。你可以回答我的问题来帮助我。你也可以问我一些问题.</el-tag>
          </div>
        </template>
        <template #extra>
          <div class="flex items-center">
            <el-switch v-model="readDisable" class="ml-2" inline-prompt
              style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949; margin-right: 15px;"
              active-text="开启自动阅读" inactive-text="关闭自动阅读" size="large"
            />
            <el-button type="primary" class="ml-2" :icon="Plus" @click="addSession">新建会话</el-button>
          </div>
        </template>
      </el-page-header>
    </div>
    <el-divider>
      <el-icon><Comment /></el-icon>
    </el-divider>
    <el-container>
      <el-container>
        <el-aside width="300px">
          <el-card class="left-box">
            <template #header>
              <div class="card-header">
                <el-button class="left-box-button" type="info" plain>
                  New chat
                  <el-icon style="margin-left: 10px;"><Edit /></el-icon>
                </el-button>
              </div>
            </template>
            <div class="text item left-box-btn" v-if="openCache">
              <span class="chat-span">
                <el-text class="mx-1 chat-item">
                  监听Alt+Enter事件
                </el-text>
                <el-icon class="more">
                  <el-dropdown trigger="click">
                    <MoreFilled style="outline: none;" />
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item style="color: #2c3e50;">
                          <el-icon><Edit /></el-icon>
                          Rename
                        </el-dropdown-item>
                        <el-dropdown-item style="color: red;" @click="deleteChat">
                          <el-icon><Delete /></el-icon>
                          Delete chat
                        </el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </el-icon>
              </span>
            </div>
            <el-result class="cache-tip" icon="warning" title="无法缓存会话" sub-title="请先开启本地数据缓存" v-else>
              <template #extra>
                <el-button type="primary" @click="goSettings">前往设置</el-button>
              </template>
            </el-result>
            <template #footer>Footer content</template>
          </el-card>
        </el-aside>
        <el-container>
          <el-main>
            <el-alert title="正在进行语音识别, 请进行说话......" type="warning" effect="dark" center :closable="false" v-if="speaking" />
            <div ref="scrollContainer" class="question-main" v-if="questionList.length > 0">
              <div class="q-item" v-for="(item, index) in questionList" :key="index">
                <div class="avatar">
                  <el-button v-if="item.loading" loading circle size="large" type="warning" />
                  <el-button v-else-if="item.robot" :icon="Setting" circle size="large" type="info" />
                  <el-dropdown size="small" v-else>
                    <el-button :icon="UserFilled" circle size="large" type="primary" />
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item @click="reEdit(item.content)">重新编辑</el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </div>
                <el-card class="box-card question-card">
                  <el-tooltip class="box-item" effect="dark" content="点击阅读" placement="right-start">
                    <el-icon class="mic" placeholder="朗读" @click="onRead(item.content)" v-if="item.robot"><Mic /></el-icon>
                  </el-tooltip>
                  <Markdown :source="item.content" v-if="item.robot" />
                  <el-text class="w-150px mb-2" truncated v-else>
                    {{ item.content }}
                  </el-text>
                </el-card>
              </div>
              <el-backtop target=".question-main" :right="100" :bottom="200" />
            </div>
          </el-main>
          <el-footer style="height: 140px;">
            <div class="question">
              <el-divider>
                <el-icon><EditPen /></el-icon>
              </el-divider>
              <el-dropdown placement="top" style="padding: 5px;">
                <el-button plain size="large">
                  <el-icon><Operation /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click="onSpeech">
                      <el-icon><Mic /></el-icon>
                      语音识别
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
              <el-input
                ref="question"
                v-model="question"
                :autosize="{ minRows: 2, maxRows: 4 }"
                type="textarea"
                placeholder="说点什么..."
                style="width: calc(100% - 150px); margin-left: 10px;"
              />
              <el-tooltip
                class="box-item" effect="dark" content="发送 Alt+Enter" placement="top-start" v-if="questionOK"
              >
                <el-button type="primary" size="large" :icon="Promotion"
                  style="margin-left: 10px; margin-bottom: 5px;" @click="sendQuestion"
                />
              </el-tooltip>
              <el-tooltip
                class="box-item" effect="dark" content="正在思考中" placement="top-start" v-else
              >
                <el-button type="primary" size="large" :icon="Promotion"
                  style="margin-left: 10px; margin-bottom: 5px;" @click="sendQuestion" disabled
                />
              </el-tooltip>
            </div>
          </el-footer>
        </el-container>
      </el-container>
    </el-container>
    <audio :muted="false" controls="controls" hidden src="/static/answer-tip.mp3" ref="orderTip"></audio>
  </div>
</template>

<script>
// https://github.com/JanGuillermo/vue3-markdown-it
import Markdown from 'vue3-markdown-it'
import {
  Comment, Operation, EditPen, Promotion, Setting, UserFilled, Loading, Plus, Edit, MoreFilled,
  Delete, Mic
} from '@element-plus/icons-vue'
import { ElMessageBox } from 'element-plus'
import { warning_msg, success_msg } from '../../utils/message'
export default {
  name: 'Dashboard',
  components: {
    Comment,
    Operation,
    EditPen,
    Markdown,
    Edit,
    MoreFilled,
    Delete,
    Mic
  },
  data () {
    return {
      question: '',
      Promotion,
      Setting,
      UserFilled,
      Loading,
      Plus,
      response: '',
      questionList: [
        {robot: true, content: '😎很高兴见到你😆, 你可以向我提问一些问题.'}
      ],
      questionOK: true,
      readDisable: false,
      openCache: false,
      speaking: false
    }
  },
  methods: {
    sendQuestion () {
      const question = this.question
      if (!question) {
        return warning_msg('发送内容不能为空哦')
      }
      this.questionOK = false // 正在思考中
      this.pushPeopleQuestion()
      const self = this
      setTimeout(() => {
        self.questionList.push({robot: true, content: '😢😢😢 正在思考, 请等等!!!', loading: true})
        this.$nextTick(() => {
          this.scrollToBottom()
        })
      }, 500);
      pywebview.api.query_question(question).then(response => {
        this.answerTipAudioPlay()
        this.questionList[this.questionList.length - 1] = {
          robot: true, content: response, loading: false
        }
        if (this.readDisable) {
          this.onRead(response)
        }
      }).catch(() => {
        this.questionList[this.questionList.length - 1] = {
          robot: true, content: '😭😭😭 没想来, 能不能点击重试再给我一次机会!!!', loading: false
        }
      }).finally(() => {
        this.questionList[this.questionList.length - 1].loading = false
        this.questionOK = true // 思考完毕
        this.$nextTick(() => {
          this.scrollToBottom()
        })
      })
    },
    pushPeopleQuestion () {
      this.questionList.push({robot: false, content: this.question})
      this.question = '' // clear the question
      this.$nextTick(() => {
        this.scrollToBottom()
      })
    },
    listenerAltEnter (event) {
      // 监听Alt + Enter触发发送事件
      if (event.altKey && event.key === "Enter") {
        if (this.questionOK) {
          this.sendQuestion()
        }
      }
    },
    reEdit (question) {
      this.question = question
      this.$refs.question.focus()
    },
    addSession () {
      ElMessageBox.alert('如果你没有开启支持本地缓存, 所有会话都不会进行保存', '新建会话', {
        confirmButtonText: 'OK'
      })
    },
    deleteChat () {
      ElMessageBox.confirm(
        'This will delete xxxxxx',
        'Delete chat?',
        {
          confirmButtonText: 'Delete',
          cancelButtonText: 'Cancel',
          type: 'warning'
        }
      ).then(() => {
        console.log('delete')
      }).catch(() => {
        logger.log('cancel')
      })
    },
    onRead (content) {
      const synthesis = window.speechSynthesis
      if (synthesis.speaking) {
        return
      }
      const utterance = new SpeechSynthesisUtterance(content)
      utterance.rate = 0.8
      synthesis.speak(utterance)
    },
    scrollToBottom () {
      const scrollContainer = this.$refs.scrollContainer
      scrollContainer.scrollTop = scrollContainer.scrollHeight
    },
    goSettings () {
      this.$router.push({path: 'settings'})
    },
    onSpeech () {
      const recognition = new window.webkitSpeechRecognition()
      recognition.lang = 'zh-CN'
      this.speaking = true
      recognition.start()
      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript
        this.question = transcript
        this.sendQuestion()
      }
      recognition.onend = () => {
        success_msg('语音识别结束')
        this.speaking = false
      }
      recognition.onerror = () => {
        warning_msg('语音识别错误')
        this.speaking = false
      }
    },
    answerTipAudioPlay () {
      this.$refs.orderTip.currentTime = 0
      this.$refs.orderTip.volume = 0.5
      this.$refs.orderTip.play()
    }
  },
  mounted () {
    window.addEventListener('keydown', this.listenerAltEnter)
  },
  beforeUnmount () {
    window.removeEventListener('keydown', this.listenerAltEnter)
    const synthesis = window.speechSynthesis
    if (synthesis.speaking) {
      synthesis.cancel()
    }
  }
}
</script>

<style scoped>
.index {
  position: relative;
  height: calc(100vh - 150px);
}
.question-main {
  height: calc(100vh - 400px);
  overflow-y: auto;
}
.question {
  /* position: absolute; */
  width: 100%;
  bottom: 5px;
  text-align: center;
}
.avatar {
  display: inline-block;
}
.question-card {
  position: relative;
  display: inline-flex;
  margin-left: 10px;
  width: calc(100% - 100px);
}

.mic {
  position: absolute;
  right: 5px;
  top: 5px;
  color: rgba(189, 195, 199, .8);
  font-size: 20px;
  cursor: pointer;
}

.q-item {
  margin: 10px 0;
}
.q-item:first {
  margin: 0;
}

/deep/ .el-card__body {
  width: 100%;
}

/deep/ .vuepress-markdown-body {
  padding: 5px 0;
}

.left-box {
  height: calc(100vh - 200px);
}

.left-box-btn {
  height: calc(100vh - 400px);
  overflow-y: auto;
}

.cache-tip {
  height: calc(100vh - 400px);
  width: 255px;
}

.left-box-button {
  width: 100%;
}

.chat-span {
  width: calc(100% - 40px);
  display: block;
  padding: 10px 0;
  transition: .3s;
  border-radius: 5px;
  background: rgba(236, 240, 241, .3);
  margin-bottom: 5px;
  position: relative;
}

.chat-span:hover {
  background: rgba(52, 73, 94, .1);
}

.chat-item {
  padding: 10px;
}

.more {
  position: absolute;
  right: 10px;
}
</style>
