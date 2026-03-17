<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { api } from '$lib/api/client';
  import * as store from '$lib/core/store/api-store';

  let beads: any[] = [];
  let selectedBead: any = null;
  let diffResult: any = null;

  onMount(async () => {
    try {
      const result = await api.getBeads();
      beads = result || [];
    } catch (e) {
      console.error('Failed to load beads:', e);
    }
  });

  function selectBead(bead: any) {
    selectedBead = bead;
  }

  async function loadMore() {
    const result = await api.getBeads('main', beads.length + 50);
    beads = result || [];
  }
</script>

<div class="p-6">
  <div class="flex justify-between items-center mb-6">
    <h1 class="text-2xl font-bold text-white">Timeline</h1>
    <div class="flex gap-2">
      <button on:click={() => goto('/universe')} class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded">
        Universe
      </button>
      <button on:click={() => goto('/simulate')} class="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded">
        Simulate
      </button>
    </div>
  </div>

  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <div>
      <h2 class="text-lg font-bold text-white mb-4">Bead History</h2>
      <div class="bg-gray-800 rounded-lg p-4 max-h-[600px] overflow-y-auto">
        {#if beads.length === 0}
          <p class="text-gray-500">No beads in timeline. Start by creating a heroine and running simulations.</p>
        {:else}
          {#each beads as bead}
            <button
              on:click={() => selectBead(bead)}
              class="w-full text-left p-3 mb-2 rounded bg-gray-700 hover:bg-gray-600 transition {selectedBead?.id === bead.id ? 'ring-2 ring-pink-500' : ''}"
            >
              <div class="flex justify-between items-center">
                <span class="text-pink-400 font-mono text-sm">{bead.id?.slice(0, 8)}...</span>
                <span class="text-xs text-gray-400">{bead.timestamp?.split('T')[0]}</span>
              </div>
              <div class="text-white text-sm mt-1">{bead.action}</div>
              {#if bead.emotion_tag}
                <span class="text-xs px-2 py-1 bg-pink-600 rounded mt-2 inline-block">{bead.emotion_tag}</span>
              {/if}
            </button>
          {/each}
          <button
            on:click={loadMore}
            class="w-full p-3 text-center text-gray-400 hover:text-white transition"
          >
            Load More
          </button>
        {/if}
      </div>
    </div>

    <div>
      <h2 class="text-lg font-bold text-white mb-4">Bead Details</h2>
      <div class="bg-gray-800 rounded-lg p-4">
        {#if selectedBead}
          <div class="space-y-4">
            <div>
              <label class="text-gray-400 text-sm">ID</label>
              <p class="text-white font-mono">{selectedBead.id}</p>
            </div>
            <div>
              <label class="text-gray-400 text-sm">Action</label>
              <p class="text-white">{selectedBead.action}</p>
            </div>
            <div>
              <label class="text-gray-400 text-sm">Branch</label>
              <p class="text-white">{selectedBead.branch_name || 'main'}</p>
            </div>
            <div>
              <label class="text-gray-400 text-sm">Parent</label>
              <p class="text-white font-mono">{selectedBead.parent_id || 'None (Root)'}</p>
            </div>
            <div>
              <label class="text-gray-400 text-sm">Timestamp</label>
              <p class="text-white">{selectedBead.timestamp}</p>
            </div>
            <div>
              <label class="text-gray-400 text-sm">Content</label>
              <pre class="text-white text-sm bg-gray-900 p-3 rounded overflow-x-auto">{JSON.stringify(selectedBead.content, null, 2)}</pre>
            </div>
          </div>
        {:else}
          <p class="text-gray-500">Select a bead from the timeline to view details</p>
        {/if}
      </div>
    </div>
  </div>
</div>
