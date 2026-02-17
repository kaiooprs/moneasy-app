<template>
  <div class="min-h-screen bg-gray-900 text-white pb-24 pt-0 px-4">
    
    <div class="flex flex-col items-center py-8">
      <div class="relative">
        <img 
          :src="user.avatar || `https://ui-avatars.com/api/?name=${user.name}&background=2563eb&color=fff&size=128`" 
          alt="Avatar" 
          class="w-24 h-24 rounded-full border-4 border-gray-800 shadow-xl object-cover"
        />
        <button class="absolute bottom-0 right-0 bg-gray-700 p-2 rounded-full border-4 border-gray-900 text-white hover:bg-blue-600 transition-colors">
          <Camera :size="16" />
        </button>
      </div>
      <h1 class="mt-4 text-xl font-bold">{{ user.name }}</h1>
      <p class="text-gray-400 text-sm">@{{ user.username }}</p>
    </div>

    <div class="space-y-4 mt-4">
      
      <div class="bg-gray-800 rounded-2xl overflow-hidden border border-gray-700/50">
        
        <button @click="openCategories" class="w-full flex items-center justify-between p-4 hover:bg-gray-700/50 transition-colors border-b border-gray-700/50">
          <div class="flex items-center gap-3">
            <div class="p-2 bg-blue-500/10 text-blue-400 rounded-lg">
              <Tags :size="20" />
            </div>
            <span class="font-medium">Gerenciar Categorias</span>
          </div>
          <ChevronRight :size="18" class="text-gray-500" />
        </button>

        <button class="w-full flex items-center justify-between p-4 hover:bg-gray-700/50 transition-colors">
          <div class="flex items-center gap-3">
            <div class="p-2 bg-purple-500/10 text-purple-400 rounded-lg">
              <Lock :size="20" />
            </div>
            <span class="font-medium">Alterar Senha</span>
          </div>
          <ChevronRight :size="18" class="text-gray-500" />
        </button>

      </div>

      <div class="bg-gray-800 rounded-2xl overflow-hidden border border-gray-700/50">
        <button class="w-full flex items-center justify-between p-4 hover:bg-gray-700/50 transition-colors">
          <div class="flex items-center gap-3">
            <div class="p-2 bg-yellow-500/10 text-yellow-400 rounded-lg">
              <Bell :size="20" />
            </div>
            <span class="font-medium">Notificações</span>
          </div>
          
          <div class="w-10 h-6 bg-gray-700 rounded-full p-1 flex items-start">
             <div class="w-4 h-4 bg-gray-500 rounded-full"></div>
          </div>
        </button>
      </div>

      <button @click="handleLogout" class="w-full bg-red-500/10 hover:bg-red-500/20 text-red-500 p-4 rounded-2xl flex items-center justify-center gap-2 font-bold transition-colors mt-8 border border-red-500/20">
        <LogOut :size="20" />
        Sair da Conta
      </button>

      <p class="text-center text-xs text-gray-600 mt-4">Moneasy v1.0.0 • Feito por Kaio Pereira</p>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';
import { Camera, Tags, Lock, ChevronRight, LogOut, Bell } from 'lucide-vue-next';

const router = useRouter();
const user = ref({ name: 'Carregando...', username: '...', avatar: '' });

const fetchUser = async () => {
  try {
    const { data } = await api.get('/auth/me');
    user.value = {
      name: data.full_name || 'Usuário',
      username: data.username || 'user',
      avatar: data.profile_image
    };
  } catch (err) {
    console.error("Erro ao carregar perfil", err);
  }
};

const openCategories = () => {
  alert("Próxima parada: Tela de Gerenciar Categorias! 🚧");
  // router.push('/categories'); // Futuramente
};

const handleLogout = () => {
  if(confirm("Tem certeza que deseja sair?")) {
    localStorage.removeItem('token');
    router.push('/login');
  }
};

onMounted(fetchUser);
</script>