import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'

// 1. Importar o Toast e o CSS dele
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

const app = createApp(App)

app.use(router)

// 2. Configurações opcionais (deixa ele bonitão)
const options = {
    position: "top-right",
    timeout: 3000,
    closeOnClick: true,
    pauseOnFocusLoss: true,
    pauseOnHover: true,
    draggable: true,
    draggablePercent: 0.6,
    showCloseButtonOnHover: false,
    hideProgressBar: false,
    closeButton: "button",
    icon: true,
    rtl: false
};

// 3. Ativar o Toast
app.use(Toast, options);

app.mount('#app')