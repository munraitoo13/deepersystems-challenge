import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import PrimeVue from 'primevue/config'
import Aura from '@primeuix/themes/aura'

// primevue components
import { DataTable, Button, Column, Dialog, InputText, Toast, ToastService } from 'primevue'

const app = createApp(App)

app.use(router)
app.use(PrimeVue, {
  theme: {
    preset: Aura,
  },
})
app.use(ToastService)

// global components
app.component('Button', Button)
app.component('DataTable', DataTable)
app.component('Column', Column)
app.component('Dialog', Dialog)
app.component('InputText', InputText)
app.component('Toast', Toast)

// mount app
app.mount('#app')
