<template>
  <div class="p-6 pb-24">
    <h1 class="text-2xl font-bold mb-6">Minhas Carteiras</h1>

    <div v-if="wallets.length === 0" class="text-gray-500 text-center py-10">
      Nenhuma carteira encontrada.
    </div>

    <div class="space-y-4">
      <div v-for="wallet in wallets" :key="wallet.id" 
        class="p-5 rounded-2xl border border-gray-700 bg-gray-800 shadow-md">
        <div class="flex justify-between items-start">
          <div>
            <p class="text-gray-400 text-xs uppercase">{{ wallet.type }}</p>
            <h3 class="text-lg font-bold">{{ wallet.name }}</h3>
          </div>
          <span class="text-green-400 font-mono font-bold">
            R$ {{ wallet.balance.toFixed(2) }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import api from '../api';

const wallets = ref([]);

const fetchWallets = async () => {
  try {
    const { data } = await api.get('/wallets/');
    wallets.value = data;
  } catch (err) {
    console.error("Erro ao carregar carteiras", err);
  }
};

onMounted(fetchWallets);
</script>