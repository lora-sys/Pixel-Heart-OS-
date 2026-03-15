<script lang="ts">
  import { onMount } from 'svelte';
  import { state, type NPC } from '$lib/stores/app-store';
  import { simulationAPI, npcAPI } from '$lib/api/client';
  import { eventBus } from '$lib/event-bus';
  import { goto } from '$app/navigation';
  import PhaserGame from '$lib/PhaserGame.svelte';

  let playerInput = '';
  let loading = false;
  let dialogueHistory: Array<{ speaker: string; text: string; emotion?: string }> = [];
  let currentSceneType: 'dialogue' = 'dialogue';

  onMount(async () => {
    if (!$state.heroine || $state.npcs.length === 0) {
      goto('/universe');
      return;
    }

    // Load initial simulation state
    await loadState();

    // Listen for NPC clicks from Phaser
    const unsubscribe = eventBus.on('npc-clicked', (npcId: string) => {
      // Could show NPC detail panel
      console.log('NPC clicked:', npcId);
    });

    return () => unsubscribe();
  });

  async function loadState() {
    try {
      const simState = await simulationAPI.getState();

      // Update active NPCs
      state.activeNPCs = simState.active_npcs;

      // Load NPC voice data for dialogue
      for (const npc of simState.active_npcs) {
        const fullNPC = await npcAPI.get(npc.id);
        npc.voice = fullNPC.voice;
      }

      // Set current scene
      if (simState.current_scene) {
        state.currentScene = simState.current_scene;
      }

      // Load recent history
      dialogueHistory = []; // Would reconstruct from beads
    } catch (e) {
      console.error('Failed to load state:', e);
    }
  }

  async function takeTurn() {
    if (!playerInput.trim()) return;

    const action = playerInput;
    playerInput = '';
    loading = true;

    try {
      const response = await simulationAPI.takeTurn(action);

      // Add player action to history
      dialogueHistory.push({ speaker: 'player', text: action });

      // Add NPC responses with typing effect
      response.responses.forEach((resp, idx) => {
        const npc = state.activeNPCs.find(n => n.id === resp.npc_id);
        const speaker = npc?.name || 'NPC';
        setTimeout(() => {
          dialogueHistory.push({
            speaker,
            text: resp.dialogue,
            emotion: resp.emotion
          });
          // Trigger Phaser dialogue update
          eventBus.emit('show-dialogue', resp.dialogue);
        }, idx * 1000);
      });

      // Update relationships
      Object.entries(response.updated_relationships).forEach(([npcId, trust]) => {
        console.log(`Relationship update: ${npcId} → ${trust}`);
      });

      // Refresh beads
      const timeline = await beadsAPI.getTimeline();
      state.beads = timeline;

    } catch (e: any) {
      console.error('Turn failed:', e);
      dialogueHistory.push({ speaker: 'system', text: `Error: ${e.message}` });
    } finally {
      loading = false;
    }
  }

  // Refs
  let inputEl: HTMLTextAreaElement;
  function focusInput() {
    inputEl?.focus();
  }
</script>

<div class="max-w-7xl mx-auto">
  <header class="mb-6">
    <h1 class="text-accent-2 font-pixel text-2xl mb-2">Simulation</h1>
    <div class="flex justify-between items-center text-text-dim text-sm">
      <span>Scene: {state.currentScene?.name || 'None'}</span>
      <span>Beads: {$state.beads.length}</span>
      <button
        class="text-accent-3 hover:underline"
        on:click={() => goto('/timeline')}
      >
        View Timeline →
      </button>
    </div>
  </header>

  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
    <!-- Left: Phaser Game -->
    <div class="lg:col-span-2">
      <div class="card">
        <PhaserGame sceneType={currentSceneType} />
      </div>

      <!-- Player Input -->
      <div class="mt-4">
        <label class="block text-sm text-text-dim mb-2">Your response...</label>
        <textarea
          bind:value={playerInput}
          bind:this={inputEl}
          on:keydown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); takeTurn(); } }}
          placeholder="Type your reply... (Enter to send, Shift+Enter for newline)"
          rows="3"
          class="w-full bg-bg-dark border-2 border-border focus:border-accent-2 p-3 font-mono text-sm text-text-main resize-none focus:outline-none"
          disabled={loading}
        />
        <div class="mt-2 flex justify-end">
          <button
            class="btn-primary"
            disabled={loading || !playerInput.trim()}
            on:click={takeTurn}
          >
            {#if loading}
              Sending...
            {:else}
              Send
            {/if}
          </button>
        </div>
      </div>
    </div>

    <!-- Right: Dialogue Panel -->
    <div class="lg:col-span-1">
      <div class="card h-[600px] overflow-y-auto flex flex-col">
        <h2 class="font-pixel text-accent-3 mb-4 sticky top-0 bg-bg-card pb-2">
          Conversation
        </h2>

        <div class="flex-1 space-y-4" on:click={focusInput}>
          {#each dialogueHistory as entry}
            <div class="text-sm" class:ml-8={entry.speaker === 'player'}>
              <div class="font-bold text-accent-2 mb-1">
                {entry.speaker === 'player' ? 'You' : entry.speaker}
                {#if entry.emotion}
                  <span class="text-text-dim font-normal ml-2">({entry.emotion})</span>
                {/if}
              </div>
              <p class="text-text-main bg-bg-mid p-2 border-l-2 border-accent-1">
                {entry.text}
              </p>
            </div>
          {/each}

          {#if loading}
            <div class="text-text-dim animate-pulse">Waiting for NPCs...</div>
          {/if}
        </div>
      </div>
    </div>
  </div>
</div>
