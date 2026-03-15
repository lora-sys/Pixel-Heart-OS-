import { k as bind_props, i as fallback, e as ensure_array_like, b as attr_class, s as stringify, d as escape_html, a as attr } from "../../../chunks/root.js";
import "@sveltejs/kit/internal";
import "../../../chunks/exports.js";
import "../../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../../chunks/state.svelte.js";
function PhaserGame($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let sceneType = fallback($$props["sceneType"], "dialogue");
    $$renderer2.push(`<div class="w-full h-full"></div>`);
    bind_props($$props, { sceneType });
  });
}
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let playerInput = "";
    let localLoading = false;
    let dialogueHistory = [];
    $$renderer2.push(`<div class="max-w-6xl mx-auto"><header class="mb-8"><h1 class="text-accent-2 font-pixel text-3xl mb-2">Simulation</h1> <p class="text-text-dim">Interact with your characters. Watch the story unfold.</p></header> `);
    {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--> <div class="grid grid-cols-1 lg:grid-cols-3 gap-6"><div class="lg:col-span-2 card space-y-4"><h2 class="font-pixel text-accent-1">Dialogue</h2> <div class="h-96 overflow-y-auto space-y-3 p-2 bg-bg-dark border border-border"><!--[-->`);
    const each_array = ensure_array_like(dialogueHistory);
    for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
      let entry = each_array[$$index];
      $$renderer2.push(`<div${attr_class(`border-l-4 ${stringify(entry.speaker === "player" ? "border-accent-2 pl-3" : "border-accent-1 pl-3")}`)}><span class="font-bold text-sm">${escape_html(entry.speaker)}</span> <p class="text-text-main">${escape_html(entry.text)}</p> `);
      if (entry.emotion) {
        $$renderer2.push("<!--[0-->");
        $$renderer2.push(`<span class="text-xs text-text-dim">[${escape_html(entry.emotion)}]</span>`);
      } else {
        $$renderer2.push("<!--[-1-->");
      }
      $$renderer2.push(`<!--]--></div>`);
    }
    $$renderer2.push(`<!--]--></div> <div class="flex gap-2"><input type="text"${attr("value", playerInput)} placeholder="What do you say?" class="flex-1 bg-bg-dark border border-border px-3 py-2 font-mono focus:outline-none focus:border-accent-2"${attr("disabled", localLoading, true)}/> <button class="btn-primary px-6"${attr("disabled", !playerInput.trim(), true)}>`);
    {
      $$renderer2.push("<!--[-1-->");
      $$renderer2.push(`Send`);
    }
    $$renderer2.push(`<!--]--></button></div></div> <div class="card"><h2 class="font-pixel text-accent-3 mb-4">Visualization</h2> <div class="bg-bg-dark border border-border" style="height: 400px;">`);
    PhaserGame($$renderer2, { sceneType: "dialogue" });
    $$renderer2.push(`<!----></div> <div class="mt-4 text-xs text-text-dim">Relationship nebula will appear here.</div></div></div></div>`);
  });
}
export {
  _page as default
};
