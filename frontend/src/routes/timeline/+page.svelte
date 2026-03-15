<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { apiStore } from '$lib/core/store';
  import { beadService } from '$lib/services';
  import type { Bead } from '$lib/types/shared-types';

  let beads: Bead[] = [];
  let loading = false;
  let error: string | null = null;
  let selectedBranch = 'main';

  onMount(async () => {
    if (!apiStore.heroine) {
      goto('/create');
      return;
    }
    await loadTimeline();
  });

  async function loadTimeline() {
    loading = true;
    error = null;

    try {
      const timeline = await beadService.getTimeline(selectedBranch, 100);
      beads = timeline;
    } catch (e: any) {
      error = e.message || 'Failed to load timeline';
    } finally {
      loading = false;
    }
  }

  function formatTimestamp(ts: string): string {
    return new Date(ts).toLocaleString();
  }

  function getEmotionColor(emotion?: string): string {
    const colors: Record<string, string> = {
      joy: 'text-yellow-400',
      sadness: 'text-blue-400',
      anger: 'text-red-400',
      fear: 'text-purple-400',
      neutral: 'text-gray-400'
    };
    return colors[emotion || 'neutral'] || 'text-gray-400';
  }
</script>

<div class="max-w-4xl mx-auto">
  <header class="mb-8">
    <h1 class="text-accent-2 font-pixel text-3xl mb-2">Timeline</h1>
    <p class="text-text-dim">The narrative history as a chain of beads.</p>
  </header>

  {#if loading}
    <div class="text-center py-12">
      <span class="text-accent-1 animate-pulse">Loading beads...</span>
    </div>
  {/if}

  {#if error}
    <div class="mb-6 p-4 border border-red-500 text-red-300 bg-red-900/20">
      {error}
    </div>
  {/if}

  <!-- Branch selector -->
  <div class="mb-6 flex items-center gap-4">
    <label class="font-pixel text-sm">Branch:</label>
    <select
      bind:value={selectedBranch}
      on:change={loadTimeline}
      class="bg-bg-dark border border-border px-3 py-1 font-mono"
    >
      <option value="main">main</option>
      <!-- other branches would be populated from beadService.listBranches() -->
    </select>
    <button class="btn-secondary text-xs px-3 py-1" on:click={loadTimeline}>
      Refresh
    </button>
  </div>

  <!-- Beads timeline -->
  <div class="space-y-3">
    {#each beads as bead (bead.id)}
      <div
        class="card border-l-4 {bead.emotion_tag ? getEmotionColor(bead.emotion_tag) : 'border-accent-1'}"
      >
        <div class="flex justify-between items-start">
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-2">
              <span class="font-pixel text-xs text-text-dim">#{bead.id.slice(0, 8)}</span>
              <span class="text-xs px-2 py-0.5 bg-accent-2/20 text-accent-2">
                {bead.action}
              </span>
              {#if bead.emotion_tag}
                <span class="text-xs px-2 py-0.5 bg-accent-1/20 text-accent-1">
                  {bead.emotion_tag}
                </span>
              {/if}
            </div>

            <p class="text-sm text-text-dim mb-2">
              {formatTimestamp(bead.timestamp)}
            </p>

            <pre class="text-xs bg-bg-dark p-2 overflow-auto max-h-40">
{JSON.stringify(bead.content, null, 2)}
            </pre>
          </div>

          <div class="ml-4 text-xs text-text-dim">
            branch: {bead.branch_name}
          </div>
        </div>
      </div>
    {/each}
  </div>

  {#if beads.length === 0 && !loading}
    <div class="text-center py-12 text-text-dim">
      <p>No beads in the timeline yet.</p>
      <p class="text-sm">Start a simulation to create your first bead.</p>
    </div>
  {/if}
</div>
