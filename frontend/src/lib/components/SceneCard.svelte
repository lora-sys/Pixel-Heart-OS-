<script lang="ts">
  export let name: string;
  export let description: string;
  export let config: Record<string, any> = {};
</script>

<div class="card">
  <div class="aspect-video bg-bg-mid mb-4 flex items-center justify-center border-2 border-border relative overflow-hidden">
    <!-- Placeholder pixel art rendering -->
    <div class="text-6xl opacity-20">🌆</div>
    <div class="absolute bottom-2 right-2 text-xs text-text-dim font-mono">
      {config.environment?.time_of_day || 'evening'}
    </div>
  </div>

  <h3 class="font-pixel text-accent-3 mb-2">{name}</h3>
  <p class="text-sm text-text-dim">{description}</p>

  {#if config.mood}
    <div class="mt-3">
      <span class="px-2 py-1 bg-bg-mid border border-border text-xs">
        Mood: {config.mood}
      </span>
    </div>
  {/if}
</div>
