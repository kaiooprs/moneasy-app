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
            <h2 class="text-xl font-bold text-white">Novo Gasto</h2>
            <p class="text-xs text-gray-400">Para onde foi o dinheiro?</p>
          </div>
          <button @click="isOpen = false" class="bg-gray-700 p-2 rounded-full text-gray-400 hover:text-white">
            <X :size="20" />
          </button>
        </div>

        <form @submit.prevent="submitTransaction" class="space-y-5">
          
          <div>
            <label class="block text-xs text-gray-400 uppercase font-bold mb-1">Valor</label>
            <div class="relative">
              <span class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 font-bold">R$</span>
              <input 
                v-model="form.amount" 
                type="number" 
                step="0.01" 
                class="w-full bg-gray-900 border border-gray-700 rounded-xl py-4 pl-12 pr-4 text-2xl font-bold text-white focus:ring-2 focus:ring-blue-500 outline-none placeholder-gray-600"
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
              placeholder="Ex: Coxinha, Uber, Steam..." 
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
            class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-4 rounded-xl shadow-lg shadow-blue-900/20 flex items-center justify-center gap-2 mt-4 active:scale-95 transition-transform"
            :disabled="loading"
          >
            <span v-if="loading" class="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></span>
            <span v-else>Confirmar Despesa</span>
            <Check v-if="!loading" :size="20" />
          </button>

        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { Plus, X, Check } from 'lucide-vue-next';
import { useToast } from "vue-toastification";
import Swal from 'sweetalert2'; // Import do SweetAlert
import api from '../api';

const isOpen = ref(false);
const loading = ref(false);
const wallets = ref([]);
const categories = ref([]);
const toast = useToast();

// Dados do formulário
const form = ref({
  description: '',
  amount: '',
  wallet_id: '',
  category_id: ''
});

// Busca as listas para preencher os selects
const loadOptions = async () => {
  try {
    const [walletsRes, catsRes] = await Promise.all([
      api.get('/wallets/'),
      api.get('/categories/')
    ]);
    wallets.value = walletsRes.data;
    categories.value = catsRes.data;
    
    // Auto-seleciona a primeira opção
    if (wallets.value.length > 0) form.value.wallet_id = wallets.value[0]._id;
    if (categories.value.length > 0) form.value.category_id = categories.value[0]._id;
    
  } catch (err) {
    console.error("Erro ao carregar opções:", err);
  }
};

const submitTransaction = async () => {
  // 1. Validação Básica (Evita popup se tiver vazio)
  if (!form.value.amount || !form.value.description || !form.value.wallet_id || !form.value.category_id) {
    toast.warning("Preencha todos os campos!");
    return;
  }

  // 2. Confirmação com SweetAlert2
  const result = await Swal.fire({
    title: 'Confirmar Lançamento?',
    html: `
      Você vai lançar um gasto de: <br/>
      <strong style="font-size: 1.2em; color: #ef4444;">R$ ${parseFloat(form.value.amount).toFixed(2)}</strong><br/>
      referente a: <i>${form.value.description}</i>
    `,
    icon: 'question',
    showCancelButton: true,
    confirmButtonColor: '#2563eb', // Azul
    cancelButtonColor: '#374151', // Cinza
    confirmButtonText: 'Sim, confirmar!',
    cancelButtonText: 'Revisar',
    background: '#1f2937', // Dark Mode
    color: '#fff',
    reverseButtons: true
  });

  // 3. Se usuário confirmou, executa a API
  if (result.isConfirmed) {
    loading.value = true;
    try {
      // Usa Math.abs para garantir positivo, pois o backend subtrai
      const payload = {
        description: form.value.description,
        amount: Math.abs(parseFloat(form.value.amount)), 
        wallet_id: form.value.wallet_id,
        category_id: form.value.category_id
      };

      await api.post('/transactions/', payload);
      
      // Sucesso!
      toast.success("Gasto lançado com sucesso!");
      isOpen.value = false;
      
      // Limpa o form
      form.value.description = '';
      form.value.amount = '';
      
      // Recarrega
      setTimeout(() => window.location.reload(), 1000);
      
    } catch (err) {
      // Erro visual no Toast também
      toast.error("Erro ao salvar: " + (err.response?.data?.detail || err.message));
    } finally {
      loading.value = false;
    }
  }
};

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