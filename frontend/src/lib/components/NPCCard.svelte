<script lang="ts">
  import type { NPC } from '$lib/stores/app-store';

  export let npc: NPC;
  export let onRefine: () => void = () => {};
</script>

<div class="card relative group hover:shadow-pixel-accent transition-shadow">
  <!-- Role badge -->
  <div class="absolute -top-2 -right-2 bg-accent-2 text-white text-xs font-pixel px-2 py-1">
    {npc.role}
  </div>

  <h3 class="font-pixel text-accent-1 text-lg mb-2">{npc.name}</h3>

  <div class="mb-4">
    <p class="text-sm text-text-dim mb-2">
      {npc.identity.personality || 'No description'}
    </p>
    <p class="text-xs text-text-dim">
      {npc.identity.appearance || 'Appearance not specified'}
    </p>
  </div>

  <!-- Soul traits -->
  {#if npc.soul?.key_traits?.length}
    <div class="mb-4">
      <h4 class="text-xs text-accent-3 mb-1">Traits</h4>
      <div class="flex flex-wrap gap-1">
        {#each npc.soul.key_traits as trait}
          <span class="px-2 py-0.5 bg-bg-mid border border-border text-xs">
            {trait}
          </span>
        {/each}
      </div>
    </div>
  {/if}

  <div class="flex justify-end gap-2 mt-4">
    <button class="text-xs text-accent-3 hover:text-accent-2" on:click={onRefine}>
      Refine ✎
    </button>
  </div>
</div>
