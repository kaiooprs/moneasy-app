<template>
  <nav class="fixed bottom-0 left-0 right-0 bg-gray-800/95 backdrop-blur-lg border-t border-gray-700 pb-6 pt-3 px-1 z-50">
    <div class="flex justify-around items-center max-w-lg mx-auto">
      
      <router-link to="/dashboard" class="flex flex-col items-center gap-1 min-w-[60px]"
        :class="$route.path === '/dashboard' ? 'text-blue-500' : 'text-gray-500 hover:text-gray-300'">
        <LayoutDashboard :size="22" />
        <span class="text-[9px] font-bold uppercase tracking-tight">Início</span>
      </router-link>

      <router-link to="/wallets" class="flex flex-col items-center gap-1 min-w-[60px]"
        :class="$route.path === '/wallets' ? 'text-blue-500' : 'text-gray-500 hover:text-gray-300'">
        <Wallet :size="22" />
        <span class="text-[9px] font-bold uppercase tracking-tight">Carteiras</span>
      </router-link>

      <router-link to="/transactions" class="flex flex-col items-center gap-1 min-w-[60px]"
        :class="$route.path === '/transactions' ? 'text-blue-500' : 'text-gray-500 hover:text-gray-300'">
        <ScrollText :size="22" /> 
        <span class="text-[9px] font-bold uppercase tracking-tight">Extrato</span>
      </router-link>

      <router-link to="/subscriptions" class="flex flex-col items-center gap-1 min-w-[60px]"
        :class="$route.path === '/subscriptions' ? 'text-blue-500' : 'text-gray-500 hover:text-gray-300'">
        <CalendarClock :size="22" />
        <span class="text-[9px] font-bold uppercase tracking-tight">Fixos</span>
      </router-link>

      <router-link to="/analytics" class="flex flex-col items-center gap-1 min-w-[60px]"
        :class="$route.path === '/analytics' ? 'text-blue-500' : 'text-gray-500 hover:text-gray-300'">
        <PieChart :size="22" />
        <span class="text-[9px] font-bold uppercase tracking-tight">Análises</span>
      </router-link>

    </div>
  </nav>
</template>

<script setup>
import { LayoutDashboard, Wallet, ScrollText, CalendarClock, PieChart } from 'lucide-vue-next';
</script>