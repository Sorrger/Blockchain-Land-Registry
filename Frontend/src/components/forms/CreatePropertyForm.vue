<script setup lang="ts">
import { ref } from 'vue';
import { createProperty } from '@/api/properties';

const emit = defineEmits(['property-created']);

const form = ref({
  property_number: '',
  address: '',
  area: null as number | null 
});

const message = ref('');
const isSubmitting = ref(false);

const submit = async () => {
  if (isSubmitting.value) return;
  isSubmitting.value = true;
  message.value = '';
  
  try {
    await createProperty({
      ...form.value,
      area: Number(form.value.area)
    });
    message.value = '✅ Property successfully registered!';
    form.value = { property_number: '', address: '', area: null };
    emit('property-created');
    
    // Clear success message after 3 seconds
    setTimeout(() => message.value = '', 3000);
    
  } catch (e: any) {
    message.value = '❌ Error: ' + (e.response?.data?.detail || e.message);
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<template>
  <div class="form-wrapper">
    <h3>Add New Property</h3>
    <p class="form-desc">Register a new land title to the database.</p>
    
    <form @submit.prevent="submit">
      <div class="input-group">
        <label>KW Number</label>
        <input v-model="form.property_number" placeholder="e.g. WA1M/001" required />
      </div>

      <div class="input-group">
        <label>Address</label>
        <input v-model="form.address" placeholder="e.g. 123 Blockchain Blvd" required />
      </div>

      <div class="input-group">
        <label>Area (m²)</label>
        <input v-model.number="form.area" type="number" step="0.01" placeholder="0.00" required />
      </div>

      <button type="submit" :disabled="isSubmitting">
        {{ isSubmitting ? 'Registering...' : 'Create Registry Record' }}
      </button>
    </form>
    
    <p v-if="message" class="status-msg" :class="{ error: message.includes('Error') }">
      {{ message }}
    </p>
  </div>
</template>

<style scoped>
.form-wrapper {
  width: 100%;
}

h3 {
  margin: 0 0 5px 0;
  color: #f1f5f9;
  font-size: 1.25rem;
}

.form-desc {
  margin-bottom: 20px;
  color: #94a3b8;
  font-size: 0.9rem;
}

.input-group {
  margin-bottom: 15px;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 6px;
  color: #cbd5e1;
  font-size: 0.85rem;
  font-weight: 600;
}

input {
  width: 100%;
  padding: 12px;
  background: rgba(15, 23, 42, 0.6); /* Darker background for inputs */
  border: 1px solid #334155;
  border-radius: 8px;
  color: #fff;
  font-size: 1rem;
  transition: border-color 0.2s;
  box-sizing: border-box; /* Fix padding issues */
}

input:focus {
  outline: none;
  border-color: #60a5fa; /* Blue focus */
  box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.2);
}

button {
  width: 100%;
  padding: 12px;
  margin-top: 10px;
  background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.1s, opacity 0.2s;
}

button:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

button:disabled {
  background: #475569;
  cursor: not-allowed;
  transform: none;
}

.status-msg {
  margin-top: 15px;
  font-size: 0.9rem;
  color: #4ade80; /* Green success */
  text-align: center;
}

.status-msg.error {
  color: #f87171; /* Red error */
}
</style>