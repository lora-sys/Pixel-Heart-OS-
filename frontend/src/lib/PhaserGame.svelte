<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import type { Game } from 'phaser';
  import { eventBus } from './event-bus';
  import { config } from '../phaser/main';
  import type { Scene } from 'phaser';

  let game: Game;
  let canvas: HTMLCanvasElement;

  // This component will be a placeholder for the Phaser canvas
  // We'll create the game instance on mount and destroy it on unmount

  onMount(() => {
    // Create the Phaser game instance
    game = new Game({ ...config, parent: canvas });

    // Set up EventBus listeners for communication from Svelte to Phaser
    // These are examples of events that Svelte might send to Phaser
    const unsubscribeHighlight = eventBus.subscribe('bead-highlight', (data: { beadId: string }) => {
      // In a real implementation, we would send this to the Phaser scene
      // For now, we just log it
      console.log('Highlight bead:', data.beadId);
    });

    const unsubscribeSwitchScene = eventBus.subscribe('switch-scene', (data: { sceneKey: string }) => {
      // In a real implementation, we would switch the Phaser scene
      console.log('Switch to scene:', data.sceneKey);
    });

    // We would add more event listeners as needed for the project

    // Return cleanup functions from onMount
    return () => {
      unsubscribeHighlight();
      unsubscribeSwitchScene();
      // Destroy the game instance
      if (game) {
        game.destroy(true);
      }
    };
  });
</script>

<canvas bind:this={canvas} />
