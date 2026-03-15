<script lang="ts">
  export let original: any;
  export let suggested: any;
  export let diff: Array<{ field: string; from: any; to: any }>;

  type ViewMode = 'side-by-side' | 'inline';
  let viewMode: ViewMode = 'side-by-side';

  function formatValue(val: any): string {
    if (val === undefined || val === null) return '—';
    if (typeof val === 'object') return JSON.stringify(val, null, 2);
    return String(val);
  }
</script>

<div class="diff-viewer">
  <div class="flex justify-end mb-4">
    <div class="btn-group">
      <button
        class="px-3 py-1 text-sm border border-border bg-bg-card"
        class:bg-accent-2={viewMode === 'side-by-side'}
        on:click={() => viewMode = 'side-by-side'}
      >
        Side-by-Side
      </button>
      <button
        class="px-3 py-1 text-sm border border-border bg-bg-card"
        class:bg-accent-2={viewMode === 'inline'}
        on:click={() => viewMode = 'inline'}
      >
        Inline
      </button>
    </div>
  </div>

  {#if diff.length === 0}
    <p class="text-text-dim">No changes proposed.</p>
  {:else}
    {#if viewMode === 'side-by-side'}
      <div class="grid grid-cols-2 gap-4">
        <!-- Original -->
        <div class="card">
          <h3 class="font-pixel text-accent-1 mb-4">Original</h3>
          {#each Object.entries(original) as [key, val]}
            <div class="mb-3">
              <div class="text-xs text-text-dim mb-1">{key}</div>
              <pre class="text-sm bg-bg-dark p-2">{formatValue(val)}</pre>
            </div>
          {/each}
        </div>

        <!-- Suggested -->
        <div class="card">
          <h3 class="font-pixel text-accent-3 mb-4">Suggested</h3>
          {#each Object.entries(suggested) as [key, val]}
            <div class="mb-3">
              <div class="text-xs text-text-dim mb-1">{key}</div>
              <pre class="text-sm bg-bg-dark p-2">{formatValue(val)}</pre>
            </div>
          {/each}
        </div>
      </div>
    {:else}
      <div class="card">
        {#each diff as change}
          <div class="mb-4 border-b border-border pb-4 last:border-0">
            <div class="font-bold text-accent-2 mb-2">{change.field}</div>
            <div class="grid grid-cols-2 gap-4">
              <div class="bg-red-900 bg-opacity-30 p-2 border-l-4 border-red-500">
                <div class="text-xs text-red-300 mb-1">FROM</div>
                <pre class="text-sm">{formatValue(change.from)}</pre>
              </div>
              <div class="bg-green-900 bg-opacity-30 p-2 border-l-4 border-green-500">
                <div class="text-xs text-green-300 mb-1">TO</div>
                <pre class="text-sm">{formatValue(change.to)}</pre>
              </div>
            </div>
          </div>
        {/each}
      </div>
    {/if}
  {/if}
</div>
