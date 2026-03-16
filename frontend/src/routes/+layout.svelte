<script lang="ts">
  import PhaserGame from '$lib/PhaserGame.svelte';
</script>

<svelte:head>
  <title>Pixel Heart OS</title>
</svelte:head>

<div class="min-h-screen flex flex-col">
  <header class="bg-gray-900 text-white p-4">
    <h1 class="text-xl font-bold">Pixel Heart OS</h1>
  </header>
  
  <main class="flex-1 flex">
    <!-- Sidebar would go here -->
    <aside class="w-64 bg-gray-800 p-4">
      Sidebar
    </aside>
    
    <!-- Main content area with Phaser game -->
    <section class="flex-1 p-4">
      <PhaserGame />
    </section>
  </main>
  
  <footer class="bg-gray-900 text-white p-4 text-center">
    Footer
  </footer>
</div>
