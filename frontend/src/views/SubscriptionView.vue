<template>
  <div class="min-h-screen bg-gray-900 text-white pt-5 pb-24 px-4 relative">
    
    <div class="mb-6 flex justify-between items-end">
      <div>
        <h1 class="text-2xl font-bold">Fixos</h1>
        <p class="text-gray-400 text-xs">Assinaturas e contas recorrentes</p>
      </div>
      <button 
        @click="openCreateModal" 
        class="bg-blue-600 hover:bg-blue-500 text-white p-2 px-4 rounded-xl shadow-lg flex items-center gap-2 text-sm font-bold transition-transform active:scale-95"
      >
        <Plus :size="18" /> Novo
      </button>
    </div>

    <div v-if="loading" class="flex justify-center py-10 opacity-50">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
    </div>

    <div v-else class="space-y-4">
      <div v-for="sub in sortedSubscriptions" :key="sub._id" 
        class="bg-gray-800 p-5 rounded-3xl border shadow-sm relative overflow-hidden transition-all"
        :class="sub.is_paid ? 'border-green-500/30 opacity-70' : 'border-gray-700'"
      >
        <div class="flex justify-between items-start mb-4">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-2xl shadow-sm"
                 :style="{ backgroundColor: (sub.category_id?.color || '#374151') + '33', border: '1px solid ' + (sub.category_id?.color || '#374151') }">
              {{ sub.category_id?.icon || '📌' }}
            </div>
            <div>
              <h3 class="font-bold text-lg text-white" :class="{'line-through text-gray-400': sub.is_paid}">
                {{ sub.name }}
              </h3>
              <p class="text-xs font-bold text-gray-400 flex items-center gap-1 mt-0.5">
                <Calendar :size="12" /> Vence dia {{ sub.due_day }}
              </p>
            </div>
          </div>
          
          <div class="flex gap-2">
            <button @click="openEditModal(sub)" class="text-gray-400 hover:text-blue-400 transition-colors p-2 bg-gray-900 rounded-lg">
              <Pencil :size="16" />
            </button>
            <button @click="deleteSubscription(sub._id)" class="text-gray-400 hover:text-red-400 transition-colors p-2 bg-gray-900 rounded-lg">
              <Trash2 :size="16" />
            </button>
          </div>
        </div>

        <div class="flex items-center justify-between mt-2 pt-4 border-t border-gray-700/50">
          <p class="text-2xl font-bold text-red-400" :class="{'text-gray-500': sub.is_paid}">
            R$ {{ sub.amount.toFixed(2) }}
          </p>
          
          <button v-if="!sub.is_paid" @click="paySubscription(sub)"
            class="bg-green-600/20 text-green-400 hover:bg-green-600 hover:text-white px-4 py-2 rounded-xl font-bold text-sm transition-colors flex items-center gap-2">
            <Circle :size="16" /> Marcar Pago
          </button>
          
          <div v-else class="flex items-center gap-1 text-green-400 font-bold text-sm px-4 py-2">
            <CheckCircle :size="16" /> Pago
          </div>
        </div>
      </div>

      <div v-if="subscriptions.length === 0" class="text-center py-12 text-gray-500 bg-gray-800/50 rounded-2xl border border-dashed border-gray-700">
        <p>Nenhuma conta fixa cadastrada.</p>
      </div>
    </div>

    <div v-if="isModalOpen" class="fixed inset-0 z-[100] flex items-end sm:items-center justify-center px-4 py-6">
      <div class="absolute inset-0 bg-black/80 backdrop-blur-sm transition-opacity" @click="closeModal"></div>

      <div class="bg-gray-800 w-full max-w-md rounded-3xl p-6 relative shadow-2xl border border-gray-700 transform transition-all mb-6 sm:mb-0">
        
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-bold text-white">{{ isEditing ? 'Editar Fixo' : 'Novo Fixo' }}</h2>
          <button @click="closeModal" class="bg-gray-700 p-2 rounded-full text-gray-400 hover:text-white">
            <X :size="20" />
          </button>
        </div>

        <form @submit.prevent="submitSubscription" class="space-y-4">
          <div>
            <label class="block text-xs text-gray-400 uppercase font-bold mb-1">Nome</label>
            <input v-model="form.name" type="text" placeholder="Ex: Assinatura, Aluguel" required
              class="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-blue-500 outline-none" />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs text-gray-400 uppercase font-bold mb-1">Valor</label>
              <div class="relative">
                <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 font-bold">R$</span>
                <input v-model="form.amount" type="number" step="0.01" required placeholder="0.00"
                  class="w-full bg-gray-900 border border-gray-700 rounded-xl py-3 pl-10 pr-3 text-white font-bold focus:ring-2 focus:ring-blue-500 outline-none" />
              </div>
            </div>

            <div>
              <label class="block text-xs text-gray-400 uppercase font-bold mb-1">Dia do Vencimento</label>
              <input v-model="form.due_day" type="number" min="1" max="31" required placeholder="Ex: 10"
                class="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-blue-500 outline-none" />
            </div>
          </div>

          <div>
            <label class="block text-xs text-gray-400 uppercase font-bold mb-1">Categoria</label>
            <select v-model="form.category_id" required
              class="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-blue-500 outline-none appearance-none">
              <option value="" disabled>Selecione...</option>
              <option v-for="cat in categories" :key="cat._id" :value="cat._id">
                {{ cat.icon }} {{ cat.name }}
              </option>
            </select>
          </div>

          <button type="submit" :disabled="saving"
            class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-4 rounded-xl shadow-lg mt-2 flex justify-center items-center">
            <span v-if="saving" class="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></span>
            <span v-else>Salvar Alterações</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { Plus, Pencil, Trash2, X, Calendar, Circle, CheckCircle } from 'lucide-vue-next';
import { useToast } from "vue-toastification";
import Swal from 'sweetalert2';
import api from '../api';
import { refreshTrigger } from '../store';

const toast = useToast();
const subscriptions = ref([]);
const categories = ref([]);
const wallets = ref([]);
const loading = ref(true);
const saving = ref(false);

const isModalOpen = ref(false);
const isEditing = ref(false);
const editId = ref(null);

const form = ref({
  name: '',
  amount: '',
  due_day: '',
  category_id: ''
});

const sortedSubscriptions = computed(() => {
  return [...subscriptions.value].sort((a, b) => a.due_day - b.due_day);
});

const fetchData = async () => {
  loading.value = true;
  try {
    const [subRes, catRes, walletRes] = await Promise.all([
      api.get('/subscriptions/'),
      api.get('/categories/'),
      api.get('/wallets/')
    ]);
    subscriptions.value = subRes.data;
    categories.value = catRes.data;
    wallets.value = walletRes.data;
  } catch (err) {
    toast.error("Erro ao carregar dados.");
  } finally {
    loading.value = false;
  }
};

const openCreateModal = () => {
  form.value = { name: '', amount: '', due_day: '', category_id: '' };
  isEditing.value = false;
  isModalOpen.value = true;
};

const openEditModal = (sub) => {
  form.value = { 
    name: sub.name, 
    amount: sub.amount, 
    due_day: sub.due_day, 
    category_id: sub.category_id?._id || ''
  };
  editId.value = sub._id;
  isEditing.value = true;
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
};

const submitSubscription = async () => {
  saving.value = true;
  try {
    const payload = {
      name: form.value.name,
      amount: parseFloat(form.value.amount),
      due_day: parseInt(form.value.due_day),
      category_id: form.value.category_id
    };

    if (isEditing.value) {
      await api.put(`/subscriptions/${editId.value}`, payload);
      toast.success("Atualizado!");
    } else {
      await api.post('/subscriptions/', payload);
      toast.success("Criado!");
    }
    
    fetchData();
    closeModal();
  } catch (err) {
    toast.error("Erro ao salvar.");
  } finally {
    saving.value = false;
  }
};

const deleteSubscription = async (id) => {
  const result = await Swal.fire({
    title: 'Excluir Fixo?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    background: '#1f2937',
    color: '#fff'
  });

  if (result.isConfirmed) {
    try {
      await api.delete(`/subscriptions/${id}`);
      toast.success("Removido!");
      fetchData();
    } catch (err) {
      toast.error("Erro ao excluir.");
    }
  }
};

const paySubscription = async (sub) => {
  const options = wallets.value.reduce((acc, w) => {
    acc[w._id] = `${w.name} (R$ ${w.balance.toFixed(2)})`;
    return acc;
  }, {});

  const { value: walletId } = await Swal.fire({
    title: 'Pagar Assinatura',
    text: `Qual carteira utilizar para o pagamento de ${sub.name}?`,
    input: 'select',
    inputOptions: options,
    inputPlaceholder: 'Selecione a carteira',
    showCancelButton: true,
    confirmButtonColor: '#2563eb',
    background: '#1f2937',
    color: '#fff',
    inputValidator: (value) => {
      if (!value) return 'Selecione uma carteira para prosseguir!';
    }
  });

  if (walletId) {
    try {
      await api.post(`/subscriptions/${sub._id}/pay?wallet_id=${walletId}`);
      toast.success("Pagamento registrado!");
      refreshTrigger.value++;
      fetchData();
    } catch (err) {
      toast.error("Falha ao processar pagamento.");
    }
  }
};

onMounted(fetchData);
</script>