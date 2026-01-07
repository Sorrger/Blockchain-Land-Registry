<script setup lang="ts">
import { store, logout } from '@/store';
</script>

<template>
  <div class="app-container">
    <nav v-if="store.role" class="navbar">
      <div class="nav-left">
        <span class="role-badge" :class="store.role">
          {{ store.role === 'notary' ? '👨‍⚖️ NOTARY ACCESS' : '👤 PUBLIC USER' }}
        </span>
        
        <div class="nav-links">
          <template v-if="store.role === 'notary'">
            <router-link to="/users">Manage Users</router-link>
            <router-link to="/properties">Registry</router-link>
            <router-link to="/transfer">Transfer Ownership</router-link>
          </template>

          <template v-if="store.role === 'user'">
            <router-link to="/my-properties">Browse Properties</router-link>
          </template>
        </div>
      </div>
      
      <button @click="logout" class="logout-btn">
        Disconnect
      </button>
    </nav>
    
    <main>
      <router-view />
    </main>
  </div>
</template>

<style>
/* GLOBAL DARK THEME */
body {
  margin: 0;
  background-color: #0f172a; /* Deep Navy Background */
  color: #f1f5f9; /* Light Text */
  font-family: 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
}

.app-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 20px;
}

/* NAVBAR STYLING */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: rgba(30, 41, 59, 0.8); /* Glass effect */
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  margin-bottom: 40px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 25px;
}

/* Role Badges */
.role-badge {
  font-size: 0.7rem;
  font-weight: 800;
  letter-spacing: 0.05em;
  padding: 6px 12px;
  border-radius: 6px;
  text-transform: uppercase;
  border: 1px solid transparent;
}

.role-badge.notary { 
  background: rgba(79, 70, 229, 0.15); 
  color: #818cf8; 
  border-color: rgba(79, 70, 229, 0.3);
}

.role-badge.user { 
  background: rgba(16, 185, 129, 0.15); 
  color: #34d399; 
  border-color: rgba(16, 185, 129, 0.3);
}

/* Links */
.nav-links a {
  color: #94a3b8;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  transition: all 0.2s;
  padding: 8px 12px;
  border-radius: 6px;
}

.nav-links a:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.05);
}

.nav-links a.router-link-active {
  color: #fff;
  background: rgba(255, 255, 255, 0.1);
}

/* Logout Button */
.logout-btn {
  background: transparent;
  border: 1px solid #ef4444;
  color: #ef4444;
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: #ef4444;
  color: white;
  box-shadow: 0 0 15px rgba(239, 68, 68, 0.4);
}
</style>