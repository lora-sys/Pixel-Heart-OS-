import { i as fallback, d as escape_html, e as ensure_array_like, k as bind_props, c as store_get, u as unsubscribe_stores } from "../../../chunks/root.js";
import "@sveltejs/kit/internal";
import "../../../chunks/exports.js";
import "../../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../../chunks/state.svelte.js";
import { a as apiStore } from "../../../chunks/api-store.js";
import { d as dedupedFetch } from "../../../chunks/client.js";
class NPCService {
  constructor() {
    this.basePath = "/api/v1/npcs";
  }
  async generate() {
    return dedupedFetch(`${this.basePath}/generate`, {
      method: "POST"
    });
  }
  async list() {
    return dedupedFetch(`${this.basePath}/`, {
      cacheKey: "npcs:list",
      cacheTtl: 12e4
      // 2 minutes
    });
  }
  async get(id) {
    return dedupedFetch(`${this.basePath}/${id}`, {
      cacheKey: `npc:${id}`,
      cacheTtl: 12e4
    });
  }
  async refine(id, feedback) {
    return dedupedFetch(`${this.basePath}/${id}/refine`, {
      method: "PATCH",
      body: JSON.stringify({ feedback })
    });
  }
  async applyRefinement(id, refinedData) {
    return dedupedFetch(`/${this.basePath}/${id}/refine/apply`, {
      method: "POST",
      body: JSON.stringify(refinedData)
    });
  }
}
const npcService = new NPCService();
function NPCCard($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let npc = $$props["npc"];
    let onRefine = fallback($$props["onRefine"], () => {
    });
    $$renderer2.push(`<div class="card relative group hover:shadow-pixel-accent transition-shadow"><div class="absolute -top-2 -right-2 bg-accent-2 text-white text-xs font-pixel px-2 py-1">${escape_html(npc.role)}</div> <h3 class="font-pixel text-accent-1 text-lg mb-2">${escape_html(npc.name)}</h3> <div class="mb-4"><p class="text-sm text-text-dim mb-2">${escape_html(npc.identity.personality || "No description")}</p> <p class="text-xs text-text-dim">${escape_html(npc.identity.appearance || "Appearance not specified")}</p></div> `);
    if (npc.soul?.key_traits?.length) {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<div class="mb-4"><h4 class="text-xs text-accent-3 mb-1">Traits</h4> <div class="flex flex-wrap gap-1"><!--[-->`);
      const each_array = ensure_array_like(npc.soul.key_traits);
      for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
        let trait = each_array[$$index];
        $$renderer2.push(`<span class="px-2 py-0.5 bg-bg-mid border border-border text-xs">${escape_html(trait)}</span>`);
      }
      $$renderer2.push(`<!--]--></div></div>`);
    } else {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--> <div class="flex justify-end gap-2 mt-4"><button class="text-xs text-accent-3 hover:text-accent-2">Refine ✎</button></div></div>`);
    bind_props($$props, { npc, onRefine });
  });
}
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    var $$store_subs;
    let localError = null;
    async function handleRefineNPC(npcId, feedback) {
      try {
        const result = await npcService.refine(npcId, feedback);
        apiStore.update((state) => ({
          ...state,
          npcs: state.npcs.map((npc) => npc.id === npcId ? { ...npc, ...result.suggested } : npc)
        }));
      } catch (e) {
        localError = e.message || "Failed to refine NPC";
      }
    }
    $$renderer2.push(`<div class="max-w-6xl mx-auto"><header class="mb-8"><h1 class="text-accent-2 font-pixel text-3xl mb-2">Universe</h1> <p class="text-text-dim">Your heroine's social network has emerged.</p></header> `);
    {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--> `);
    if (localError) {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<div class="mb-6 p-4 border border-red-500 text-red-300 bg-red-900/20">${escape_html(localError)}</div>`);
    } else {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--> <div class="grid grid-cols-1 lg:grid-cols-2 gap-8"><section><h2 class="font-pixel text-accent-1 text-xl mb-4">Characters</h2> <div class="space-y-4"><!--[-->`);
    const each_array = ensure_array_like(store_get($$store_subs ??= {}, "$apiStore", apiStore).npcs);
    for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
      let npc = each_array[$$index];
      NPCCard($$renderer2, {
        npc,
        onRefine: (feedback) => handleRefineNPC(npc.id, feedback)
      });
    }
    $$renderer2.push(`<!--]--></div></section> <section><h2 class="font-pixel text-accent-3 text-xl mb-4">Scenes</h2> <div class="space-y-4"><div class="card border-dashed border-2 border-border"><p class="text-text-dim text-sm">Scene generation is being woven into the fabric.</p></div></div></section></div> <div class="mt-8 text-center"><button class="btn-primary px-6 py-3 font-pixel">Enter Simulation</button></div></div>`);
    if ($$store_subs) unsubscribe_stores($$store_subs);
  });
}
export {
  _page as default
};
