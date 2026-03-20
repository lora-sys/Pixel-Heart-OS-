<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { api } from '$lib/api/client';
  import * as store from '$lib/core/store/api-store';

  let playerAction = $state('');
  let loading = $state(false);
  let lastResponse = $state<any>(null);
  let history = $state<any[]>([]);

  async function runTurn() {
    if (!playerAction.trim()) return;
    loading = true;
    try {
      const result = await api.runSimulation(playerAction);
      lastResponse = result;
      history = [...history, { action: playerAction, response: result }];
      playerAction = '';
    } catch (e) {
      console.error(e);
    } finally {
      loading = false;
    }
  }

  async function reset() {
    await api.resetSimulation();
    history = [];
    lastResponse = null;
  }

  function getEmotionColor(emotion: string) {
    const colors: Record<string, string> = {
      joy: '#4ade80',
      sadness: '#3b82f6',
      anger: '#f87171',
      fear: '#a78bfa',
      neutral: '#94a3b8',
    };
    return colors[emotion] || colors.neutral;
  }
</script>

<div class="p-6">
  <div class="flex justify-between items-center mb-6">
    <h1 class="text-2xl font-bold text-white">Simulate</h1>
    <div class="flex gap-2">
      <button onclick={() => goto('/universe')} class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded">
        Universe
      </button>
      <button onclick={() => goto('/timeline')} class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded">
        Timeline
      </button>
    </div>
  </div>

  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <div>
      <div class="bg-gray-800 rounded-lg p-4 mb-4">
        <h2 class="text-lg font-bold text-pink-400 mb-3">Your Action</h2>
        <form onsubmit={(e) => { e.preventDefault(); runTurn(); }}>
          <textarea
            bind:value={playerAction}
            placeholder="What does your heroine do?"
            class="w-full h-32 bg-gray-700 text-white rounded p-3 mb-3 resize-none"
            disabled={loading}
          ></textarea>
          <div class="flex gap-2">
            <button
              type="submit"
              disabled={loading || !playerAction.trim()}
              class="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded disabled:opacity-50"
            >
              {loading ? 'Thinking...' : 'Send'}
            </button>
            <button
              type="button"
              onclick={reset}
              class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded"
            >
              Reset
            </button>
          </div>
        </form>
      </div>

      {#if lastResponse}
        <div class="bg-gray-800 rounded-lg p-4">
          <h2 class="text-lg font-bold text-green-400 mb-3">Turn {lastResponse.turn_number}</h2>
          {#each lastResponse.npc_responses as response}
            <div class="mb-3 pb-3 border-b border-gray-700">
              <div class="flex items-center gap-2 mb-1">
                <p class="text-pink-300 font-bold">{response.npc_name}</p>
                <span 
                  class="text-xs px-2 py-1 rounded"
                  style="background: {getEmotionColor(response.emotion)}"
                >
                  {response.emotion}
                </span>
              </div>
              <p class="text-gray-300">{response.message}</p>
            </div>
          {/each}
        </div>
      {/if}
    </div>

    <div>
      <h2 class="text-lg font-bold text-white mb-3">History</h2>
      <div class="bg-gray-800 rounded-lg p-4 max-h-96 overflow-y-auto">
        {#if history.length === 0}
          <p class="text-gray-500">No conversation yet. Start by sending an action!</p>
        {:else}
          {#each history as entry, i}
            <div class="mb-4 pb-4 border-b border-gray-700">
              <div class="flex justify-between items-center mb-2">
                <p class="text-pink-400 font-bold">Turn {i + 1}</p>
                <p class="text-gray-500 text-sm">You:</p>
              </div>
              <p class="text-gray-300 mb-2">{entry.action}</p>
              {#each entry.response.npc_responses as resp}
                <div class="ml-4 mt-2">
                  <p class="text-green-400 text-sm font-bold">{resp.npc_name}:</p>
                  <p class="text-gray-300 text-sm">{resp.message}</p>
                </div>
              {/each}
            </div>
          {/each}
        {/if}
      </div>
    </div>
  </div>
</div>
