import { sveltekit } from '@sveltejs/kit/vite';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

export default {
	kit: {
		ssr: false,
		vite: {
			resolve: {
				alias: {
					'$lib': '/src/lib',
					'$phaser': '/src/lib/PhaserGame.svelte'
				}
			}
		}
	},
	svelte: {
		preprocess: vitePreprocess(),
		compilerOptions: {
			// Enable experimental runes support
			runes: true,
		},
	},
};
