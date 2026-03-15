<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { uiStore, apiStore } from '$lib/core/store';
  import { npcService } from '$lib/services';
  import NPCCard from '$lib/components/NPCCard.svelte';

  let loading = false;
  let localError: string | null = null;

  onMount(async () => {
    await loadUniverse();
  });

  async function loadUniverse() {
    loading = true;
    localError = null;

    try {
      // Load NPCs with cache
      let npcs = await npcService.list();

      if (npcs.length === 0) {
        // Generate NPCs if none exist
        npcs = await npcService.generate();
      }

      // Update API store
      apiStore.update(state => ({ ...state, npcs, lastUpdated: new Date().toISOString() }));

    } catch (e: any) {
      localError = e.message || 'Failed to load universe';
      uiStore.update(s => ({ ...s, errorMessage: localError }));
    } finally {
      loading = false;
    }
  }

  async function handleRefineNPC(npcId: string, feedback: string) {
    try {
      const result = await npcService.refine(npcId, feedback);

      // Update store with refined data
      apiStore.update(state => ({
        ...state,
        npcs: state.npcs.map(npc =>
          npc.id === npcId
            ? { ...npc, ...result.suggested }
            : npc
        )
      }));
    } catch (e: any) {
      localError = e.message || 'Failed to refine NPC';
    }
  }
</script>

<div class="max-w-6xl mx-auto">
  <header class="mb-8">
    <h1 class="text-accent-2 font-pixel text-3xl mb-2">Universe</h1>
    <p class="text-text-dim">Your heroine's social network has emerged.</p>
  </header>

  {#if loading}
    <div class="text-center py-12">
      <span class="text-accent-1 animate-pulse">Weaving the universe...</span>
    </div>
  {/if}

  {#if localError}
    <div class="mb-6 p-4 border border-red-500 text-red-300 bg-red-900/20">
      {localError}
    </div>
  {/if}

  <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
    <!-- NPCs Section -->
    <section>
      <h2 class="font-pixel text-accent-1 text-xl mb-4">Characters</h2>
      <div class="space-y-4">
        {#each $apiStore.npcs as npc (npc.id)}
          <NPCCard
            {npc}
            onRefine={(feedback) => handleRefineNPC(npc.id, feedback)}
          />
        {/each}
      </div>
    </section>

    <!-- Scenes Section -->
    <section>
      <h2 class="font-pixel text-accent-3 text-xl mb-4">Scenes</h2>
      <div class="space-y-4">
        <div class="card border-dashed border-2 border-border">
          <p class="text-text-dim text-sm">
            Scene generation is being woven into the fabric.
          </p>
        </div>
      </div>
    </section>
  </div>

  <div class="mt-8 text-center">
    <button
      class="btn-primary px-6 py-3 font-pixel"
      on:click={() => goto('/simulate')}
    >
      Enter Simulation
    </button>
  </div>
</div>
