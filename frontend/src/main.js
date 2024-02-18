import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

// other
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'normalize.css'
import 'highlight.js/styles/github.css'

const app = createApp(App)

app.use(store)
app.use(router)
app.use(ElementPlus)
app.mount('#app')