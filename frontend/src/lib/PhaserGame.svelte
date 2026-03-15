<script lang="ts">
  import { onMount, onDestroy, afterUpdate } from 'svelte';
  import type { Phaser } from 'phaser';
  import { eventBus } from '$lib/event-bus';
  import { apiStore } from '$lib/core/store';

  export let sceneType: 'timeline' | 'nebula' | 'dialogue' = 'dialogue';

  let canvas: HTMLCanvasElement;
  let game: Phaser.Game | null = null;
  let currentScene: Phaser.Scene | null = null;
  let prevBeadsLength = 0;
  let prevNebulaNodesLength = 0;

  // Helper: Get emotion color
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

    const unsubscribeDialogue = eventBus.on('dialogue-update', (data: { npc_id: string; dialogue: string }) => {
      if (currentScene && 'updateDialogue' in currentScene) {
        (currentScene as any).updateDialogue(data.dialogue);
      }
    });

    return () => {
      unsubscribeHighlight();
      unsubscribeSwitchScene();
      unsubscribeDialogue();
      game?.destroy(true);
    };
  });

  // React to state changes
  afterUpdate(() => {
    if (!currentScene) return;

    // Timeline scene: update beads
    if (sceneType === 'timeline' && apiStore.beads.length !== prevBeadsLength) {
      prevBeadsLength = apiStore.beads.length;
      currentScene.events.emit('update-beads', apiStore.beads);
    }

    // Nebula scene: update nodes/edges
    if (sceneType === 'nebula') {
      const totalNodes = apiStore.relationshipNebula?.nodes.length || 0;
      if (totalNodes !== prevNebulaNodesLength) {
        prevNebulaNodesLength = totalNodes;
        currentScene.events.emit('update-nebula', apiStore.relationshipNebula);
      }
    }

    // Dialogue scene: update NPC
    if (sceneType === 'dialogue' && apiStore.npcs.length > 0) {
      currentScene.events.emit('update-npc', apiStore.npcs[0]);
    }
  });

  function createScene(type: string) {
    switch (type) {
      case 'timeline':
        return class TimelineScene extends Phaser.Scene {
          private beads: any[] = [];
          private beadGraphics: Phaser.GameObjects.Graphics[] = [];

          create() {
            this.events.on('update-beads', (beads: any[]) => {
              this.beads = beads;
              this.redraw();
            });

            this.beads = apiStore.beads;
            this.redraw();
            eventBus.emit('scene-ready');
          }

          redraw() {
            this.beadGraphics.forEach(g => g.destroy());
            this.beadGraphics = [];

            this.beads.forEach((bead, i) => {
              const x = 100 + (i % 10) * 70;
              const y = 100 + Math.floor(i / 10) * 70;
              const color = getEmotionColor(bead.emotion_tag);
              const circle = this.add.circle(x, y, 20, color).setInteractive();

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
            const nodes = apiStore.relationshipNebula?.nodes || [];
            const edges = apiStore.relationshipNebula?.edges || [];

            this.events.on('update-nebula', (data: { nodes: any[], edges: any[] }) => {
              this.redrawNebula(data.nodes, data.edges);
            });

            this.redrawNebula(nodes, edges);
            eventBus.emit('scene-ready');
          }

          redrawNebula(nodes: any[], edges: any[]) {
            this.children.removeAll();
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
            this.add.rectangle(400, 300, 800, 600, 0x0d0d1a);

            this.events.on('update-npc', (npc: any) => {
              this.currentNPC = npc;
              this.updatePortrait(npc);
            });

            const npc = apiStore.npcs[0];
            if (npc) {
              this.currentNPC = npc;
              this.updatePortrait(npc);
            }

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
            this.children.list.forEach(child => {
              if (child.input && child.input.enabled && child !== this.dialogueText?.parent) {
                child.destroy();
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

          showDialogue(text: string) {
            if (this.dialogueText) {
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

          updateDialogue(text: string) {
            this.children.list.forEach(child => {
              if (child.type === 'Text' && child.style?.fontFamily?.includes('Share')) {
                child.destroy();
              }
            });
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
</script>

<div bind:this={canvas} class="w-full h-full"></div>
