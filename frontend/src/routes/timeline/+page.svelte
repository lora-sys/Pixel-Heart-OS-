<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { api } from '$lib/api/client';
  import * as store from '$lib/core/store/api-store';
  import DiffViewer from '$lib/components/DiffViewer.svelte';

  let beads = $state<any[]>([]);
  let selectedBead = $state<any>(null);
  let compareBead = $state<any>(null);
  let diffResult = $state<any>(null);
  let loading = $state(false);
  let page = $state(1);
  const pageSize = 20;

  onMount(async () => {
    await loadBeads();
  });

  async function loadBeads() {
    loading = true;
    try {
      const result = await api.getBeads('main', pageSize);
      beads = result || [];
    } catch (e) {
      console.error('Failed to load beads:', e);
    } finally {
      loading = false;
    }
  }

  async function loadMore() {
    loading = true;
    try {
      const result = await api.getBeads('main', beads.length + pageSize);
      beads = result || [];
      page++;
    } catch (e) {
      console.error('Failed to load more beads:', e);
    } finally {
      loading = false;
    }
  }

  function selectBead(bead: any) {
    if (selectedBead && selectedBead.id !== bead.id) {
      compareBead = bead;
      computeDiff();
    } else {
      selectedBead = bead;
      compareBead = null;
      diffResult = null;
    }
  }

  function computeDiff() {
    if (!selectedBead || !compareBead) return;
    
    const content1 = selectedBead.content || {};
    const content2 = compareBead.content || {};
    
    const added: Record<string, any> = {};
    const removed: Record<string, any> = {};
    const modified: Record<string, any> = {};
    
    for (const key in content2) {
      if (!(key in content1)) {
        added[key] = content2[key];
      } else if (JSON.stringify(content1[key]) !== JSON.stringify(content2[key])) {
        modified[key] = { old: content1[key], new: content2[key] };
      }
    }
    
    for (const key in content1) {
      if (!(key in content2)) {
        removed[key] = content1[key];
      }
    }
    
    diffResult = { added, removed, modified };
  }

  function clearSelection() {
    selectedBead = null;
    compareBead = null;
    diffResult = null;
  }

  function getEmotionColor(emotion: string | null) {
    const colors: Record<string, string> = {
      joy: '#4ade80',
      sadness: '#3b82f6',
      anger: '#f87171',
      fear: '#a78bfa',
      hope: '#34d399',
      mystery: '#8b5cf6',
    };
    return emotion ? (colors[emotion] || '#94a3b8') : '#94a3b8';
  }
</script>

<div class="p-6">
  <div class="flex justify-between items-center mb-6">
    <h1 class="text-2xl font-bold text-white">Timeline</h1>
    <div class="flex gap-2">
      <button onclick={() => goto('/universe')} class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded">
        Universe
      </button>
      <button onclick={() => goto('/simulate')} class="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded">
        Simulate
      </button>
    </div>
  </div>

  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <div>
      <h2 class="text-lg font-bold text-white mb-4">Bead History</h2>
      <p class="text-gray-400 text-sm mb-3">Click to select, click another to compare</p>
      <div class="bg-gray-800 rounded-lg p-4 max-h-[600px] overflow-y-auto">
        {#if beads.length === 0}
          <p class="text-gray-500">No beads in timeline. Start by creating a heroine and running simulations.</p>
        {:else}
          {#each beads as bead}
            <button
              onclick={() => selectBead(bead)}
              class="w-full text-left p-3 mb-2 rounded transition {selectedBead?.id === bead.id ? 'bg-pink-600' : compareBead?.id === bead.id ? 'bg-green-600' : 'bg-gray-700 hover:bg-gray-600'}"
            >
              <div class="flex justify-between items-center">
                <span class="font-mono text-sm">{bead.id?.slice(0, 8)}...</span>
                <span class="text-xs">{bead.timestamp?.split('T')[0]}</span>
              </div>
              <div class="text-sm mt-1">{bead.action}</div>
              {#if bead.emotion_tag}
                <span 
                  class="text-xs px-2 py-1 rounded mt-2 inline-block"
                  style="background: {getEmotionColor(bead.emotion_tag)}"
                >
                  {bead.emotion_tag}
                </span>
              {/if}
            </button>
          {/each}
          <button
            onclick={loadMore}
            disabled={loading}
            class="w-full p-3 text-center text-gray-400 hover:text-white transition disabled:opacity-50"
          >
            {loading ? 'Loading...' : 'Load More'}
          </button>
        {/if}
      </div>
    </div>

    <div>
      <h2 class="text-lg font-bold text-white mb-4">Bead Details</h2>
      <div class="bg-gray-800 rounded-lg p-4">
        {#if selectedBead}
          <div class="space-y-4">
            <div class="flex justify-between items-center">
              <h3 class="text-pink-400 font-bold">Selected Bead</h3>
              <button onclick={clearSelection} class="text-gray-400 hover:text-white">Clear</button>
            </div>
            
            <div>
              <label class="text-gray-400 text-sm">ID</label>
              <p class="text-white font-mono text-sm">{selectedBead.id}</p>
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
              <p class="text-white font-mono text-sm">{selectedBead.parent_id || 'None (Root)'}</p>
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

          {#if compareBead}
            <div class="mt-6 pt-6 border-t border-gray-700">
              <h3 class="text-green-400 font-bold mb-4">Comparison Bead</h3>
              <div>
                <label class="text-gray-400 text-sm">ID</label>
                <p class="text-white font-mono text-sm">{compareBead.id}</p>
              </div>
              <div class="mt-2">
                <label class="text-gray-400 text-sm">Action</label>
                <p class="text-white">{compareBead.action}</p>
              </div>
            </div>

            {#if diffResult}
              <div class="mt-6 pt-6 border-t border-gray-700">
                <h3 class="text-yellow-400 font-bold mb-4">Diff Result</h3>
                <DiffViewer diff={diffResult} />
              </div>
            {/if}
          {/if}
        {:else}
          <p class="text-gray-500">Select a bead from the timeline to view details</p>
        {/if}
      </div>
    </div>
  </div>
</div>
