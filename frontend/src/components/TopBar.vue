<template>
  <header class="fixed top-0 left-0 right-0 bg-gray-900/95 backdrop-blur-md border-b border-gray-800 px-6 py-4 z-50 flex justify-between items-center shadow-lg">
    
    <div 
      class="flex items-center gap-3 cursor-pointer hover:opacity-80 transition-opacity" 
      @click="router.push('/profile')"
    >
      <div class="relative">
        <img 
          :src="user.avatar || `https://ui-avatars.com/api/?name=${user.name}&background=2563eb&color=fff`" 
          alt="Avatar" 
          class="w-10 h-10 rounded-full border-2 border-gray-700 object-cover"
        />
        <div class="absolute bottom-0 right-0 w-3 h-3 bg-green-500 border-2 border-gray-900 rounded-full"></div>
      </div>
      
      <div class="leading-tight">
        <p class="text-xs text-gray-400">Olá,</p>
        <p class="text-sm font-bold text-white max-w-[100px] truncate">{{ user.name || 'Kaio' }}</p>
      </div>
    </div>

    <div class="text-right">
      <p class="text-[10px] text-gray-400 uppercase tracking-wider font-bold">Disponível</p>
      <p class="text-lg font-bold text-blue-400">
        R$ {{ liquidBalance.toFixed(2) }}
      </p>
    </div>

    </header>
  
  <div class="h-20"></div> 
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router'; // Importante para a navegação funcionar
import api from '../api';

const router = useRouter(); // Inicializa o roteador
const user = ref({ name: '', avatar: '' });
const wallets = ref([]);

// Lógica de Saldo: Soma tudo, MENOS o que tiver "Reserva" no nome
const liquidBalance = computed(() => {
  return wallets.value.reduce((acc, wallet) => {
    if (wallet.name.toLowerCase().includes('reserva')) {
      return acc;
    }
    return acc + wallet.balance;
  }, 0);
});

const fetchData = async () => {
  try {
    const userRes = await api.get('/auth/me');
    user.value = { 
      name: userRes.data.full_name || userRes.data.username,
      avatar: userRes.data.profile_image 
    };

    const walletRes = await api.get('/wallets/');
    wallets.value = walletRes.data;
  } catch (err) {
    console.error("Erro ao carregar TopBar:", err);
  }
};

onMounted(fetchData);
</script>