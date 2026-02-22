<template>
  <div class="min-h-screen bg-gray-900 text-white pt-5 pb-24 px-4 relative">
    
    <div class="mb-6">
      <h1 class="text-2xl font-bold">Inteligência Financeira</h1>
      <p class="text-gray-400 text-xs">Visão geral do seu dinheiro</p>
    </div>

    <div v-if="loading" class="flex justify-center py-12 opacity-50">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
    </div>

    <div v-else class="space-y-6">
      
      <div class="grid grid-cols-2 gap-3">
        <div class="bg-gray-800 p-4 rounded-2xl border border-gray-700 shadow-sm relative overflow-hidden">
          <p class="text-[10px] text-gray-400 font-bold uppercase mb-1 tracking-wider">Saldo em Contas</p>
          <p class="text-xl font-bold text-blue-400">R$ {{ overview.available_balance.toFixed(2) }}</p>
        </div>
        <div class="bg-gray-800 p-4 rounded-2xl border border-gray-700 shadow-sm relative overflow-hidden">
          <p class="text-[10px] text-gray-400 font-bold uppercase mb-1 tracking-wider">Total Gasto (Mês)</p>
          <p class="text-xl font-bold text-red-400">R$ {{ overview.total_spent.toFixed(2) }}</p>
        </div>
      </div>

      <div class="bg-gradient-to-br from-purple-900 to-gray-800 p-5 rounded-3xl border border-purple-700/50 shadow-lg">
        <div class="flex justify-between items-end mb-3">
          <div>
            <h2 class="text-sm font-bold text-purple-300 uppercase tracking-widest flex items-center gap-2">
              <ShieldAlert :size="16" /> Reserva de Emergência
            </h2>
          </div>
          <span class="text-xl font-bold text-white">{{ reserve.progress_percentage.toFixed(0) }}%</span>
        </div>
        
        <div class="w-full bg-gray-900 rounded-full h-3 mb-2 overflow-hidden border border-gray-700">
          <div class="bg-purple-500 h-3 rounded-full transition-all duration-1000" :style="{ width: `${reserve.progress_percentage}%` }"></div>
        </div>
        
        <div class="flex justify-between text-xs text-gray-400 font-bold">
          <span>Salvo: R$ {{ reserve.total_saved.toFixed(2) }}</span>
          <span>Meta: R$ {{ reserve.total_goal.toFixed(2) }}</span>
        </div>
      </div>

      <div class="bg-gray-800 p-6 rounded-3xl border border-gray-700 shadow-xl">
        <h2 class="text-center text-sm font-bold text-gray-400 uppercase tracking-widest mb-6 flex items-center justify-center gap-2">
          <PieChartIcon :size="16" /> Despesas por Categoria
        </h2>
        
        <div v-if="categoriesData.length > 0" class="relative h-64 w-full flex justify-center mb-6">
          <Doughnut :data="chartData" :options="chartOptions" />
          
          <div class="absolute inset-0 flex flex-col items-center justify-center pointer-events-none mt-2">
            <span class="text-[10px] text-gray-400 font-bold uppercase tracking-widest">Movimentado</span>
            <span class="text-xl font-bold text-white">R$ {{ totalFromCategories.toFixed(2) }}</span>
          </div>
        </div>

        <div v-else class="text-center py-8 text-gray-500">
          <p class="text-sm">Nenhum dado para o gráfico.</p>
        </div>

        <div v-if="categoriesData.length > 0" class="space-y-2 mt-4">
          <div v-for="cat in categoriesData" :key="cat.name" 
            class="bg-gray-900 p-3 rounded-xl flex items-center justify-between border border-gray-700/50">
            
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center text-sm shadow-sm" :style="{ backgroundColor: cat.color + '33', border: '1px solid ' + cat.color }">
                {{ cat.icon }}
              </div>
              <span class="font-bold text-sm text-gray-200">{{ cat.name }}</span>
            </div>
            
            <div class="text-right">
              <p class="font-bold text-white text-sm">R$ {{ cat.total.toFixed(2) }}</p>
              <p class="text-[10px] text-gray-500 font-bold">{{ ((cat.total / totalFromCategories) * 100).toFixed(1) }}%</p>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { Doughnut } from 'vue-chartjs';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { ShieldAlert, PieChart as PieChartIcon } from 'lucide-vue-next';
import api from '../api';

ChartJS.register(ArcElement, Tooltip, Legend);

const loading = ref(true);
const overview = ref({ available_balance: 0, total_spent: 0, transaction_count: 0 });
const reserve = ref({ total_saved: 0, total_goal: 0, progress_percentage: 0 });
const categoriesData = ref([]);

const fetchAnalytics = async () => {
  loading.value = true;
  try {
    const [overviewRes, reserveRes, categoriesRes] = await Promise.all([
      api.get('/analytics/monthly-overview'),
      api.get('/analytics/emergency-reserve'),
      api.get('/analytics/spending-by-category')
    ]);

    overview.value = overviewRes.data;
    reserve.value = reserveRes.data;
    categoriesData.value = categoriesRes.data;

  } catch (err) {
    console.error("Erro ao carregar inteligência financeira:", err);
  } finally {
    loading.value = false;
  }
};

const totalFromCategories = computed(() => {
  return categoriesData.value.reduce((acc, cat) => acc + cat.total, 0);
});

const chartData = computed(() => {
  return {
    labels: categoriesData.value.map(cat => cat.name),
    datasets: [{
      data: categoriesData.value.map(cat => cat.total),
      backgroundColor: categoriesData.value.map(cat => cat.color),
      borderWidth: 0,
      hoverOffset: 8
    }]
  };
});

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  cutout: '75%',
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      backgroundColor: '#1f2937',
      titleColor: '#fff',
      bodyColor: '#fff',
      borderColor: '#374151',
      borderWidth: 1,
      padding: 12,
      callbacks: {
        label: function(context) {
          let label = context.label || '';
          if (label) {
            label += ': ';
          }
          if (context.parsed !== null) {
            label += new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(context.parsed);
          }
          return label;
        }
      }
    }
  }
});

onMounted(fetchAnalytics);
</script>