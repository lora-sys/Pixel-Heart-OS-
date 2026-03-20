<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { api } from '$lib/api/client';
  import * as store from '$lib/core/store/api-store';
  import NPCCard from '$lib/components/NPCCard.svelte';
  import SceneCard from '$lib/components/SceneCard.svelte';

  let heroine = $state<any>(null);
  let npcs = $state<any[]>([]);
  let scenes = $state<any[]>([]);
  let loading = $state(false);
  let selectedNPC = $state<any>(null);

  onMount(async () => {
    store.heroine.subscribe(v => heroine = v);
    store.npcs.subscribe(v => npcs = v || []);
    store.scenes.subscribe(v => scenes = v || []);
  });

  async function generateScene() {
    loading = true;
    try {
      const scene = await api.generateScene('Mysterious Forest');
      store.addScene(scene);
    } catch (e) {
      console.error(e);
    } finally {
      loading = false;
    }
  }

  function selectNPC(npc: any) {
    selectedNPC = npc;
  }
</script>

<div class="p-6">
  <div class="flex justify-between items-center mb-6">
    <h1 class="text-2xl font-bold text-white">Universe</h1>
    <div class="flex gap-2">
      <button onclick={() => goto('/simulate')} class="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded">
        Simulate
      </button>
      <button onclick={() => goto('/timeline')} class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded">
        Timeline
      </button>
    </div>
  </div>

  {#if heroine}
    <div class="bg-gray-800 rounded-lg p-6 mb-6">
      <h2 class="text-2xl font-bold text-pink-400 mb-2">{heroine.identity?.name || 'Heroine'}</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <p class="text-gray-400 text-sm">Archetype</p>
          <p class="text-white">{heroine.soul?.archetype || 'Unknown'}</p>
        </div>
        <div>
          <p class="text-gray-400 text-sm">Role</p>
          <p class="text-white">{heroine.identity?.role || 'Unknown'}</p>
        </div>
        <div>
          <p class="text-gray-400 text-sm">Description</p>
          <p class="text-gray-300 text-sm">{heroine.soul?.description || 'No description'}</p>
        </div>
      </div>
    </div>
  {/if}

  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <div>
      <div class="flex justify-between items-center mb-3">
        <h2 class="text-xl font-bold text-white">NPCs</h2>
      </div>
      <div class="space-y-3">
        {#each npcs as npc}
          <NPCCard 
            npc={npc} 
            onclick={() => selectNPC(npc)}
          />
        {:else}
          <p class="text-gray-500">No NPCs yet</p>
        {/each}
      </div>
    </div>

    <div>
      <div class="flex justify-between items-center mb-3">
        <h2 class="text-xl font-bold text-white">Scenes</h2>
        <button onclick={generateScene} class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded text-sm" disabled={loading}>
          {loading ? 'Generating...' : 'Generate Scene'}
        </button>
      </div>
      <div class="space-y-3">
        {#each scenes as scene}
          <SceneCard scene={scene} />
        {:else}
          <p class="text-gray-500">No scenes yet. Generate one to get started!</p>
        {/each}
      </div>
    </div>
  </div>

  {#if selectedNPC}
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-bold text-pink-400">{selectedNPC.name}</h3>
          <button onclick={() => selectedNPC = null} class="text-gray-400 hover:text-white">
            ✕
          </button>
        </div>
        <div class="space-y-3">
          <div>
            <p class="text-gray-400 text-sm">Archetype</p>
            <p class="text-white">{selectedNPC.archetype}</p>
          </div>
          <div>
            <p class="text-gray-400 text-sm">Role</p>
            <p class="text-white">{selectedNPC.role}</p>
          </div>
          <div>
            <p class="text-gray-400 text-sm">Relationship</p>
            <p class="text-white">{selectedNPC.relationship}</p>
          </div>
        </div>
        <button onclick={() => { selectedNPC = null; goto('/simulate'); }} class="mt-4 w-full bg-pink-600 hover:bg-pink-700 text-white py-2 rounded">
          Start Simulation
        </button>
      </div>
    </div>
  {/if}
</div>
