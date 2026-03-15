/**
 * EventBus for Svelte ↔ Phaser communication
 */
type EventCallback = (...args: any[]) => void;

class EventBus {
  private listeners: Map<string, Set<EventCallback>> = new Map();

  emit(event: string, ...args: any[]): void {
    const callbacks = this.listeners.get(event);
    if (callbacks) {
      callbacks.forEach(cb => {
        try {
          cb(...args);
        } catch (e) {
          console.error(`Error in event listener for ${event}:`, e);
        }
      });
    }
  }

  on(event: string, callback: EventCallback): () => void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(callback);

    // Return unsubscribe function
    return () => this.off(event, callback);
  }

  off(event: string, callback: EventCallback): void {
    const callbacks = this.listeners.get(event);
    if (callbacks) {
      callbacks.delete(callback);
    }
  }

  removeAllListeners(event?: string): void {
    if (event) {
      this.listeners.delete(event);
    } else {
      this.listeners.clear();
    }
  }
}

// Singleton instance
export const eventBus = new EventBus();

// Event type definitions
export const Events = {
  // Svelte → Phaser
  BEAD_HIGHLIGHT: 'bead-highlight',
  SWITCH_SCENE: 'switch-scene',
  NPC_MOVE: 'npc-move',
  SHOW_DIALOGUE: 'show-dialogue',
  UPDATE_NEBULA: 'update-nebula',

  // Phaser → Svelte
  SCENE_READY: 'scene-ready',
  NPC_CLICKED: 'npc-clicked',
  DIALOGUE_CHOICE: 'dialogue-choice',
  BEAD_SELECTED: 'bead-selected',
  NEBULA_INTERACTION: 'nebula-interaction'
} as const;
