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
import { refreshTrigger } from './store';

const syncOfflineData = async () => {
  try {
    const allData = await db.transactions.toArray();
        
    const offlineData = allData.filter(item => item.synced === false);

    if (offlineData.length > 0) {
      for (const item of offlineData) {
        try {          
          const { id, synced, ...payloadReadyForRender } = item;
                    
          await api.post('/transactions/', payloadReadyForRender);
          
          await db.transactions.delete(item.id);

          refreshTrigger.value++;
          
          console.log('Sincronizado com sucesso:', item.description);
        } catch (apiError) {
          console.error('Falha na API ou Render ainda dormindo:', apiError);
        }
      }
    }
  } catch (dbError) {
    console.error('Erro de leitura no banco local:', dbError);
  }
};

onMounted(() => {
  syncOfflineData();
  window.addEventListener('online', syncOfflineData);
});
</script>