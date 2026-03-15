<script lang="ts">
  import { onMount, onDestroy } from 'svelte';

  export let value = '';
  export let placeholder = '';
  export let rows = 6;
  export let autofocus = true;

  let textarea: HTMLTextAreaElement;
  let cursorVisible = true;

  onMount(() => {
    if (autofocus) {
      textarea?.focus();
    }

    // Blink cursor effect
    const interval = setInterval(() => {
      cursorVisible = !cursorVisible;
    }, 530);

    return () => clearInterval(interval);
  });

  function handleInput() {
    // Auto-resize
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
  }
</script>

<div class="relative group">
  <textarea
    bind:this={textarea}
    bind:value
    on:input={handleInput}
    placeholder={placeholder}
    rows={rows}
    class="w-full bg-bg-dark text-text-main font-mono text-sm p-4
           border-2 border-border focus:border-accent-2 focus:outline-none
           resize-none overflow-hidden transition-colors
           placeholder:text-text-dim"
    style="min-height: {rows * 1.5}em;"
  />

  <!-- Cursor blink indicator -->
  <div
    class="absolute right-2 bottom-2 w-2 h-4 bg-accent-1 opacity-50"
    class:opacity-0={!cursorVisible}
  />
</div>
