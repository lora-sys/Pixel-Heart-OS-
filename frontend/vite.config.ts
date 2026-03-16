import { svelte } from '@sveltejs/vite-plugin-svelte';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [svelte()],
  optimizeDeps: {
    include: ['phaser'],
  },
  build: {
    target: 'esnext',
  },
});