<template>
  <div class="p-6 pb-24 text-white">
    <header class="mb-6">
      <h1 class="text-2xl font-bold">Assinaturas e Fixos</h1>
      <p class="text-gray-400 text-sm">Controle seus gastos mensais</p>
    </header>

    <div v-if="subscriptions.length === 0" class="text-center py-10 text-gray-500">
      Nenhuma assinatura encontrada.
    </div>

    <div class="space-y-4">
      <div v-for="sub in subscriptions" :key="sub._id" 
        class="bg-gray-800 border border-gray-700 p-4 rounded-2xl flex items-center justify-between shadow-sm">
        
        <div class="flex items-center gap-4">
          <div class="p-3 bg-gray-700 rounded-xl text-blue-400">
            <Calendar :size="20" />
          </div>
          <div>
            <h3 class="font-bold text-white">{{ sub.name }}</h3>
            <p class="text-xs text-gray-400 capitalize">{{ sub.frequency }} • Vence dia {{ sub.due_day }}</p>
          </div>
        </div>

        <div class="text-right">
          <p class="font-bold text-lg text-white">R$ {{ sub.amount.toFixed(2) }}</p>
          <span :class="sub.is_paid ? 'text-green-400' : 'text-yellow-400'" 
            class="text-[10px] px-2 py-0.5 rounded-full font-bold uppercase border border-current opacity-80">
            {{ sub.is_paid ? 'Pago' : 'Pendente' }}
          </span>
        </div>
      </div>
    </div>

    <div v-if="subscriptions.length > 0" class="mt-8 p-4 bg-blue-600/10 border border-blue-500/20 rounded-xl">
      <div class="flex justify-between items-center text-blue-400">
        <span class="text-sm font-medium">Comprometido este mês:</span>
        <span class="text-lg font-bold">R$ {{ totalSubscriptions.toFixed(2) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import { Calendar } from 'lucide-vue-next';
import api from '../api';

const subscriptions = ref([]);

const totalSubscriptions = computed(() => {
  return subscriptions.value.reduce((acc, sub) => acc + (sub.amount || 0), 0);
});

const fetchSubscriptions = async () => {
  try {
    const { data } = await api.get('/subscriptions/');
    subscriptions.value = data;
  } catch (err) {
    console.error("Erro ao buscar assinaturas:", err);
  }
};

onMounted(fetchSubscriptions);
</script>