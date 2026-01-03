<template>
  <div>
    <nav>
      <router-link to="/users">Users</router-link> |
      <router-link to="/properties">Properties</router-link> |
      <router-link to="/transfer">Transfer</router-link>
    </nav>

    <router-view />
  </div>
</template>
