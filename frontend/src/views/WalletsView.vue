<template>
  <div class="min-h-screen bg-gray-900 text-white pt-5 pb-24 px-4 relative">
    <div class="mb-6 flex justify-between items-end">
      <div>
        <h1 class="text-2xl font-bold">Carteiras</h1>
        <p class="text-gray-400 text-xs">Gerencie seus saldos e reservas</p>
      </div>
      <button @click="openCreateModal" 
        class="bg-blue-600 hover:bg-blue-500 text-white p-2 px-4 rounded-xl shadow-lg shadow-blue-900/20 flex items-center gap-2 text-sm font-bold transition-transform active:scale-95">
        <Plus :size="18" /> Nova
      </button>
    </div>

    <div v-if="loading" class="flex justify-center py-10 opacity-50">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
    </div>

    <div class="grid gap-4">
      <div v-for="w in wallets" :key="w._id" 
        class="bg-gray-800 p-5 rounded-2xl border border-gray-700 shadow-sm relative overflow-hidden"
        :style="{ borderLeftWidth: '4px', borderLeftColor: w.color || '#3b82f6' }">
        
        <div class="absolute -right-4 -top-4 opacity-[0.03] text-white">
          <WalletIcon :size="100" />
        </div>

        <div class="relative z-10 flex justify-between items-start">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <h3 class="font-bold text-lg text-white">{{ w.name }}</h3>
              <span v-if="w.type === 'poupanca'" class="bg-purple-500/20 text-purple-400 text-[10px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider">
                Reserva
              </span>
            </div>
            <p v-if="w.description" class="text-xs text-gray-400 mb-3">{{ w.description }}</p>
            
            <p class="text-[10px] text-gray-500 font-bold uppercase tracking-wide">Saldo Atual</p>
            <p class="text-2xl font-bold" :class="w.balance >= 0 ? 'text-blue-400' : 'text-red-400'">
              R$ {{ w.balance.toFixed(2) }}
            </p>
            
            <p v-if="w.type === 'poupanca' && w.goal > 0" class="text-[9px] text-purple-400 font-bold mt-1 uppercase">
              Meta: R$ {{ w.goal.toFixed(2) }}
            </p>
          </div>
          
          <div class="flex flex-col gap-2">
            <button @click="openEditModal(w)" class="text-gray-400 hover:text-blue-400 transition-colors p-2 bg-gray-900 rounded-lg">
              <Pencil :size="16" />
            </button>
            <button @click="deleteWallet(w._id, w.name)" class="text-gray-400 hover:text-red-400 transition-colors p-2 bg-gray-900 rounded-lg">
              <Trash2 :size="16" />
            </button>
          </div>
        </div>
      </div>

      <div v-if="!loading && wallets.length === 0" class="text-center py-12 text-gray-500 bg-gray-800/50 rounded-2xl border border-dashed border-gray-700">
        <p>Nenhuma carteira cadastrada.</p>
      </div>
    </div>

    <div v-if="isModalOpen" class="fixed inset-0 z-[100] flex items-end sm:items-center justify-center px-4 py-6">
      <div class="absolute inset-0 bg-black/80 backdrop-blur-sm transition-opacity" @click="closeModal"></div>

      <div class="bg-gray-800 w-full max-w-md rounded-3xl p-6 relative shadow-2xl border border-gray-700 transform transition-all animate-slide-up mb-6 sm:mb-0">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-bold text-white">{{ isEditing ? 'Editar Carteira' : 'Nova Carteira' }}</h2>
          <button @click="closeModal" class="bg-gray-700 p-2 rounded-full text-gray-400 hover:text-white">
            <X :size="20" />
          </button>
        </div>

        <form @submit.prevent="submitWallet" class="space-y-4">
          <div>
            <label class="block text-xs text-gray-400 uppercase font-bold mb-1">Nome</label>
            <input v-model="form.name" type="text" placeholder="Ex: Conta Principal" required
              class="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-blue-500 outline-none" />
          </div>

          <div class="flex gap-2 bg-gray-900 p-1 rounded-xl border border-gray-700">
            <button type="button" @click="form.type = 'corrente'"
              class="flex-1 py-2 text-sm font-bold rounded-lg transition-all"
              :class="form.type === 'corrente' ? 'bg-blue-500/20 text-blue-400' : 'text-gray-500'">
              Corrente
            </button>
            <button type="button" @click="form.type = 'poupanca'"
              class="flex-1 py-2 text-sm font-bold rounded-lg transition-all"
              :class="form.type === 'poupanca' ? 'bg-purple-500/20 text-purple-400' : 'text-gray-500'">
              Reserva
            </button>
          </div>

          <div class="grid gap-4" :class="form.type === 'poupanca' ? 'grid-cols-2' : 'grid-cols-1'">
            <div>
              <label class="block text-xs text-gray-400 uppercase font-bold mb-1">Saldo Atual</label>
              <div class="relative">
                <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 font-bold">R$</span>
                <input v-model="form.balance" type="number" step="0.01" required placeholder="0.00"
                  class="w-full bg-gray-900 border border-gray-700 rounded-xl py-3 pl-10 pr-3 text-white font-bold focus:ring-2 focus:ring-blue-500 outline-none" />
              </div>
            </div>

            <div v-if="form.type === 'poupanca'">
              <label class="block text-xs text-gray-400 uppercase font-bold mb-1">Meta (Opcional)</label>
              <div class="relative">
                <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 font-bold">R$</span>
                <input v-model="form.goal" type="number" step="0.01" placeholder="0.00"
                  class="w-full bg-gray-900 border border-gray-700 rounded-xl py-3 pl-10 pr-3 text-white font-bold focus:ring-2 focus:ring-purple-500 outline-none" />
              </div>
            </div>
          </div>

          <div>
            <label class="block text-xs text-gray-400 uppercase font-bold mb-1">Cor do Cartão</label>
            <div class="flex gap-2 pt-1">
              <button type="button" v-for="color in presetColors" :key="color" @click="form.color = color"
                class="w-8 h-8 rounded-full border-2 transition-transform"
                :class="form.color === color ? 'border-white scale-110' : 'border-transparent'"
                :style="{ backgroundColor: color }">
              </button>
            </div>
          </div>

          <div>
            <label class="block text-xs text-gray-400 uppercase font-bold mb-1">Descrição</label>
            <input v-model="form.description" type="text" placeholder="Breve descrição"
              class="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-blue-500 outline-none" />
          </div>

          <button type="submit" :disabled="saving"
            class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-4 rounded-xl shadow-lg mt-2 flex justify-center items-center">
            <span v-if="saving" class="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></span>
            <span v-else>{{ isEditing ? 'Salvar Alterações' : 'Criar Carteira' }}</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Plus, Wallet as WalletIcon, Pencil, Trash2, X } from 'lucide-vue-next';
import { useToast } from "vue-toastification";
import Swal from 'sweetalert2';
import api from '../api';
import { refreshTrigger } from '../store';

const toast = useToast();
const wallets = ref([]);
const loading = ref(true);
const saving = ref(false);
const isModalOpen = ref(false);
const isEditing = ref(false);
const editId = ref(null);
const presetColors = ['#8b5cf6', '#f97316', '#22c55e', '#eab308', '#3b82f6'];

const form = ref({
  name: '',
  balance: '',
  goal: '',
  type: 'corrente',
  color: '#8b5cf6',
  description: ''
});

const fetchWallets = async () => {
  loading.value = true;
  try {
    const { data } = await api.get('/wallets/');
    wallets.value = data;
  } catch (err) {
    toast.error("Erro ao carregar carteiras.");
  } finally {
    loading.value = false;
  }
};

const openCreateModal = () => {
  form.value = { name: '', balance: '', goal: '', type: 'corrente', color: presetColors[0], description: '' };
  isEditing.value = false;
  isModalOpen.value = true;
};

const openEditModal = (wallet) => {
  form.value = { 
    name: wallet.name, 
    balance: wallet.balance, 
    goal: wallet.goal || '',
    type: wallet.type || 'corrente', 
    color: wallet.color || presetColors[0], 
    description: wallet.description || '' 
  };
  editId.value = wallet._id;
  isEditing.value = true;
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
};

const submitWallet = async () => {
  saving.value = true;
  try {
    const payload = {
      name: form.value.name,
      balance: parseFloat(form.value.balance) || 0,
      goal: parseFloat(form.value.goal) || 0,
      type: form.value.type,
      color: form.value.color,
      description: form.value.description || null
    };

    if (isEditing.value) {
      await api.put(`/wallets/${editId.value}`, payload);
      toast.success("Carteira atualizada!");
    } else {
      await api.post('/wallets/', payload);
      toast.success("Carteira criada!");
    }

    refreshTrigger.value++; 
    fetchWallets();
    closeModal();
  } catch (err) {
    toast.error("Erro ao salvar.");
  } finally {
    saving.value = false;
  }
};

const deleteWallet = async (id, name) => {
  const result = await Swal.fire({
    title: 'Excluir carteira?',
    text: `Confirmar exclusão da carteira "${name}"?`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#374151',
    confirmButtonText: 'Confirmar',
    background: '#1f2937',
    color: '#fff'
  });

  if (result.isConfirmed) {
    try {
      await api.delete(`/wallets/${id}`);
      toast.success("Carteira excluída!");
      refreshTrigger.value++; 
      fetchWallets();
    } catch (err) {
      toast.error("Erro ao excluir.");
    }
  }
};

onMounted(fetchWallets);
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