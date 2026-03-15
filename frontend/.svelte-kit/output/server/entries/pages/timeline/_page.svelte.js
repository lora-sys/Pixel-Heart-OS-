import { e as ensure_array_like, b as attr_class, s as stringify, d as escape_html } from "../../../chunks/root.js";
import "@sveltejs/kit/internal";
import "../../../chunks/exports.js";
import "../../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../../chunks/state.svelte.js";
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let beads = [];
    let selectedBranch = "main";
    function formatTimestamp(ts) {
      return new Date(ts).toLocaleString();
    }
    function getEmotionColor(emotion) {
      const colors = {
        joy: "text-yellow-400",
        sadness: "text-blue-400",
        anger: "text-red-400",
        fear: "text-purple-400",
        neutral: "text-gray-400"
      };
      return colors[emotion || "neutral"] || "text-gray-400";
    }
    $$renderer2.push(`<div class="max-w-4xl mx-auto"><header class="mb-8"><h1 class="text-accent-2 font-pixel text-3xl mb-2">Timeline</h1> <p class="text-text-dim">The narrative history as a chain of beads.</p></header> `);
    {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--> `);
    {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--> <div class="mb-6 flex items-center gap-4"><label for="branch-select" class="font-pixel text-sm">Branch:</label> `);
    $$renderer2.select(
      {
        id: "branch-select",
        value: selectedBranch,
        class: "bg-bg-dark border border-border px-3 py-1 font-mono"
      },
      ($$renderer3) => {
        $$renderer3.option({ value: "main" }, ($$renderer4) => {
          $$renderer4.push(`main`);
        });
      }
    );
    $$renderer2.push(` <button class="btn-secondary text-xs px-3 py-1">Refresh</button></div> <div class="space-y-3"><!--[-->`);
    const each_array = ensure_array_like(beads);
    for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
      let bead = each_array[$$index];
      $$renderer2.push(`<div${attr_class(`card border-l-4 ${stringify(bead.emotion_tag ? getEmotionColor(bead.emotion_tag) : "border-accent-1")}`)}><div class="flex justify-between items-start"><div class="flex-1"><div class="flex items-center gap-2 mb-2"><span class="font-pixel text-xs text-text-dim">#${escape_html(bead.id.slice(0, 8))}</span> <span class="text-xs px-2 py-0.5 bg-accent-2/20 text-accent-2">${escape_html(bead.action)}</span> `);
      if (bead.emotion_tag) {
        $$renderer2.push("<!--[0-->");
        $$renderer2.push(`<span class="text-xs px-2 py-0.5 bg-accent-1/20 text-accent-1">${escape_html(bead.emotion_tag)}</span>`);
      } else {
        $$renderer2.push("<!--[-1-->");
      }
      $$renderer2.push(`<!--]--></div> <p class="text-sm text-text-dim mb-2">${escape_html(formatTimestamp(bead.timestamp))}</p> <pre class="text-xs bg-bg-dark p-2 overflow-auto max-h-40">${escape_html(JSON.stringify(bead.content, null, 2))}
            </pre></div> <div class="ml-4 text-xs text-text-dim">branch: ${escape_html(bead.branch_name)}</div></div></div>`);
    }
    $$renderer2.push(`<!--]--></div> `);
    if (beads.length === 0 && true) {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<div class="text-center py-12 text-text-dim"><p>No beads in the timeline yet.</p> <p class="text-sm">Start a simulation to create your first bead.</p></div>`);
    } else {
      $$renderer2.push("<!--[-1-->");
    }
    $$renderer2.push(`<!--]--></div>`);
  });
}
export {
  _page as default
};
