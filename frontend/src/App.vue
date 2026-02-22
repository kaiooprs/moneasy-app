<template>
  <div class="min-h-screen bg-gray-900 text-white font-sans relative">
    
    <TopBar v-if="$route.path !== '/login'" />
    
    <router-view />
    
    <NewTransactionModal v-if="$route.path !== '/login'" />

    <BottomNav v-if="$route.path !== '/login'" />
    
  </div>
</template>

<script setup>
import BottomNav from './components/BottomNav.vue';
import TopBar from './components/TopBar.vue';
import NewTransactionModal from './components/NewTransactionModal.vue';
</script>