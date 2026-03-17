<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { api } from '$lib/api/client';
  import * as store from '$lib/core/store/api-store';
  import * as appStore from '$lib/core/store/app-store';

  let description = '';
  let loading = false;
  let errorMsg = '';

  onMount(async () => {
    try {
      const heroine = await api.getHeroine();
      if (heroine) {
        store.setHeroine(heroine);
        const npcs = await api.getNPCs();
        store.setNPCs(npcs);
        goto('/universe');
      }
    } catch (e) {
      console.log('No heroine yet');
    }
  });

  async function createHeroine() {
    if (!description.trim()) {
      errorMsg = 'Please enter a description';
      return;
    }
    loading = true;
    errorMsg = '';
    try {
      const heroine = await api.createHeroine(description);
      store.setHeroine(heroine);
      const npcs = await api.generateNPCs(3);
      store.setNPCs(npcs);
      goto('/universe');
    } catch (e) {
      errorMsg = 'Failed to create heroine';
    } finally {
      loading = false;
    }
  }
</script>

<div class="min-h-screen bg-gray-900 flex items-center justify-center p-4">
  <div class="max-w-lg w-full bg-gray-800 rounded-lg p-8 shadow-xl">
    <h1 class="text-3xl font-bold text-white mb-2">Pixel Heart OS</h1>
    <p class="text-gray-400 mb-6">Create your heroine from a natural language description</p>
    
    <form on:submit|preventDefault={createHeroine}>
      <textarea
        bind:value={description}
        placeholder="Describe your heroine... (e.g., 'A brave young woman with a mysterious past who seeks to protect her village')"
        class="w-full h-40 bg-gray-700 text-white rounded-lg p-4 mb-4 resize-none focus:outline-none focus:ring-2 focus:ring-pink-500"
        disabled={loading}
      ></textarea>
      
      {#if errorMsg}
        <p class="text-red-400 mb-4">{errorMsg}</p>
      {/if}
      
      <button
        type="submit"
        disabled={loading}
        class="w-full bg-pink-600 hover:bg-pink-700 text-white font-bold py-3 rounded-lg transition disabled:opacity-50"
      >
        {loading ? 'Creating...' : 'Create Heroine'}
      </button>
    </form>
    
    <div class="mt-6 text-center">
      <p class="text-gray-500 text-sm">
        Your heroine will be generated with unique soul, identity, and voice
      </p>
    </div>
  </div>
</div>
