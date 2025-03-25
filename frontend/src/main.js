import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import PrimeVue from 'primevue/config'
import Aura from '@primeuix/themes/material/'
import 'primeicons/primeicons.css'

// primevue components
import {
  DataTable,
  Button,
  Column,
  Dialog,
  InputText,
  Toast,
  ToastService,
  Select,
  Fluid,
  MultiSelect,
} from 'primevue'

const app = createApp(App)

app.use(router)
app.use(PrimeVue, {
  theme: {
    inputStyle: 'filled',
    preset: Aura,
    options: {
      darkModeSelector: '.dark-mode',
    },
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
app.component('Select', Select)
app.component('Fluid', Fluid)
app.component('MultiSelect', MultiSelect)

// mount app
app.mount('#app')
