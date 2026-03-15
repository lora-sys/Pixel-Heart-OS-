<script lang="ts">
  import { goto } from '$app/navigation';
  import { apiStore } from '$lib/core/store';

  $effect(() => {
    const unsubscribe = apiStore.subscribe(state => {
      if (state.heroine) {
        goto('/universe');
      } else {
        goto('/create');
      }
    });
    return () => unsubscribe();
  });
</script>

<div class="flex items-center justify-center min-h-screen">
  <div class="text-center">
    <h1 class="text-accent-2 font-pixel text-2xl mb-4 animate-pulse">Pixel Heart OS</h1>
    <p class="text-text-dim">Initializing...</p>
  </div>
</div>
