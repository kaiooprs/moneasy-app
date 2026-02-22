<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900 p-4">
    <div class="max-w-md w-full bg-gray-800 rounded-xl p-8 shadow-2xl border border-gray-700">
      <h2 class="text-3xl font-bold text-white mb-2 text-center">Moneasy</h2>
      <p class="text-gray-400 text-center mb-8">Gestão financeira simples</p>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">Usuário</label>
          <input 
            v-model="username" 
            type="text" 
            class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white focus:ring-2 focus:ring-blue-500 outline-none transition"
            placeholder="Digite seu usuário"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-300 mb-2">Senha</label>
          <input 
            v-model="password" 
            type="password" 
            class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white focus:ring-2 focus:ring-blue-500 outline-none transition"
            placeholder="••••••••"
            required
          />
        </div>

        <button 
          type="submit" 
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg transition transform active:scale-95 shadow-lg"
        >
          Entrar
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router'; 
import { useToast} from "vue-toastification";
import api from '../api';

const username = ref('');
const password = ref('');
const router = useRouter(); 
const toast = useToast();

const handleLogin = async () => {
  try {
    const formData = new FormData();
    formData.append('username', username.value);
    formData.append('password', password.value);

    const { data } = await api.post('/auth/login', formData);
    
    localStorage.setItem('token', data.access_token);
    
    router.push('/dashboard'); 
  } catch (err) {
    toast.error('Erro: ' + (err.response?.data?.detail || 'Falha no login'));
  }
};
</script>