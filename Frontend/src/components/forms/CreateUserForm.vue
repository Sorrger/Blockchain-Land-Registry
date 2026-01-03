<script setup lang="ts">
import { ref } from "vue";
import { createUser } from "@/api/users";

const form = ref({
  first_name: "",
  last_name: "",
  email: "",
  pesel: "",
  wallet_address: "",
});

const loading = ref(false);
const error = ref<string | null>(null);
const success = ref(false);

const submit = async () => {
  error.value = null;
  success.value = false;

  try {
    loading.value = true;
    await createUser(form.value);
    success.value = true;

    // reset form
    form.value = {
      first_name: "",
      last_name: "",
      email: "",
      pesel: "",
      wallet_address: "",
    };
  } catch (e: any) {
    error.value = e?.response?.data?.detail ?? "Error creating user";
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <form @submit.prevent="submit" class="form">
    <h2>Create User</h2>

    <input v-model="form.first_name" placeholder="First name" required />
    <input v-model="form.last_name" placeholder="Last name" required />
    <input v-model="form.email" placeholder="Email (optional)" />
    <input v-model="form.pesel" placeholder="PESEL" required />
    <input
      v-model="form.wallet_address"
      placeholder="Wallet address"
      required
    />

    <button type="submit" :disabled="loading">
      {{ loading ? "Creating..." : "Create User" }}
    </button>

    <p v-if="error" style="color: red">{{ error }}</p>
    <p v-if="success" style="color: green">User created successfully</p>
  </form>
</template>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 400px;
}
input {
  padding: 8px;
}
button {
  padding: 8px;
}
</style>
