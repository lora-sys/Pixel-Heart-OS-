<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { api } from '$lib/api/client';
  import * as store from '$lib/core/store/api-store';

  let heroine: any = null;
  let npcs: any[] = [];
  let scenes: any[] = [];

  onMount(async () => {
    store.heroine.subscribe(v => heroine = v);
    store.npcs.subscribe(v => npcs = v || []);
    store.scenes.subscribe(v => scenes = v || []);
  });

  async function generateScene() {
    try {
      const scene = await api.generateScene('Mysterious Forest');
      store.addScene(scene);
    } catch (e) {
      console.error(e);
    }
  }
</script>

<div class="p-6">
  <div class="flex justify-between items-center mb-6">
    <h1 class="text-2xl font-bold text-white">Universe</h1>
    <div class="flex gap-2">
      <button on:click={() => goto('/simulate')} class="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded">
        Simulate
      </button>
      <button on:click={() => goto('/timeline')} class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded">
        Timeline
      </button>
    </div>
  </div>

  {#if heroine}
    <div class="bg-gray-800 rounded-lg p-4 mb-6">
      <h2 class="text-xl font-bold text-pink-400 mb-2">{heroine.identity?.name || 'Heroine'}</h2>
      <p class="text-gray-300">{heroine.soul?.archetype} - {heroine.identity?.role}</p>
      <p class="text-gray-400 text-sm mt-2">{heroine.soul?.description}</p>
    </div>
  {/if}

  <div class="mb-6">
    <div class="flex justify-between items-center mb-3">
      <h2 class="text-xl font-bold text-white">NPCs</h2>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      {#each npcs as npc}
        <div class="bg-gray-800 rounded-lg p-4">
          <h3 class="font-bold text-pink-400">{npc.name}</h3>
          <p class="text-gray-400 text-sm">{npc.archetype}</p>
          <p class="text-gray-500 text-xs">{npc.role}</p>
        </div>
      {:else}
        <p class="text-gray-500">No NPCs yet</p>
      {/each}
    </div>
  </div>

  <div>
    <div class="flex justify-between items-center mb-3">
      <h2 class="text-xl font-bold text-white">Scenes</h2>
      <button on:click={generateScene} class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded text-sm">
        Generate Scene
      </button>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      {#each scenes as scene}
        <div class="bg-gray-800 rounded-lg p-4">
          <h3 class="font-bold text-green-400">{scene.title}</h3>
          <p class="text-gray-400 text-sm">{scene.location}</p>
          <p class="text-gray-500 text-xs">{scene.description}</p>
        </div>
      {:else}
        <p class="text-gray-500">No scenes yet</p>
      {/each}
    </div>
  </div>
</div>
