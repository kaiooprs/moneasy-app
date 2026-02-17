<template>
  <div class="min-h-screen bg-gray-900 text-white pt-20 pb-24 px-4">
    
    <div class="grid grid-cols-2 gap-3 mb-6">
      <div class="bg-gray-800 p-4 rounded-2xl border border-gray-700 shadow-sm relative overflow-hidden">
        <div class="absolute top-0 right-0 p-3 opacity-10">
          <ArrowDownCircle :size="48" />
        </div>
        <p class="text-xs text-gray-400 font-bold uppercase mb-1">Saídas (Mês)</p>
        <p class="text-xl font-bold text-red-400">R$ {{ monthExpense.toFixed(2) }}</p>
      </div>

      <div class="bg-gray-800 p-4 rounded-2xl border border-gray-700 shadow-sm relative overflow-hidden">
        <div class="absolute top-0 right-0 p-3 opacity-10">
          <ArrowUpCircle :size="48" />
        </div>
        <p class="text-xs text-gray-400 font-bold uppercase mb-1">Entradas (Mês)</p>
        <p class="text-xl font-bold text-green-400">R$ {{ monthIncome.toFixed(2) }}</p>
      </div>
    </div>

    <div class="bg-gradient-to-r from-blue-600 to-blue-800 rounded-2xl p-4 mb-8 flex items-center justify-between shadow-lg shadow-blue-900/20">
      <div>
        <h3 class="font-bold text-lg">Balanço Mensal</h3>
        <p class="text-xs text-blue-100 opacity-80">Seu saldo líquido este mês</p>
      </div>
      <div class="text-right">
        <p class="text-2xl font-bold">R$ {{ (monthIncome - monthExpense).toFixed(2) }}</p>
      </div>
    </div>

    <div class="flex justify-between items-end mb-4">
      <h2 class="text-lg font-bold">Últimos Lançamentos</h2>
      <button @click="$router.push('/transactions')" class="text-xs text-blue-400 font-bold hover:underline">Ver tudo</button>
    </div>

    <div v-if="loading" class="flex justify-center py-6 opacity-50">
      <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
    </div>

    <div v-else-if="recentTransactions.length === 0" class="text-center py-8 text-gray-500 bg-gray-800/50 rounded-2xl border border-dashed border-gray-700">
      <p class="text-sm">Nada por aqui ainda.</p>
    </div>

    <div class="space-y-3">
      <div v-for="t in recentTransactions" :key="t._id" 
        class="bg-gray-800 p-4 rounded-2xl flex items-center justify-between border border-gray-700/50">
        
        <div class="flex items-center gap-3">
          <div class="p-2 rounded-lg bg-gray-700 text-gray-300">
            <component :is="getCategoryIcon(t.category)" :size="18" />
          </div>
          <div>
            <h3 class="font-bold text-sm">{{ t.description }}</h3>
            <p class="text-[10px] text-gray-400 capitalize">{{ formatDate(t.date) }}</p>
          </div>
        </div>

        <span class="font-bold font-mono text-sm" 
          :class="t.amount < 0 ? 'text-red-400' : 'text-green-400'">
          {{ t.amount < 0 ? '-' : '+' }} R$ {{ Math.abs(t.amount).toFixed(2) }}
        </span>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '../api';
import { 
  ArrowDownCircle, ArrowUpCircle, ShoppingBag, Utensils, 
  Car, Zap, Gamepad2, Home, Briefcase, HelpCircle 
} from 'lucide-vue-next';

const transactions = ref([]);
const loading = ref(true);

// Filtra e calcula totais
const monthExpense = computed(() => {
  return transactions.value
    .filter(t => t.amount < 0)
    .reduce((acc, t) => acc + Math.abs(t.amount), 0);
});

const monthIncome = computed(() => {
  return transactions.value
    .filter(t => t.amount > 0)
    .reduce((acc, t) => acc + t.amount, 0);
});

// Pega só as 5 últimas para exibir
const recentTransactions = computed(() => {
  return transactions.value.slice(0, 5);
});

// --- Utilitários (Mesmos da TransactionsView) ---
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

const fetchData = async () => {
  try {
    const { data } = await api.get('/transactions/');
    // Ordena por data (mais recente primeiro)
    transactions.value = data.sort((a, b) => new Date(b.date) - new Date(a.date));
  } catch (err) {
    console.error("Erro ao carregar dashboard", err);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchData);
</script>