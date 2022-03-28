import { createApp } from 'vue'
import App from './App.vue'
import './index.css'
import './assets/css/bootstrap.css'
import { createStore } from 'vuex'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'



// 创建一个新的 store 实例
// Vuex
const store = createStore({
  state () {
    return {
      username: '',
      userid: -1
    }
  },
  mutations: {
    changeUserName (state, username) {
      state.username = username
    },
    changeUserId(state, user_id){
      state.userid = user_id
    }
  }
})

// axios
import axios from 'axios'
const app = createApp(App)
app.config.globalProperties.$http = axios

// router
import router from './router'
app.use(router)
app.use(ElementPlus);
app.use(store)


app.mount('#app')

