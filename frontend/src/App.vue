<template>
  <div class="min-h-screen bg-gray-900 text-white font-sans relative">
    
    <TopBar v-if="$route.path !== '/login'" />
    
    <router-view />
    
    <NewTransactionModal v-if="$route.path !== '/login'" />

    <BottomNav v-if="$route.path !== '/login'" />
    
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import BottomNav from './components/BottomNav.vue';
import TopBar from './components/TopBar.vue';
import NewTransactionModal from './components/NewTransactionModal.vue';
import { db } from './services/offlineDb';
import api from './api';

const syncOfflineData = async () => {
  const offlineData = await db.transactions.where({ synced: false }).toArray();

  if (offlineData.length > 0) {
    for (const item of offlineData) {
      try {
        await api.post('/transactions/', item);
        await db.transactions.delete(item.id);
      } catch (e) {
        console.error(e);
      }
    }
  }
};

onMounted(() => {
  syncOfflineData();
  window.addEventListener('online', syncOfflineData);
});
</script>