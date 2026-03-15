import "clsx";
import "@sveltejs/kit/internal";
import "../../chunks/exports.js";
import "../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../chunks/root.js";
import "../../chunks/state.svelte.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    $$renderer2.push(`<div class="flex items-center justify-center min-h-screen"><div class="text-center"><h1 class="text-accent-2 font-pixel text-2xl mb-4 animate-pulse">Pixel Heart OS</h1> <p class="text-text-dim">Initializing...</p></div></div>`);
  });
}
export {
  _page as default
};
