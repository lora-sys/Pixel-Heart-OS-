<script lang="ts">
  import { onMount } from 'svelte';
  import { state, type NPC } from '$lib/stores/app-store';
  import { npcAPI, sceneAPI } from '$lib/api/client';
  import { goto } from '$app/navigation';
  import NPCCard from '$lib/components/NPCCard.svelte';
  import SceneCard from '$lib/components/SceneCard.svelte';
  import DiffViewer from '$lib/components/DiffViewer.svelte';

  let loading = false;
  let error: string | null = null;
  let refiningNPC: NPC | null = null;
  let refinement: { original: any; suggested: any; diff: any[] } | null = null;

  onMount(async () => {
    if (!$state.heroine) {
      goto('/create');
      return;
    }

    await loadUniverse();
  });

  async function loadUniverse() {
    loading = true;
    error = null;

    try {
      // Load NPCs
      const npcs = await npcAPI.list();
      if (npcs.length === 0) {
        // Generate NPCs if none exist
        const generated = await npcAPI.generate();
        state.npcs = generated.map(n => ({
          id: n.id,
          name: n.name,
          role: n.role as 'protector' | 'competitor' | 'shadow',
          soul: n.soul,
          identity: n.identity,
          voice: n.voice,
          created_at: n.created_at
        }));
      } else {
        state.npcs = npcs;
      }

      // Load scenes (generate if needed)
      const scenes = await sceneAPI.list();
      if (scenes.length === 0) {
        await sceneAPI.generate();
      }
    } catch (e: any) {
      error = e.message || 'Failed to load universe';
    } finally {
      loading = false;
    }
  }

  async function startSimulation() {
    goto('/simulate');
  }

  async function startRefinement(npc: NPC) {
    refiningNPC = npc;
    const result = await npcAPI.refine(npc.id, 'Deepen the character: give more nuanced motivations and internal contradictions');
    refinement = result;
  }

  async function applyRefinement() {
    if (!refinement) return;
    await npcAPI.applyRefinement(refiningNPC!.id, refinement.suggested);
    // Refresh NPC data
    const updated = await npcAPI.get(refiningNPC!.id);
    state.npcs = state.npcs.map(n =>
      n.id === refiningNPC!.id
        ? { ...n, ...updated, soul: updated.soul, identity: updated.identity, voice: updated.voice }
        : n
    );
    refiningNPC = null;
    refinement = null;
  }
</script>

<div class="max-w-6xl mx-auto">
  <header class="mb-8">
    <h1 class="text-accent-2 font-pixel text-3xl mb-2">Emergent Universe</h1>
    <p class="text-text-dim">
      Your heroine's soul has manifested these characters and scenes.
    </p>
  </header>

  {#if loading}
    <div class="text-center py-12">
      <div class="inline-block animate-spin text-accent-1 text-4xl">⟳</div>
      <p class="mt-4">Generating universe...</p>
    </div>
  {/if}

  {#if error}
    <div class="card border-red-500 mb-6">
      <p class="text-red-300">{error}</p>
    </div>
  {/if}

  <!-- NPCs Section -->
  <section class="mb-12">
    <h2 class="font-pixel text-accent-1 text-xl mb-4">Characters</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      {#each $state.npcs as npc (npc.id)}
        <NPCCard
          {npc}
          on:refine={() => startRefinement(npc)}
        />
      {/each}
    </div>
  </section>

  <!-- Scenes Section -->
  <section class="mb-12">
    <h2 class="font-pixel text-accent-3 text-xl mb-4">Environments</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Placeholder - will populate with scene data -->
      {#each ['Rainy Window', 'Midnight Store', 'Abandoned Park'] as sceneName, i}
        <SceneCard
          name={sceneName}
          description="A moody environment matching the heroine's preferences."
        />
      {/each}
    </div>
  </section>

  <!-- Action -->
  <div class="text-center py-8">
    <button class="btn-primary font-pixel text-lg px-8 py-3" on:click={startSimulation}>
      Begin Simulation →
    </button>
  </div>
</div>

<!-- Refinement Modal -->
{#if refiningNPC && refinement}
  <div class="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
    <div class="card max-w-4xl w-full max-h-[90vh] overflow-auto mx-4">
      <h2 class="font-pixel text-accent-2 text-xl mb-4">
        Refine: {refiningNPC.name}
      </h2>
      <DiffViewer
        original={refinement.original}
        suggested={refinement.suggested}
        diff={refinement.diff}
      />
      <div class="flex justify-end gap-4 mt-6">
        <button class="btn-secondary" on:click={() => { refiningNPC = null; refinement = null; }}>
          Cancel
        </button>
        <button class="btn-primary" on:click={applyRefinement}>
          Apply Changes
        </button>
      </div>
    </div>
  </div>
{/if}
