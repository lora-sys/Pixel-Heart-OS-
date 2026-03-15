<script lang="ts">
  import { state } from '$lib/stores/app-store';
  import { goto } from '$app/navigation';

  $effect(() => {
    if ($state.heroine) {
      goto('/universe');
    } else {
      goto('/create');
    }
  });
</script>

<div class="flex items-center justify-center min-h-screen">
  <div class="text-center">
    <h1 class="text-accent-2 font-pixel text-2xl mb-4 animate-pulse">Pixel Heart OS</h1>
    <p class="text-text-dim">Initializing...</p>
  </div>
</div>
