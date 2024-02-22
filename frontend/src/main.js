import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

// other
import VueClipboard from 'vue-clipboard2'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'normalize.css'
import 'highlight.js/styles/github.css'

const app = createApp(App)

app.use(store)
app.use(router)
app.use(ElementPlus)
app.use(VueClipboard)
app.mount('#app')
