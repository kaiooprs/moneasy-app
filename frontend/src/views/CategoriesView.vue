<template>
  <div class="min-h-screen bg-gray-900 text-white pt-5 pb-24 px-4 relative">
    
    <div class="mb-6 flex justify-between items-end">
      <div>
        <button @click="$router.push('/profile')" class="text-gray-400 hover:text-white mb-2 flex items-center gap-1 text-sm transition-colors">
          <ArrowLeft :size="16" /> Voltar
        </button>
        <h1 class="text-2xl font-bold">Categorias</h1>
        <p class="text-gray-400 text-xs">Organize seus lançamentos</p>
      </div>
      <button 
        @click="openCreateModal" 
        class="bg-blue-600 hover:bg-blue-500 text-white p-2 px-4 rounded-xl shadow-lg shadow-blue-900/20 flex items-center gap-2 text-sm font-bold transition-transform active:scale-95"
      >
        <Plus :size="18" /> Nova
      </button>
    </div>

    <div v-if="loading" class="flex justify-center py-10 opacity-50">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
    </div>

    <div class="space-y-3">
      <div v-for="c in categories" :key="c._id" 
        class="bg-gray-800 p-4 rounded-2xl border border-gray-700/50 flex items-center justify-between shadow-sm">
        
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 rounded-xl flex items-center justify-center text-2xl shadow-sm"
              :style="{ backgroundColor: (c.color || '#4CAF50') + '33', border: '1px solid ' + (c.color || '#4CAF50') }">
            {{ c.icon || '💰' }}
          </div>
          <div>
            <h3 class="font-bold text-white">{{ c.name }}</h3>
          </div>
        </div>
        
        <div class="flex gap-2">
          <button @click="openEditModal(c)" class="text-gray-400 hover:text-blue-400 transition-colors p-2 bg-gray-900 rounded-lg">
            <Pencil :size="16" />
          </button>
          <button @click="deleteCategory(c._id, c.name)" class="text-gray-400 hover:text-red-400 transition-colors p-2 bg-gray-900 rounded-lg">
            <Trash2 :size="16" />
          </button>
        </div>
      </div>

      <div v-if="!loading && categories.length === 0" class="text-center py-12 text-gray-500 bg-gray-800/50 rounded-2xl border border-dashed border-gray-700">
        <p>Nenhuma categoria criada.</p>
      </div>
    </div>

    <div v-if="isModalOpen" class="fixed inset-0 z-[100] flex items-end sm:items-center justify-center px-4 py-6">
      <div class="absolute inset-0 bg-black/80 backdrop-blur-sm transition-opacity" @click="closeModal"></div>

      <div class="bg-gray-800 w-full max-w-md rounded-3xl p-6 relative shadow-2xl border border-gray-700 transform transition-all animate-slide-up mb-6 sm:mb-0">
        
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-xl font-bold text-white">{{ isEditing ? 'Editar Categoria' : 'Nova Categoria' }}</h2>
          <button @click="closeModal" class="bg-gray-700 p-2 rounded-full text-gray-400 hover:text-white">
            <X :size="20" />
          </button>
        </div>

        <form @submit.prevent="submitCategory" class="space-y-5">
          
          <div>
            <label class="block text-xs text-gray-400 uppercase font-bold mb-1">Nome</label>
            <input v-model="form.name" type="text" placeholder="Ex: Alimentação, Transporte..." required
              class="w-full bg-gray-900 border border-gray-700 rounded-xl px-4 py-3 text-white focus:ring-2 focus:ring-blue-500 outline-none" />
          </div>

          <div>
            <label class="block text-xs text-gray-400 uppercase font-bold mb-1">Cor</label>
            <div class="flex gap-2 pt-1 flex-wrap">
              <button type="button" v-for="color in presetColors" :key="color" 
                @click="form.color = color"
                class="w-8 h-8 rounded-full border-2 transition-transform"
                :class="form.color === color ? 'border-white scale-110' : 'border-transparent hover:scale-105'"
                :style="{ backgroundColor: color }">
              </button>
            </div>
          </div>

          <div>
            <label class="block text-xs text-gray-400 uppercase font-bold mb-2">Escolha um Ícone</label>
            <div class="grid grid-cols-5 gap-2 bg-gray-900 p-3 rounded-xl border border-gray-700 max-h-48 overflow-y-auto">
              <button type="button" v-for="icon in preseticons" :key="icon" 
                @click="form.icon = icon"
                class="text-2xl w-full aspect-square flex items-center justify-center rounded-lg transition-all"
                :class="form.icon === icon ? 'bg-blue-500/20 border-2 border-blue-500 scale-110' : 'bg-gray-800 border-2 border-transparent hover:bg-gray-700'">
                {{ icon }}
              </button>
            </div>
          </div>

          <button type="submit" :disabled="saving"
            class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-4 rounded-xl shadow-lg mt-2 flex justify-center items-center">
            <span v-if="saving" class="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></span>
            <span v-else>{{ isEditing ? 'Salvar Alterações' : 'Criar Categoria' }}</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'; 
import { Plus, Pencil, Trash2, X, ArrowLeft } from 'lucide-vue-next';
import { useToast } from "vue-toastification";
import Swal from 'sweetalert2';
import api from '../api';
import { refreshTrigger } from '../store'; 

const toast = useToast();
const categories = ref([]);
const loading = ref(true);
const saving = ref(false);

const isModalOpen = ref(false);
const isEditing = ref(false);
const editId = ref(null);

const preseticons = [
  '🍛', '🛒', '🚗', '🚌', '🏠', '💡', '💧', '📱', 
  '🎮', '🎬', '💊', '👕', '✈️', '🐶', '🎓', '🏋️',
  '💼', '💰', '🎁', '🔧', '💇', '👶', '📚', '📌'
];

const presetColors = ['#8b5cf6', '#f97316', '#22c55e', '#eab308', '#3b82f6', '#ef4444', '#ec4899', '#14b8a6']; 

const form = ref({
  name: '',
  icon: '📌',
  color: '#8b5cf6'
});

const fetchCategories = async () => {
  loading.value = true;
  try {
    const { data } = await api.get('/categories/');
    categories.value = data;
  } catch (err) {
    toast.error("Erro ao carregar categorias.");
  } finally {
    loading.value = false;
  }
};

const openCreateModal = () => {
  form.value = { name: '', icon: '🍛', color: '#8b5cf6' };
  isEditing.value = false;
  isModalOpen.value = true;
};

const openEditModal = (category) => {
  form.value = { 
    name: category.name, 
    icon: category.icon || '📌',
    color: category.color || '#8b5cf6'
  };
  editId.value = category._id;
  isEditing.value = true;
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
};

const submitCategory = async () => {
  saving.value = true;
  try {
    const payload = {
      name: form.value.name,
      icon: form.value.icon,
      color: form.value.color
    };

    if (isEditing.value) {
      await api.put(`/categories/${editId.value}`, payload);
      toast.success("Categoria atualizada!");
    } else {
      await api.post('/categories/', payload);
      toast.success("Categoria criada com sucesso!");
    }

    refreshTrigger.value++;
    
    fetchCategories();
    closeModal();
  } catch (err) {
    toast.error("Erro ao salvar.");
  } finally {
    saving.value = false;
  }
};

const deleteCategory = async (id, name) => {
  const result = await Swal.fire({
    title: 'Excluir categoria?',
    text: `Quer mesmo excluir a categoria "${name}"?`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#374151',
    confirmButtonText: 'Sim, excluir!',
    background: '#1f2937',
    color: '#fff'
  });

  if (result.isConfirmed) {
    try {
      await api.delete(`/categories/${id}`);
      toast.success("Categoria excluída!");
      
      refreshTrigger.value++;
      
      fetchCategories();
    } catch (err) {
      toast.error("Erro ao excluir.");
    }
  }
};

watch(refreshTrigger, () => {
  fetchCategories();
});

onMounted(fetchCategories);
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