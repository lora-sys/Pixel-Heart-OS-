<script lang="ts">
  import '../app.css';
  import Navigation from '$lib/components/Navigation.svelte';
  import { setContext } from 'svelte';
  import { uiStore, apiStore } from '$lib/core/store';

  // Pass stores to children via context for easy access
  setContext('uiStore', uiStore);
  setContext('apiStore', apiStore);
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
