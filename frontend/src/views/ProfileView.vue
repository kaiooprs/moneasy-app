<template>
  <div class="min-h-screen bg-gray-900 text-white pt-5 pb-24 px-4 relative">
    
    <div class="mb-6">
      <h1 class="text-2xl font-bold">Meu Perfil</h1>
      <p class="text-gray-400 text-xs">Configure sua conta</p>
    </div>

    <div v-if="loading" class="flex justify-center py-10 opacity-50">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
    </div>

    <div v-else class="bg-gray-800 rounded-3xl p-6 border border-gray-700 shadow-xl flex flex-col items-center text-center relative mb-6">
      
      <button @click="openEditModal" class="absolute top-4 right-4 text-gray-400 hover:text-blue-400 p-2 bg-gray-900 rounded-xl transition-colors shadow-sm">
        <Pencil :size="18" />
      </button>

      <div class="relative mb-4">
        <img :src="avatarUrl" alt="Avatar" class="w-24 h-24 rounded-full border-4 border-gray-700 object-cover shadow-lg" />
      </div>

      <h2 class="text-xl font-bold text-white">{{ user.full_name || user.username }}</h2>
      <p class="text-gray-400 text-sm mb-6">{{ user.email }}</p>

      <div class="w-full space-y-3">
        
        <button @click="$router.push('/categories')" class="w-full bg-gray-900 hover:bg-gray-700 text-left p-4 rounded-xl flex items-center justify-between transition-all border border-gray-700/50 group">
          <div class="flex items-center gap-3">
            <div class="p-2 bg-blue-500/10 rounded-lg text-blue-400 group-hover:bg-blue-500/20 transition-colors">
              <Tags :size="20" />
            </div>
            <span class="font-bold text-sm">Gerenciar Categorias</span>
          </div>
          <ChevronRight class="text-gray-500" :size="18" />
        </button>

        <button @click="logout" class="w-full bg-red-500/10 hover:bg-red-500/20 text-red-400 text-left p-4 rounded-xl flex items-center gap-3 transition-colors border border-red-500/20">
          <div class="p-2 bg-red-500/10 rounded-lg">
            <LogOut :size="20" />
          </div>
          <span class="font-bold text-sm">Sair do Aplicativo</span>
        </button>
      </div>
    </div>

    <div v-if="isModalOpen" class="fixed inset-0 z-[100] flex items-end sm:items-center justify-center px-4 py-6">
      <div class="absolute inset-0 bg-black/80 backdrop-blur-sm transition-opacity" @click="closeModal"></div>

      <div class="bg-gray-800 w-full max-w-md rounded-3xl p-6 relative shadow-2xl border border-gray-700 transform transition-all animate-slide-up mb-6 sm:mb-0">
        
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-bold text-white">Editar Perfil</h2>
          <button @click="closeModal" class="bg-gray-700 p-2 rounded-full text-gray-400 hover:text-white">
            <X :size="20" />
          </button>
        </div>

        <form @submit.prevent="submitProfile" class="space-y-4">
          
          <div>
            <label class="block text-xs text-gray-400 uppercase font-bold mb-1">Nome de Exibição</label>
            <input v-model="form.full_name" type="text" placeholder="Digite seu nome completo" 
              class="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-blue-500 outline-none" />
          </div>

          <div>
            <label class="block text-xs text-gray-400 uppercase font-bold mb-1">Link da Foto (Opcional)</label>
            <input v-model="form.profile_image" type="url" placeholder="https://exemplo.com/foto.jpg" 
              class="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-blue-500 outline-none text-sm" />
            <p class="text-[10px] text-gray-500 mt-1">Cole o link de uma imagem da internet.</p>
          </div>

          <button type="submit" :disabled="saving"
            class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-4 rounded-xl shadow-lg mt-2 flex justify-center items-center">
            <span v-if="saving" class="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></span>
            <span v-else>Salvar Alterações</span>
          </button>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { LogOut, Tags, ChevronRight, Pencil, X } from 'lucide-vue-next';
import { useToast } from "vue-toastification";
import Swal from 'sweetalert2';
import api from '../api';
import { refreshTrigger } from '../store';

const router = useRouter();
const toast = useToast();
const loading = ref(true);
const saving = ref(false);

const user = ref({
  username: '',
  email: '',
  full_name: '',
  profile_image: ''
});

const isModalOpen = ref(false);
const form = ref({ full_name: '', profile_image: '' });

const avatarUrl = computed(() => {
  if (user.value.profile_image) {
    return user.value.profile_image;
  }
  const nameToUse = user.value.full_name || user.value.username || 'User';
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(nameToUse)}&background=3b82f6&color=fff&size=150&font-size=0.4`;
});

const fetchUser = async () => {
  loading.value = true;
  try {
    const { data } = await api.get('/auth/me');
    user.value = data;
  } catch (err) {
    toast.error("Erro ao carregar perfil.");
  } finally {
    loading.value = false;
  }
};

const openEditModal = () => {
  form.value.full_name = user.value.full_name || '';
  form.value.profile_image = user.value.profile_image || '';
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
};

const submitProfile = async () => {
  saving.value = true;
  try {
    const payload = {
      full_name: form.value.full_name || null,
      profile_image: form.value.profile_image || null
    };

    const { data } = await api.put('/auth/me', payload);
    
    user.value.full_name = data.full_name;
    user.value.profile_image = data.profile_image;
    
    toast.success("Perfil atualizado!");
    refreshTrigger.value++; 
    closeModal();
  } catch (err) {
    toast.error("Erro ao atualizar: " + (err.response?.data?.detail || err.message));
  } finally {
    saving.value = false;
  }
};

const logout = async () => {
  const result = await Swal.fire({
    title: 'Sair do Moneasy?',
    text: "Você precisará fazer login novamente.",
    icon: 'question',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#374151',
    confirmButtonText: 'Sim, sair',
    background: '#1f2937',
    color: '#fff'
  });

  if (result.isConfirmed) {
    localStorage.removeItem('token');
    router.push('/login');
    toast.info("Você saiu do sistema.");
  }
};

onMounted(fetchUser);
</script>

<style scoped>
.animate-slide-up {
  animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes slideUp {
  from { transform: translateY(100%); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
</style>