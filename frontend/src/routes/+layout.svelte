<script lang="ts">
  import '../app.css';
  import Navigation from '$lib/components/Navigation.svelte';
  import { setContext } from 'svelte';
  import { writable } from 'svelte/store';

  // Global app state store (Svelte 5 Runes style)
  import { state } from '$lib/stores/app-store';

  // Pass state to children via context
  setContext('appState', state);
</script>

<div class="min-h-screen bg-bg-dark text-text-main font-mono">
  <Navigation />
  <main class="container mx-auto px-4 py-8">
    <slot />
  </main>
  <footer class="text-center py-4 text-text-dim text-sm">
    Pixel Heart OS v0.1.0
  </footer>
</div>
