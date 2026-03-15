<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { uiStore, apiStore } from '$lib/core/store';
  import { simulationService } from '$lib/services/simulation.service';
  import { eventBus } from '$lib/event-bus';
  import PhaserGame from '$lib/PhaserGame.svelte';

  let playerInput = '';
  let localLoading = false;
  let dialogueHistory: Array<{ speaker: string; text: string; emotion?: string }> = [];
  let localError: string | null = null;

  onMount(async () => {
    // Check heroine and NPCs existence
    const checkAndLoad = () => {
      const state = { ...$apiStore }; // Snapshot
      if (!state.heroine || state.npcs.length === 0) {
        goto('/universe');
        return;
      }
      loadState();
    };

    // Initial check
    checkAndLoad();
  });

  async function loadState() {
    try {
      const simState = await simulationService.getState();

      // Update API store with scenes if needed
      if (simState.current_scene) {
        apiStore.update(state => ({
          ...state,
          scenes: [simState.current_scene]
        }));
      }

      // Load recent history (would reconstruct from beads)
      dialogueHistory = [];
    } catch (e: any) {
      console.error('Failed to load state:', e);
      localError = e.message;
    }
  }

  async function takeTurn() {
    if (!playerInput.trim()) return;

    const action = playerInput;
    playerInput = '';
    localLoading = true;
    localError = null;

    try {
      const response = await simulationService.takeTurn({
        player_action: action
      });

      // Add player action to history
      dialogueHistory.push({ speaker: 'player', text: action });

      // Add NPC responses with typing effect
      response.responses.forEach((resp, idx) => {
        setTimeout(() => {
          dialogueHistory.push({
            speaker: resp.npc_name || resp.npc_id,
            text: resp.dialogue,
            emotion: resp.emotion
          });
          eventBus.emit('dialogue-update', { npc_id: resp.npc_id, dialogue: resp.dialogue });
        }, idx * 500);
      });

    } catch (e: any) {
      localError = e.message || 'Failed to take turn';
      uiStore.update(s => ({ ...s, errorMessage: localError }));
    } finally {
      localLoading = false;
    }
  }
</script>

<div class="max-w-6xl mx-auto">
  <header class="mb-8">
    <h1 class="text-accent-2 font-pixel text-3xl mb-2">Simulation</h1>
    <p class="text-text-dim">Interact with your characters. Watch the story unfold.</p>
  </header>

  {#if localError}
    <div class="mb-6 p-4 border border-red-500 text-red-300 bg-red-900/20">
      {localError}
    </div>
  {/if}

  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
    <!-- Dialogue Panel (2 cols) -->
    <div class="lg:col-span-2 card space-y-4">
      <h2 class="font-pixel text-accent-1">Dialogue</h2>

      <!-- Dialogue History -->
      <div class="h-96 overflow-y-auto space-y-3 p-2 bg-bg-dark border border-border">
        {#each dialogueHistory as entry}
          <div class="border-l-4 {entry.speaker === 'player' ? 'border-accent-2 pl-3' : 'border-accent-1 pl-3'}">
            <span class="font-bold text-sm">{entry.speaker}</span>
            <p class="text-text-main">{entry.text}</p>
            {#if entry.emotion}
              <span class="text-xs text-text-dim">[{entry.emotion}]</span>
            {/if}
          </div>
        {/each}
      </div>

      <!-- Player Input -->
      <div class="flex gap-2">
        <input
          type="text"
          bind:value={playerInput}
          placeholder="What do you say?"
          class="flex-1 bg-bg-dark border border-border px-3 py-2 font-mono focus:outline-none focus:border-accent-2"
          on:keydown={(e) => e.key === 'Enter' && !localLoading && takeTurn()}
          disabled={localLoading}
        />
        <button
          class="btn-primary px-6"
          disabled={localLoading || !playerInput.trim()}
          on:click={takeTurn}
        >
          {#if localLoading}
            ...
          {:else}
            Send
          {/if}
        </button>
      </div>
    </div>

    <!-- Phaser Canvas / Status Panel -->
    <div class="card">
      <h2 class="font-pixel text-accent-3 mb-4">Visualization</h2>
      <div class="bg-bg-dark border border-border" style="height: 400px;">
        <PhaserGame sceneType="dialogue" />
      </div>
      <div class="mt-4 text-xs text-text-dim">
        Relationship nebula will appear here.
      </div>
    </div>
  </div>
</div>
