<template>
  <div class="min-h-screen bg-gray-900 text-white pt-5 pb-24 px-4"> 
    
    <div class="mb-6 flex justify-between items-end border-b border-gray-800 pb-4">
      <div>
        <h1 class="text-2xl font-bold">Extrato</h1>
        <p class="text-gray-400 text-xs">Histórico completo</p>
      </div>
      
      <div class="text-right">
        <span class="text-[10px] text-gray-500 uppercase font-bold tracking-wider">Total Listado</span>
        <p class="text-lg font-bold text-white leading-none">
          {{ transactions.length }}
        </p>
      </div>
    </div>

    <div class="space-y-3">
      
      <div v-if="loading" class="flex justify-center py-10 opacity-50">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>

      <div v-else-if="transactions.length === 0" class="text-center py-12 text-gray-500">
        <p>Nenhum lançamento por aqui.</p>
      </div>

      <div v-for="t in transactions" :key="t._id" 
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
            <p class="font-bold font-mono text-sm" 
              :class="t.type === 'income' ? 'text-green-400' : 'text-red-400'">
              {{ t.type === 'income' ? '+' : '-' }} R$ {{ Math.abs(t.amount).toFixed(2) }}
            </p>
          </div>
        </div>

        <div class="mt-3 pt-3 border-t border-gray-700/50 flex justify-end gap-4 opacity-100 sm:opacity-0 sm:group-hover:opacity-100 transition-opacity">
          
          <button @click="editTransaction(t)" class="flex items-center gap-1 text-xs text-blue-400 hover:text-blue-300 font-medium">
            <Pencil :size="14" /> Editar
          </button>
          
          <button @click="confirmDelete(t._id)" class="flex items-center gap-1 text-xs text-red-400 hover:text-red-300 font-medium">
            <Trash2 :size="14" /> Excluir
          </button>

        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import api from '../api';
import { useToast } from "vue-toastification";
import Swal from 'sweetalert2';
import { refreshTrigger } from '../store';
import { 
  ShoppingBag, Utensils, Car, Zap, Gamepad2, 
  Home, Briefcase, HelpCircle, Trash2, Pencil 
} from 'lucide-vue-next';

const transactions = ref([]);
const loading = ref(true);
const toast = useToast();

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

const editTransaction = (transaction) => {
  toast.info(`Funcionalidade de edição para "${transaction.description}" em breve.`);
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