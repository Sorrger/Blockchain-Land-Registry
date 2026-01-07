import { reactive } from 'vue';

export const store = reactive({
  role: localStorage.getItem('user_role') || ''
});

export function setRole(role: string) {
  store.role = role;
  localStorage.setItem('user_role', role);
}

export function logout() {
  store.role = '';
  localStorage.removeItem('user_role');
  window.location.href = '/';
}