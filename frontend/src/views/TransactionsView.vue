<template>
  <div class="min-h-screen bg-gray-900 text-white pt-5 pb-24 px-4"> 
    
    <div class="mb-6 border-b border-gray-800 pb-4">
      <div class="flex justify-between items-center mb-4">
        <div>
          <h1 class="text-2xl font-bold">Extrato</h1>
          <p class="text-gray-400 text-xs">Histórico de lançamentos</p>
        </div>
        <div class="text-right">
          <span class="text-[10px] text-gray-500 uppercase font-bold tracking-wider">Total no Mês</span>
          <p class="text-lg font-bold text-white leading-none">{{ filteredTransactions.length }}</p>
        </div>
      </div>

      <div class="flex items-center gap-2 bg-gray-800 p-2 rounded-xl border border-gray-700">
        <Calendar :size="18" class="text-blue-400 ml-2" />
        <input 
          type="month" 
          v-model="selectedPeriod"
          class="bg-transparent text-sm font-bold text-white outline-none w-full appearance-none"
        />
      </div>
    </div>

    <div class="space-y-3">
      <div v-if="loading" class="flex justify-center py-10 opacity-50">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>

      <div v-else-if="filteredTransactions.length === 0" class="text-center py-12 text-gray-500 bg-gray-800/30 rounded-2xl border border-dashed border-gray-700">
        <p>Nenhum lançamento encontrado para este período.</p>
      </div>

      <div v-for="t in filteredTransactions" :key="t._id" 
        class="group bg-gray-800 p-4 rounded-2xl border border-gray-700/50 shadow-sm relative overflow-hidden transition-all hover:border-gray-600">
        
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-gray-700 flex items-center justify-center text-xl">
              <span v-if="t.category_id?.icon">{{ t.category_id.icon }}</span>
              <component v-else :is="getCategoryIcon(t.category)" :size="18" class="text-gray-300" />
            </div>
            <div>
              <h3 class="font-bold text-sm text-gray-100">{{ t.description }}</h3>
              <div class="flex items-center gap-2 text-[11px] text-gray-400">
                <span>{{ formatDate(t.date) }}</span>
                <span class="w-1 h-1 bg-gray-600 rounded-full"></span>
                <span class="capitalize">{{ t.category }}</span>
              </div>
            </div>
          </div>
          <div class="text-right">
            <p class="font-bold font-mono text-sm" :class="t.type === 'income' ? 'text-green-400' : 'text-red-400'">
              {{ t.type === 'income' ? '+' : '-' }} R$ {{ Math.abs(t.amount).toFixed(2) }}
            </p>
          </div>
        </div>

        <div class="mt-3 pt-3 border-t border-gray-700/50 flex justify-end gap-4">
          <button @click="openEditModal(t)" class="flex items-center gap-1 text-xs text-blue-400 hover:text-blue-300 font-medium">
            <Pencil :size="14" /> Editar
          </button>
          <button @click="confirmDelete(t._id)" class="flex items-center gap-1 text-xs text-red-400 hover:text-red-300 font-medium">
            <Trash2 :size="14" /> Excluir
          </button>
        </div>
      </div>
    </div>

    <div v-if="showEditModal" class="fixed inset-0 z-[100] flex items-end sm:items-center justify-center px-4 py-6">
      <div class="absolute inset-0 bg-black/80 backdrop-blur-sm" @click="showEditModal = false"></div>
      <div class="bg-gray-800 w-full max-w-md rounded-3xl p-6 relative shadow-2xl border border-gray-700 animate-slide-up">
        <h2 class="text-xl font-bold mb-6">Editar Transação</h2>
        
        <form @submit.prevent="updateTransaction" class="space-y-4">
          <div>
            <label class="block text-xs text-gray-400 uppercase font-bold mb-1">Descrição</label>
            <input v-model="editForm.description" type="text" required class="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-blue-500 outline-none" />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs text-gray-400 uppercase font-bold mb-1">Valor</label>
              <input v-model="editForm.amount" type="number" step="0.01" required class="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-blue-500 outline-none" />
            </div>
            <div>
              <label class="block text-xs text-gray-400 uppercase font-bold mb-1">Data</label>
              <input v-model="editForm.date" type="date" required class="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-blue-500 outline-none" />
            </div>
          </div>

          <button type="submit" :disabled="saving" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-4 rounded-xl shadow-lg mt-4 flex justify-center items-center">
            <span v-if="saving" class="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></span>
            <span v-else>Salvar Alterações</span>
          </button>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import api from '../api';
import { useToast } from "vue-toastification";
import Swal from 'sweetalert2';
import { refreshTrigger } from '../store';
import { 
  ShoppingBag, Utensils, Car, Zap, Gamepad2, 
  Home, Briefcase, HelpCircle, Trash2, Pencil, Calendar 
} from 'lucide-vue-next';

const transactions = ref([]);
const loading = ref(true);
const saving = ref(false);
const toast = useToast();

// Seletor de período (formato YYYY-MM para o input type="month")
const selectedPeriod = ref(new Date().toISOString().substring(0, 7));

// Modal de Edição
const showEditModal = ref(false);
const editForm = ref({ id: null, description: '', amount: 0, date: '', type: '' });

// Filtro por Mês e Ano
const filteredTransactions = computed(() => {
  const [year, month] = selectedPeriod.value.split('-').map(Number);
  return transactions.value.filter(t => {
    const d = new Date(t.date);
    return d.getMonth() + 1 === month && d.getFullYear() === year;
  });
});

const openEditModal = (t) => {
  editForm.value = {
    id: t._id,
    description: t.description,
    amount: Math.abs(t.amount),
    date: new Date(t.date).toISOString().substring(0, 10),
    type: t.type
  };
  showEditModal.value = true;
};

const updateTransaction = async () => {
  saving.value = true;
  try {
    const payload = {
      description: editForm.value.description,
      amount: editForm.value.type === 'expense' ? -Math.abs(editForm.value.amount) : Math.abs(editForm.value.amount),
      date: editForm.value.date
    };
    await api.put(`/transactions/${editForm.value.id}`, payload);
    toast.success("Atualizado com sucesso!");
    showEditModal.value = false;
    refreshTrigger.value++;
    fetchTransactions();
  } catch (err) {
    toast.error("Erro ao atualizar.");
  } finally {
    saving.value = false;
  }
};

const confirmDelete = async (id) => {
  const result = await Swal.fire({
    title: 'Tem certeza?',
    text: "Esta ação não pode ser desfeita.",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#374151',
    confirmButtonText: 'Sim, excluir!',
    cancelButtonText: 'Cancelar',
    background: '#1f2937',
    color: '#fff'
  });

  if (result.isConfirmed) {
    try {
      await api.delete(`/transactions/${id}`);
      transactions.value = transactions.value.filter(t => t._id !== id);
      toast.success("Transação excluída!");
      refreshTrigger.value++;
    } catch (err) {
      toast.error("Erro ao excluir.");
    }
  }
};

const getCategoryIcon = (category) => {
  const map = {
    'alimentação': Utensils, 'food': Utensils,
    'transporte': Car, 'transport': Car,
    'lazer': Gamepad2, 'jogos': Gamepad2,
    'casa': Home, 'housing': Home,
    'contas': Zap, 'utilities': Zap,
    'salário': Briefcase, 'salary': Briefcase,
    'compras': ShoppingBag, 'shopping': ShoppingBag
  };
  return map[category?.toLowerCase()] || HelpCircle;
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('pt-BR', { day: '2-digit', month: '2-digit' }).format(date);
};

const fetchTransactions = async () => {
  try {
    loading.value = true;
    const { data } = await api.get('/transactions/');
    transactions.value = data.sort((a, b) => new Date(b.date) - new Date(a.date));
  } catch (err) {
    console.error("Erro ao buscar extrato");
  } finally {
    loading.value = false;
  }
};

watch(refreshTrigger, () => {
  fetchTransactions();
});

onMounted(fetchTransactions);
</script>

<style scoped>
.animate-slide-up {
  animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes slideUp {
  from { transform: translateY(100%); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
input[type="month"]::-webkit-calendar-picker-indicator {
  filter: invert(1);
  cursor: pointer;
}
</style>