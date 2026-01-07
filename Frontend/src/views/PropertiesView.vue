<script setup lang="ts">
import { ref, onMounted } from 'vue';
import CreatePropertyForm from '@/components/forms/CreatePropertyForm.vue';
import { getProperties, type Property } from '@/api/properties';

const properties = ref<Property[]>([]);
const isNotary = ref(false);

const loadProperties = async () => {
  properties.value = await getProperties();
};

onMounted(() => {
  isNotary.value = localStorage.getItem('user_role') === 'notary';
  loadProperties();
});
</script>

<template>
  <div class="view-container">
    <header class="page-header">
      <h1 class="gradient-title">Properties Registry</h1>
      <p class="subtitle">Manage and view decentralized land titles</p>
    </header>
    
    <div class="content-grid">
      <div v-if="isNotary" class="sidebar">
        <div class="glass-panel form-panel">
          <CreatePropertyForm @property-created="loadProperties" /> 
        </div>
      </div>

      <div class="list-section" :class="{ 'full-width': !isNotary }">
        <div class="section-header">
          <h3>Registry Records ({{ properties.length }})</h3>
          <button @click="loadProperties" class="refresh-btn">🔄 Refresh</button>
        </div>

        <ul v-if="properties.length" class="property-list">
          <li v-for="prop in properties" :key="prop.id" class="glass-card property-item">
            <div class="prop-header">
              <span class="kw-number">{{ prop.property_number }}</span>
              <span class="status-badge" :class="prop.is_onchain ? 'on-chain' : 'pending'">
                {{ prop.is_onchain ? '✅ On-Chain' : '⏳ Pending' }}
              </span>
            </div>
            
            <div class="prop-details">
              <div class="detail-row">
                <span class="label">Address:</span>
                <span class="value">{{ prop.address }}</span>
              </div>
              <div class="detail-row">
                <span class="label">Area:</span>
                <span class="value">{{ prop.area }} m²</span>
              </div>
            </div>
          </li>
        </ul>
        
        <div v-else class="empty-state">
          No properties found in the registry.
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* PAGE LAYOUT */
.view-container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.gradient-title {
  font-size: 3rem;
  margin: 0;
  background: linear-gradient(to right, #60a5fa, #c084fc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 800;
}

.subtitle {
  color: #94a3b8;
  margin-top: 10px;
  font-size: 1.1rem;
}

/* GRID SYSTEM */
.content-grid {
  display: flex;
  gap: 30px;
  align-items: flex-start;
}

.sidebar {
  flex: 0 0 350px; /* Fixed width for form */
}

.list-section {
  flex: 1;
}

.list-section.full-width {
  flex: 100%;
}

/* GLASSMORPHISM PANELS */
.glass-panel, .glass-card {
  background: rgba(30, 41, 59, 0.7); /* Dark semi-transparent blue */
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
}

.form-panel {
  padding: 25px;
  border-top: 4px solid #4f46e5; /* Accent line for form */
}

/* LIST STYLING */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h3 {
  color: #e2e8f0;
  font-size: 1.3rem;
  margin: 0;
}

.refresh-btn {
  background: transparent;
  border: 1px solid #475569;
  color: #94a3b8;
  padding: 5px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}
.refresh-btn:hover { background: rgba(255,255,255,0.05); color: white; }

.property-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); /* Responsive Grid */
  gap: 20px;
}

.property-item {
  padding: 20px;
  transition: transform 0.2s;
}

.property-item:hover {
  transform: translateY(-4px);
  background: rgba(30, 41, 59, 0.9);
  border-color: rgba(255, 255, 255, 0.2);
}

/* ITEM DETAILS */
.prop-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.kw-number {
  color: #fff;
  font-weight: 700;
  font-size: 1.1rem;
}

.status-badge {
  font-size: 0.75rem;
  padding: 4px 8px;
  border-radius: 20px;
  font-weight: bold;
  text-transform: uppercase;
}

.on-chain { background: rgba(16, 185, 129, 0.2); color: #4ade80; border: 1px solid rgba(16, 185, 129, 0.4); }
.pending { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }

.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 0.95rem;
}

.label { color: #94a3b8; }
.value { color: #e2e8f0; text-align: right; }

.empty-state {
  text-align: center;
  padding: 40px;
  color: #64748b;
  background: rgba(255,255,255,0.02);
  border-radius: 12px;
  border: 2px dashed #334155;
}

/* Responsive adjust for mobile */
@media (max-width: 768px) {
  .content-grid { flex-direction: column; }
  .sidebar { width: 100%; }
}
</style>