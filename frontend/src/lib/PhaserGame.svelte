<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import Phaser from 'phaser';
  import { eventBus } from '$lib/event-bus';
  import { state } from '$lib/stores/app-store';
  import { simulationAPI } from '$lib/api/client';

  export let sceneType: 'timeline' | 'nebula' | 'dialogue' = 'dialogue';

  let canvas: HTMLCanvasElement;
  let game: Phaser.Game | null = null;

  onMount(() => {
    const config: Phaser.Types.Core.GameConfig = {
      type: Phaser.AUTO,
      width: 800,
      height: 600,
      parent: canvas,
      backgroundColor: '#0d0d1a',
      scene: createScene(sceneType),
      physics: { default: 'arcade' },
      plugins: {
        global: [
          {
            key: 'EventBusPlugin',
            plugin: class {
              private eventBus: typeof eventBus;
              constructor(eventBus: typeof eventBus) {
                this.eventBus = eventBus;
              }
              start() {}
            },
            start: 'start',
            argument: eventBus
          }
        ]
      }
    };

    game = new Phaser.Game(config);

    // Listen for events from Svelte
    const unsubscribeHighlight = eventBus.on('bead-highlight', (data: any) => {
      game?.scene.scenes[0]?.events?.emit('highlight-bead', data);
    });

    const unsubscribeSwitchScene = eventBus.on('switch-scene', (data: any) => {
      game?.scene.scenes[0]?.events?.emit('change-scene', data);
    });

    return () => {
      unsubscribeHighlight();
      unsubscribeSwitchScene();
      game?.destroy(true);
    };
  });

  function createScene(type: string) {
    switch (type) {
      case 'timeline':
        return class TimelineScene extends Phaser.Scene {
          create() {
            // Basic implementation: render beads as circles
            const beads = $state.beads;
            beads.forEach((bead, i) => {
              const x = 100 + (i % 10) * 70;
              const y = 100 + Math.floor(i / 10) * 70;
              const color = getEmotionColor(bead.emotion_tag);
              this.add.circle(x, y, 20, color).setInteractive();
            });

            // Notify Svelte when scene is ready
            eventBus.emit('scene-ready');
          }
        };
      case 'nebula':
        return class NebulaScene extends Phaser.Scene {
          create() {
            const nodes = $state.relationshipNebula.nodes;
            nodes.forEach(node => {
              this.add.circle(node.x, node.y, node.size, node.color).setInteractive();
            });

            const edges = $state.relationshipNebula.edges;
            edges.forEach(edge => {
              const source = nodes.find(n => n.id === edge.source);
              const target = nodes.find(n => n.id === edge.target);
              if (source && target) {
                this.add.line(
                  0, 0,
                  source.x, source.y,
                  target.x, target.y,
                  getEdgeColor(edge.type)
                ).setLineWidth(2 * edge.strength);
              }
            });

            eventBus.emit('scene-ready');
          }
        };
      case 'dialogue':
      default:
        return class DialogueScene extends Phaser.Scene {
          private currentNPC: any = null;

          create() {
            // Background
            this.add.rectangle(400, 300, 800, 600, 0x0d0d1a);

            // NPC sprite placeholder
            const npc = $state.activeNPCs[0];
            if (npc) {
              this.currentNPC = npc;
              const portrait = this.add.rectangle(400, 200, 150, 150, 0x7b61ff);
              portrait.setInteractive();

              portrait.on('pointerdown', () => {
                eventBus.emit('npc-clicked', npc.id);
              });
            }

            eventBus.emit('scene-ready');
          }

          updateDialogue(text: string) {
            // Clear old text
            this.children.list.forEach(child => {
              if (child.type === 'Text' && child.style?.fontFamily?.includes('Share')) {
                child.destroy();
              }
            });

            // Add new dialogue
            this.add.text(400, 450, text, {
              fontSize: '16px',
              fontFamily: '"Share Tech Mono", monospace',
              color: '#e8e8ff',
              align: 'center',
              wordWrap: { width: 700 }
            }).setOrigin(0.5);
          }
        };
    }
  }

  function getEmotionColor(emotion?: string): number {
    const colors: Record<string, number> = {
      joy: 0xff6eb4,
      sadness: 0x00e5ff,
      anger: 0xff0000,
      fear: 0x8888bb,
      neutral: 0x3a3a6a,
      comforting: 0x4dff91,
      hostile: 0xff4444,
      defiant: 0xffaa00
    };
    return colors[emotion || 'neutral'] || 0x3a3a6a;
  }

  function getEdgeColor(type: string): number {
    switch (type) {
      case 'protector': return 0x4dff91;
      case 'competitor': return 0xff6eb4;
      case 'shadow': return 0x7b61ff;
      default: return 0x3a3a6a;
    }
  }
</script>

<div class="relative">
  <canvas bind:this={canvas} class="border-2 border-border" />
  {#if sceneType === 'dialogue'}
    <slot />
  {/if}
</div>
