<script lang="ts">
  import { page } from '$app/stores';
  import { apiStore } from '$lib/core/store';

  const navItems = [
    { href: '/create', label: 'Create' },
    { href: '/universe', label: 'Universe' },
    { href: '/simulate', label: 'Simulate' },
    { href: '/timeline', label: 'Timeline' }
  ];
</script>

<nav class="bg-bg-mid border-b border-border px-6 py-3">
  <div class="flex items-center justify-between">
    <a href="/" class="text-accent-1 font-pixel text-lg no-underline hover:text-accent-2">
      Pixel Heart OS
    </a>

    <ul class="flex space-x-2">
      {#each navItems as item}
        <li>
          <a
            href={item.href}
            class="px-3 py-1 font-pixel text-sm no-underline transition-all
              {$page.url.pathname.startsWith(item.href)
                ? 'bg-accent-2 text-white shadow-pixel'
                : 'text-text-dim hover:text-text-main hover:border-border border border-transparent'}"
          >
            {item.label}
          </a>
        </li>
      {/each}
    </ul>

    <div class="text-text-dim text-xs">
      {#if $apiStore.heroine}
        <span class="text-accent-1">Heroine: {$apiStore.heroine.identity.name}</span>
      {:else}
        <span>No heroine</span>
      {/if}
    </div>
  </div>
</nav>
