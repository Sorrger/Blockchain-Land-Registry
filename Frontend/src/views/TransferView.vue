<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getProperties, type Property } from '@/api/properties';
import { getUsers, type User } from '@/api/users';
import { createOwnership } from '@/api/ownerships';

const properties = ref<Property[]>([]);
const users = ref<User[]>([]);

const selectedPropertyId = ref('');
const selectedWallet = ref('');
const status = ref('');
const txHash = ref('');

onMounted(async () => {
  properties.value = await getProperties();
  users.value = await getUsers();
});

const handleTransfer = async () => {
  if (!selectedPropertyId.value || !selectedWallet.value) return;
  
  status.value = 'Processing Transaction on Blockchain... (Please wait)';
  txHash.value = '';

  try {
    const response = await createOwnership({
      property_id: selectedPropertyId.value,
      owner_wallet: selectedWallet.value
    });
    
    status.value = 'Success! Ownership Transferred.';
    txHash.value = response.tx_hash;
  } catch (e: any) {
    status.value = 'Error: ' + (e.response?.data?.detail || e.message);
  }
};
</script>

<template>
  <div class="transfer-container">
    <h1>Transfer Ownership (Blockchain)</h1>
    
    <div class="form-group">
      <label>1. Select Property:</label>
      <select v-model="selectedPropertyId">
        <option disabled value="">Select a property</option>
        <option v-for="prop in properties" :key="prop.id" :value="prop.id">
          {{ prop.property_number }} - {{ prop.address }}
        </option>
      </select>
    </div>

    <div class="form-group">
      <label>2. Select New Owner (Wallet):</label>
      <select v-model="selectedWallet">
        <option disabled value="">Select a user</option>
        <option v-for="user in users" :key="user.id" :value="user.wallet_address">
          {{ user.first_name }} {{ user.last_name }} ({{ user.wallet_address.substring(0, 8) }}...)
        </option>
      </select>
    </div>

    <button @click="handleTransfer" :disabled="!selectedPropertyId || !selectedWallet">
      Execute On-Chain Transfer
    </button>

    <div v-if="status" class="status-box">
      <p>{{ status }}</p>
      <p v-if="txHash" class="hash">TX Hash: {{ txHash }}</p>
    </div>
  </div>
</template>

<style scoped>
.transfer-container { max-width: 500px; }
.form-group { margin-bottom: 15px; display: flex; flex-direction: column; }
select { padding: 10px; margin-top: 5px; }
button { padding: 15px; background-color: #3b82f6; color: white; border: none; font-weight: bold; cursor: pointer; margin-top: 10px; }
button:disabled { background-color: #ccc; }
.status-box { margin-top: 20px; padding: 15px; background: #f3f4f6; border-radius: 5px; }
.hash { font-family: monospace; word-break: break-all; color: #d97706; }
</style>