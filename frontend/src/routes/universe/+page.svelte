<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { uiStore, apiStore, invalidateCache, API_CACHE_KEYS } from '$lib/core/store';
  import { npcService, sceneService } from '$lib/services';
  import NPCCard from '$lib/components/NPCCard.svelte';
  import SceneCard from '$lib/components/SceneCard.svelte';
  import DiffViewer from '$lib/components/DiffViewer.svelte';

  let loading = false;
  let localError: string | null = null;
  let refiningNPC: any = null;
  let refinement: { original: any; suggested: any; diff: any[] } | null = null;

  onMount(async () => {
    if (!apiStore.heroine) {
      goto('/create');
      return;
    }
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
      apiStore.npcs = npcs;

      // Load scenes (generate if needed)
      // Note: sceneService.list() returns empty currently (needs implementation)
      // For now, we can skip or generate
      await sceneService.generate(); // Generate some scenes

    } catch (e: any) {
      localError = e.message || 'Failed to load universe';
      uiStore.errorMessage = localError;
    } finally {
      loading = false;
    }
  }

  async function startSimulation() {
    goto('/simulate');
  }

  async function handleRefineNPC(npcId: string, feedback: string) {
    try {
      const result = await npcService.refine(npcId, feedback);
      refinement = result;

      // Update store with refined data after user approves
      // For now, auto-apply (refine endpoint already updates DB)
      const index = apiStore.npcs.findIndex(n => n.id === npcId);
      if (index !== -1) {
        apiStore.npcs[index] = { ...apiStore.npcs[index], ...result.suggested };
      }

      invalidateCache(API_CACHE_KEYS.NPC(npcId));
      invalidateCache(API_CACHE_KEYS.NPC_LIST);
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
        {#each apiStore.npcs as npc (npc.id)}
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
        <!-- Scenes would be populated here -->
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
      on:click={startSimulation}
    >
      Enter Simulation
    </button>
  </div>
</div>
