<template>
  <div>
    <button 
      @click="isOpen = true"
      class="fixed bottom-24 right-6 bg-blue-600 hover:bg-blue-500 text-white p-4 rounded-full shadow-lg shadow-blue-900/50 z-40 transition-transform active:scale-90 flex items-center justify-center"
    >
      <Plus :size="28" stroke-width="3" />
    </button>

    <div v-if="isOpen" class="fixed inset-0 z-[100] flex items-end sm:items-center justify-center px-4 py-6">
      
      <div class="absolute inset-0 bg-black/80 backdrop-blur-sm transition-opacity" @click="isOpen = false"></div>

      <div class="bg-gray-800 w-full max-w-md rounded-3xl p-6 relative shadow-2xl border border-gray-700 transform transition-all animate-slide-up mb-6 sm:mb-0">
        
        <div class="flex justify-between items-center mb-6">
          <div>
            <h2 class="text-xl font-bold text-white">Novo Lançamento</h2>
            <p class="text-xs text-gray-400">Entrou ou saiu dinheiro?</p>
          </div>
          <button @click="isOpen = false" class="bg-gray-700 p-2 rounded-full text-gray-400 hover:text-white transition-colors">
            <X :size="20" />
          </button>
        </div>

        <form @submit.prevent="submitTransaction" class="space-y-5">
          
          <div class="flex gap-2 bg-gray-900 p-1.5 rounded-xl border border-gray-700">
            <button 
              type="button" 
              @click="form.type = 'income'"
              class="flex-1 py-2.5 text-sm font-bold rounded-lg transition-all flex justify-center items-center gap-2"
              :class="form.type === 'income' ? 'bg-green-500/20 text-green-400 shadow-sm' : 'text-gray-500 hover:text-gray-300'"
            >
              <ArrowUpCircle :size="18" /> Entrada
            </button>
            <button 
              type="button" 
              @click="form.type = 'expense'"
              class="flex-1 py-2.5 text-sm font-bold rounded-lg transition-all flex justify-center items-center gap-2"
              :class="form.type === 'expense' ? 'bg-red-500/20 text-red-400 shadow-sm' : 'text-gray-500 hover:text-gray-300'"
            >
              <ArrowDownCircle :size="18" /> Saída
            </button>
          </div>

          <div>
            <label class="block text-xs text-gray-400 uppercase font-bold mb-1">Valor</label>
            <div class="relative">
              <span class="absolute left-4 top-1/2 -translate-y-1/2 font-bold"
                    :class="form.type === 'income' ? 'text-green-500' : 'text-red-500'">R$</span>
              <input 
                v-model="form.amount" 
                type="number" 
                step="0.01" 
                class="w-full bg-gray-900 border border-gray-700 rounded-xl py-4 pl-12 pr-4 text-2xl font-bold text-white focus:ring-2 outline-none placeholder-gray-600 transition-shadow"
                :class="form.type === 'income' ? 'focus:ring-green-500' : 'focus:ring-red-500'"
                placeholder="0,00" 
                required
              />
            </div>
          </div>

          <div>
            <label class="block text-xs text-gray-400 uppercase font-bold mb-1">Descrição</label>
            <input 
              v-model="form.description" 
              type="text" 
              class="w-full bg-gray-700 border border-gray-600 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-blue-500 outline-none"
              placeholder="Ex: Salário, Mercado, Pix..." 
              required
            />
          </div>

          <div class="grid grid-cols-2 gap-4">
            
            <div>
              <label class="block text-xs text-gray-400 uppercase font-bold mb-1">Carteira</label>
              <select 
                v-model="form.wallet_id" 
                class="w-full bg-gray-700 border border-gray-600 rounded-xl px-3 py-3 text-white text-sm focus:ring-2 focus:ring-blue-500 outline-none appearance-none"
                required
              >
                <option value="" disabled>Escolher...</option>
                <option v-for="w in wallets" :key="w._id" :value="w._id">
                  {{ w.name }}
                </option>
              </select>
            </div>

            <div>
              <label class="block text-xs text-gray-400 uppercase font-bold mb-1">Categoria</label>
              <select 
                v-model="form.category_id" 
                class="w-full bg-gray-700 border border-gray-600 rounded-xl px-3 py-3 text-white text-sm focus:ring-2 focus:ring-blue-500 outline-none appearance-none"
                required
              >
                <option value="" disabled>Escolher...</option>
                <option v-for="c in categories" :key="c._id" :value="c._id">
                  {{ c.name }}
                </option>
              </select>
            </div>
          </div>

          <button 
            type="submit" 
            class="w-full text-white font-bold py-4 rounded-xl shadow-lg flex items-center justify-center gap-2 mt-4 active:scale-95 transition-all"
            :class="form.type === 'income' ? 'bg-green-600 hover:bg-green-500 shadow-green-900/20' : 'bg-red-600 hover:bg-red-500 shadow-red-900/20'"
            :disabled="loading"
          >
            <span v-if="loading" class="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></span>
            <span v-else>{{ form.type === 'income' ? 'Confirmar Entrada' : 'Confirmar Saída' }}</span>
            <Check v-if="!loading" :size="20" />
          </button>

        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { Plus, X, Check, ArrowUpCircle, ArrowDownCircle } from 'lucide-vue-next';
import { useToast } from "vue-toastification";
import { refreshTrigger } from '../store';
import Swal from 'sweetalert2';
import api from '../api';
import { db } from '../services/offlineDb';

const isOpen = ref(false);
const loading = ref(false);
const wallets = ref([]);
const categories = ref([]);
const toast = useToast();

const form = ref({
  description: '',
  amount: '',
  wallet_id: '',
  category_id: '',
  type: 'expense'
});

const loadOptions = async () => {
  try {
    const [walletsRes, catsRes] = await Promise.all([
      api.get('/wallets/'),
      api.get('/categories/')
    ]);
    wallets.value = walletsRes.data;
    categories.value = catsRes.data;
    
    if (wallets.value.length > 0) form.value.wallet_id = wallets.value[0]._id;
    if (categories.value.length > 0) form.value.category_id = categories.value[0]._id;
    
  } catch (err) {
    console.error("Erro ao carregar opções:", err);
  }
};

const submitTransaction = async () => {
  if (!form.value.amount || !form.value.description || !form.value.wallet_id || !form.value.category_id) {
    toast.warning("Preencha todos os campos!");
    return;
  }

  const isIncome = form.value.type === 'income';
  const colorHex = isIncome ? '#22c55e' : '#ef4444';
  const typeText = isIncome ? 'uma entrada' : 'um gasto';

  const result = await Swal.fire({
    title: 'Confirmar Lançamento?',
    html: `
      Você vai registrar ${typeText} de: <br/>
      <strong style="font-size: 1.2em; color: ${colorHex};">R$ ${parseFloat(form.value.amount).toFixed(2)}</strong><br/>
      referente a: <i>${form.value.description}</i>
    `,
    icon: 'question',
    showCancelButton: true,
    confirmButtonColor: colorHex,
    cancelButtonColor: '#374151',
    confirmButtonText: 'Sim, confirmar!',
    cancelButtonText: 'Revisar',
    background: '#1f2937',
    color: '#fff',
    reverseButtons: true
  });

  if (result.isConfirmed) {
    loading.value = true;
    
    const payload = {
      description: form.value.description,
      amount: Math.abs(parseFloat(form.value.amount)), 
      wallet_id: form.value.wallet_id,
      category_id: form.value.category_id,
      type: form.value.type,
      date: new Date().toISOString()
    };

    try {
      await api.post('/transactions/', payload);
      toast.success("Lançamento salvo com sucesso!");
      isOpen.value = false;
    } catch (err) {
      await db.transactions.add({
        ...payload,
        synced: false
      });
      toast.info("Você está offline! Salvo no dispositivo para sincronização.");
      isOpen.value = false;
    } finally {
      form.value.description = '';
      form.value.amount = '';
      form.value.type = 'expense'; 
      refreshTrigger.value++;
      loading.value = false;
    }
  }
};

watch(refreshTrigger, () => {
  loadOptions();
});

onMounted(() => {
  loadOptions();
});
</script>

<style scoped>
.animate-slide-up {
  animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes slideUp {
  from { transform: translateY(100%); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
</style>