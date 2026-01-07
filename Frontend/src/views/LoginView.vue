<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { setRole } from '@/store'; 

// Make sure this address matches your MetaMask account exactly (lowercase)
const NOTARY_ADDRESS = "0x70997970c51812dc3a010c7d01b50e0d17dc79c8";

const router = useRouter();
const errorMsg = ref('');
const isConnecting = ref(false);

const loginAsUser = () => {
  setRole('user'); 
  router.push('/my-properties');
};

const loginWithMetaMask = async () => {
  errorMsg.value = '';
  isConnecting.value = true;
  
  if (!(window as any).ethereum) {
    errorMsg.value = 'MetaMask is not installed!';
    isConnecting.value = false;
    return;
  }
  
  try {
    const accounts = await (window as any).ethereum.request({ method: 'eth_requestAccounts' });
    const connectedAccount = accounts[0].toLowerCase();
    
    if (connectedAccount === NOTARY_ADDRESS) {
      setRole('notary');
      router.push('/properties');
    } else {
      errorMsg.value = 'Access Denied: Wallet is not authorized as Notary.';
    }
  } catch (err: any) {
    errorMsg.value = 'Connection failed: ' + err.message;
  } finally {
    isConnecting.value = false;
  }
};
</script>

<template>
  <div class="login-wrapper">
    <div class="header-section">
      <h1 class="gradient-text">Blockchain Land Registry</h1>
      <p class="subtitle">Secure, Transparent, Immutable Property Management</p>
    </div>
    
    <div class="cards-container">
      <div class="glass-card notary-card" @click="loginWithMetaMask">
        <div class="icon-circle">🦊</div>
        <h2>Notary Access</h2>
        <p v-if="!isConnecting">Connect MetaMask to verify official authority.</p>
        <p v-else class="pulsing">Connecting to Wallet...</p>
      </div>
      
      <div class="glass-card user-card" @click="loginAsUser">
        <div class="icon-circle">👤</div>
        <h2>Public Portal</h2>
        <p>View properties and check ownership history.</p>
      </div>
    </div>

    <div v-if="errorMsg" class="error-toast">
      ⚠️ {{ errorMsg }}
    </div>
  </div>
</template>

<style scoped>
.login-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 80vh;
  text-align: center;
}

.gradient-text {
  font-size: 3.5rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -1px;
}

.subtitle {
  color: #94a3b8;
  font-size: 1.1rem;
  margin-bottom: 3rem;
}

.cards-container {
  display: flex;
  gap: 30px;
  flex-wrap: wrap;
  justify-content: center;
}

.glass-card {
  width: 280px;
  padding: 40px 30px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
}

.glass-card:hover {
  transform: translateY(-8px);
  background: rgba(30, 41, 59, 0.9);
  border-color: rgba(255, 255, 255, 0.2);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
}

.icon-circle {
  font-size: 3rem;
  margin-bottom: 20px;
  background: rgba(255,255,255,0.05);
  width: 80px;
  height: 80px;
  line-height: 80px;
  border-radius: 50%;
  margin-left: auto;
  margin-right: auto;
}

.notary-card:hover { border-color: #f97316; box-shadow: 0 0 20px rgba(249, 115, 22, 0.2); }
.user-card:hover { border-color: #10b981; box-shadow: 0 0 20px rgba(16, 185, 129, 0.2); }

h2 { color: #f8fafc; margin-bottom: 10px; font-size: 1.5rem; }
p { color: #94a3b8; font-size: 0.95rem; line-height: 1.5; }

.error-toast {
  margin-top: 30px;
  padding: 12px 24px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #fca5a5;
  border-radius: 8px;
  animation: slideUp 0.3s ease;
}

.pulsing { animation: pulse 1.5s infinite; color: #fbbf24; }
@keyframes slideUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
@keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
</style>