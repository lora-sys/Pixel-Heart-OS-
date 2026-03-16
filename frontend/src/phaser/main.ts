// frontend/src/phaser/main.ts
import type { GameConfig } from 'phaser';

// Basic Phaser configuration
// This will be extended with actual scenes and game logic later
export const config: GameConfig = {
  type: 'phaser-auto', // Let Phaser decide between WebGL and Canvas
  width: 800,
  height: 600,
  parent: 'game-container', // This will be overridden by the parent element in the component
  backgroundColor: '#000000',
  scale: {
    mode: 'fit',
    autoCenter: true,
  },
  // We'll add scenes later
  scene: [],
};

export default config;
