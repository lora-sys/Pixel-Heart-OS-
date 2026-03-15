<script lang="ts">
  import { onMount, onDestroy, afterUpdate } from 'svelte';
  import Phaser from 'phaser';
  import { eventBus } from '$lib/event-bus';
  import { state } from '$lib/stores/app-store';
  import { simulationAPI } from '$lib/api/client';

  export let sceneType: 'timeline' | 'nebula' | 'dialogue' = 'dialogue';

  let canvas: HTMLCanvasElement;
  let game: Phaser.Game | null = null;
  let currentScene: Phaser.Scene | null = null;
  let prevBeadsLength = 0;
  let prevNebulaNodesLength = 0;

  // Helper: Get emotion color (same as app.css)
  function getEmotionColor(emotion?: string): number {
    const colors: Record<string, number> = {
      neutral: 0x8888bb,
      joy: 0xff6eb4,
      sadness: 0x4dff91,
      anger: 0xff4444,
      fear: 0xffa500,
      comforting: 0x00e5ff,
      hostile: 0xff0000,
      defiant: 0x7b61ff,
      mysterious: 0x9933ff,
    };
    return colors[emotion || 'neutral'] || 0x8888bb;
  }

  function getEdgeColor(type: string): number {
    const colors = {
      protector: 0x4dff91,
      competitor: 0xff6eb4,
      shadow: 0x7b61ff,
      neutral: 0x8888bb,
    };
    return colors[type] || 0x8888bb;
  }

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

    // Get reference to scene after creation
    game.events.on('ready', () => {
      currentScene = game?.scene.scenes[0];
    });

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

  // React to state changes (beads, nebula, activeNPCs)
  afterUpdate(() => {
    if (!currentScene) return;

    // Timeline scene: update beads
    if (sceneType === 'timeline' && state.beads.length !== prevBeadsLength) {
      prevBeadsLength = state.beads.length;
      currentScene.events.emit('update-beads', state.beads);
    }

    // Nebula scene: update nodes/edges
    if (sceneType === 'nebula') {
      const totalNodes = state.relationshipNebula.nodes.length;
      if (totalNodes !== prevNebulaNodesLength) {
        prevNebulaNodesLength = totalNodes;
        currentScene.events.emit('update-nebula', state.relationshipNebula);
      }
    }

    // Dialogue scene: update NPC
    if (sceneType === 'dialogue' && state.activeNPCs.length > 0) {
      currentScene.events.emit('update-npc', state.activeNPCs[0]);
    }
  });

  function createScene(type: string) {
    switch (type) {
      case 'timeline':
        return class TimelineScene extends Phaser.Scene {
          private beads: any[] = [];
          private beadGraphics: Phaser.GameObjects.Graphics[] = [];

          create() {
            // Listen for updates from Svelte
            this.events.on('update-beads', (beads: any[]) => {
              this.beads = beads;
              this.redraw();
            });

            // Initial draw
            this.beads = state.beads;
            this.redraw();

            eventBus.emit('scene-ready');
          }

          redraw() {
            // Clear existing
            this.beadGraphics.forEach(g => g.destroy());
            this.beadGraphics = [];

            // Draw beads in a simple grid
            this.beads.forEach((bead, i) => {
              const x = 100 + (i % 10) * 70;
              const y = 100 + Math.floor(i / 10) * 70;
              const color = getEmotionColor(bead.emotion_tag);
              const circle = this.add.circle(x, y, 20, color).setInteractive();

              // Simple hover effect
              circle.on('pointerover', () => {
                circle.setScale(1.2);
                eventBus.emit('bead-selected', bead.id);
              });
              circle.on('pointerout', () => {
                circle.setScale(1.0);
              });

              this.beadGraphics.push(circle);
            });
          }
        };
      case 'nebula':
        return class NebulaScene extends Phaser.Scene {
          create() {
            const nodes = $state.relationshipNebula.nodes;
            const edges = $state.relationshipNebula.edges;

            // Listen for updates
            this.events.on('update-nebula', (data: { nodes: any[], edges: any[] }) => {
              this.redrawNebula(data.nodes, data.edges);
            });

            this.redrawNebula(nodes, edges);
            eventBus.emit('scene-ready');
          }

          redrawNebula(nodes: any[], edges: any[]) {
            this.children.removeAll();
            // Draw edges first (under nodes)
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
            // Draw nodes
            nodes.forEach(node => {
              const circle = this.add.circle(node.x, node.y, node.size || 20, node.color).setInteractive();
              circle.on('pointerdown', () => {
                eventBus.emit('npc-clicked', node.id);
              });
            });
          }
        };
      case 'dialogue':
      default:
        return class DialogueScene extends Phaser.Scene {
          private currentNPC: any = null;
          private dialogueText?: Phaser.GameObjects.Text;

          create() {
            // Background
            this.add.rectangle(400, 300, 800, 600, 0x0d0d1a);

            // Listen for NPC updates
            this.events.on('update-npc', (npc: any) => {
              this.currentNPC = npc;
              this.updatePortrait(npc);
            });

            // Initial NPC
            const npc = $state.activeNPCs[0];
            if (npc) {
              this.currentNPC = npc;
              this.updatePortrait(npc);
            }

            // Dialogue box
            const box = this.add.rectangle(400, 450, 700, 150, 0x1a1a35).setStrokeStyle(4, 0xff6eb4);
            this.dialogueText = this.add.text(420, 420, '', {
              fontFamily: '"Share Tech Mono"',
              fontSize: '16px',
              color: '#e8e8ff',
              wordWrap: { width: 680 }
            });

            eventBus.emit('scene-ready');
          }

          updatePortrait(npc: any) {
            // Clear previous portrait
            this.children.list.forEach(child => {
              if (child.input && child.input.enabled && child !== this.dialogueText?.parent) {
                // Simplified: just update placeholder
              }
            });
            const portrait = this.add.rectangle(400, 200, 150, 150, 0x7b61ff);
            portrait.setInteractive();
            portrait.on('pointerdown', () => {
              eventBus.emit('npc-clicked', npc.id);
            });
            const name = this.add.text(400, 370, npc.name, {
              fontFamily: '"Press Start 2P"',
              fontSize: '12px',
              color: '#ff6eb4'
            }).setOrigin(0.5);
          }

          // Method to show dialogue (called via eventBus)
          showDialogue(text: string) {
            if (this.dialogueText) {
              // Typewriter effect
              this.tweens.add({
                targets: this.dialogueText,
                alpha: 0,
                duration: 100,
                onComplete: () => {
                  this.dialogueText!.setText(text);
                  this.tweens.add({ targets: this.dialogueText, alpha: 1, duration: 100 });
                }
              });
            }
          }
        };

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
