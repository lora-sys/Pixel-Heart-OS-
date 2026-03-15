<script lang="ts">
  import { onMount } from 'svelte';
  import { state } from '$lib/stores/app-store';
  import { heroineAPI } from '$lib/api/client';
  import { goto } from '$app/navigation';
  import TerminalInput from '$lib/components/TerminalInput.svelte';

  let description = '';
  let loading = false;
  let error: string | null = null;
  let createdData: any = null;

  async function handleCreate() {
    if (!description.trim()) return;

    loading = true;
    error = null;

    try {
      const result = await heroineAPI.create(description);
      createdData = result;

      // Update global state
      state.heroine = {
        id: result.id,
        soul: result.soul,
        identity: result.identity,
        voice: result.voice,
        created_at: result.created_at
      };

      // Navigate to universe after short delay
      setTimeout(() => goto('/universe'), 1500);
    } catch (e: any) {
      error = e.message || 'Failed to create heroine';
    } finally {
      loading = false;
    }
  }
</script>

<div class="max-w-4xl mx-auto">
  <header class="mb-8 text-center">
    <h1 class="text-accent-2 font-pixel text-3xl mb-2">Creation Mirror</h1>
    <p class="text-text-dim">Describe your heroine. Let the system extract her soul.</p>
  </header>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <!-- Input Panel -->
    <div class="card">
      <h2 class="font-pixel text-accent-1 mb-4">Input</h2>
      <TerminalInput
        bind:value={description}
        placeholder="Describe your heroine's personality, past, desires, fears...&#10;&#10;Example: A shy librarian who lost her parents at young age, believes intimacy is dangerous, secretly dreams of being a rockstar..."
        rows={12}
      />

      <div class="mt-4 flex gap-2">
        <button
          class="btn-primary flex-1"
          disabled={loading || !description.trim()}
          on:click={handleCreate}
        >
          {#if loading}
            Parsing...
          {:else}
            Create Heroine
          {/if}
        </button>
      </div>

      {#if error}
        <div class="mt-4 p-3 border border-red-500 text-red-300">
          {error}
        </div>
      {/if}
    </div>

    <!-- Preview Panel -->
    <div class="card">
      <h2 class="font-pixel text-accent-3 mb-4">
        {#if createdData}
          Generated
        {:else}
          Preview
        {/if}
      </h2>

      {#if createdData}
        <div class="space-y-4">
          <div>
            <h3 class="text-accent-1 font-bold mb-1">Soul Structure</h3>
            <pre class="text-xs bg-bg-dark p-2 overflow-auto max-h-40">{JSON.stringify(createdData.soul, null, 2)}</pre>
          </div>

          <div>
            <h3 class="text-accent-3 font-bold mb-1">Identity</h3>
            <p class="text-sm">{createdData.identity.name}, {createdData.identity.age}</p>
            <p class="text-text-dim">{createdData.identity.personality}</p>
          </div>
        </div>
      {:else}
        <p class="text-text-dim text-sm">
          The soul structure will appear here after parsing. It includes core traumas, defense mechanisms, ideal type, and scene preferences.
        </p>
      {/if}
    </div>
  </div>
</div>
