import { i as fallback, a as attr, j as attr_style, d as escape_html, b as attr_class, k as bind_props, s as stringify, c as store_get, u as unsubscribe_stores } from "../../../chunks/root.js";
import "@sveltejs/kit/internal";
import "../../../chunks/exports.js";
import "../../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../../chunks/state.svelte.js";
import { u as uiStore } from "../../../chunks/app-store.js";
import { a as apiStore } from "../../../chunks/api-store.js";
function TerminalInput($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    let value = fallback($$props["value"], "");
    let placeholder = fallback($$props["placeholder"], "");
    let rows = fallback($$props["rows"], 6);
    let autofocus = fallback($$props["autofocus"], true);
    $$renderer2.push(`<div class="relative group"><textarea${attr("placeholder", placeholder)}${attr("rows", rows)} class="w-full bg-bg-dark text-text-main font-mono text-sm p-4 border-2 border-border focus:border-accent-2 focus:outline-none resize-none overflow-hidden transition-colors placeholder:text-text-dim"${attr_style(`min-height: ${stringify(rows * 1.5)}em;`)}>`);
    const $$body = escape_html(value);
    if ($$body) {
      $$renderer2.push(`${$$body}`);
    }
    $$renderer2.push(`</textarea> <div${attr_class("absolute right-2 bottom-2 w-2 h-4 bg-accent-1 opacity-50", void 0, { "opacity-0": false })}></div></div>`);
    bind_props($$props, { value, placeholder, rows, autofocus });
  });
}
function _page($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    var $$store_subs;
    let description = "";
    let $$settled = true;
    let $$inner_renderer;
    function $$render_inner($$renderer3) {
      $$renderer3.push(`<div class="max-w-4xl mx-auto"><header class="mb-8 text-center"><h1 class="text-accent-2 font-pixel text-3xl mb-2">Creation Mirror</h1> <p class="text-text-dim">Describe your heroine. Let the system extract her soul.</p></header> <div class="grid grid-cols-1 md:grid-cols-2 gap-6"><div class="card"><h2 class="font-pixel text-accent-1 mb-4">Input</h2> `);
      TerminalInput($$renderer3, {
        placeholder: "Describe your heroine's personality, past, desires, fears...  Example: A shy librarian who lost her parents at young age, believes intimacy is dangerous, secretly dreams of being a rockstar...",
        rows: 12,
        get value() {
          return description;
        },
        set value($$value) {
          description = $$value;
          $$settled = false;
        }
      });
      $$renderer3.push(`<!----> <div class="mt-4 flex gap-2"><button class="btn-primary flex-1"${attr("disabled", store_get($$store_subs ??= {}, "$uiStore", uiStore).isLoading || !description.trim(), true)}>`);
      if (store_get($$store_subs ??= {}, "$uiStore", uiStore).isLoading) {
        $$renderer3.push("<!--[0-->");
        $$renderer3.push(`Parsing...`);
      } else {
        $$renderer3.push("<!--[-1-->");
        $$renderer3.push(`Create Heroine`);
      }
      $$renderer3.push(`<!--]--></button></div> `);
      {
        $$renderer3.push("<!--[-1-->");
      }
      $$renderer3.push(`<!--]--></div> <div class="card"><h2 class="font-pixel text-accent-3 mb-4">`);
      if (store_get($$store_subs ??= {}, "$apiStore", apiStore).heroine) {
        $$renderer3.push("<!--[0-->");
        $$renderer3.push(`Generated`);
      } else {
        $$renderer3.push("<!--[-1-->");
        $$renderer3.push(`Preview`);
      }
      $$renderer3.push(`<!--]--></h2> `);
      if (store_get($$store_subs ??= {}, "$apiStore", apiStore).heroine) {
        $$renderer3.push("<!--[0-->");
        $$renderer3.push(`<div class="space-y-4"><div><h3 class="text-accent-1 font-bold mb-1">Soul Structure</h3> <pre class="text-xs bg-bg-dark p-2 overflow-auto max-h-40">${escape_html(JSON.stringify(store_get($$store_subs ??= {}, "$apiStore", apiStore).heroine.soul, null, 2))}</pre></div> <div><h3 class="text-accent-3 font-bold mb-1">Identity</h3> <p class="text-sm">${escape_html(store_get($$store_subs ??= {}, "$apiStore", apiStore).heroine.identity.name)}, ${escape_html(store_get($$store_subs ??= {}, "$apiStore", apiStore).heroine.identity.age)}</p> <p class="text-text-dim">${escape_html(store_get($$store_subs ??= {}, "$apiStore", apiStore).heroine.identity.personality)}</p></div></div>`);
      } else {
        $$renderer3.push("<!--[-1-->");
        $$renderer3.push(`<p class="text-text-dim text-sm">The soul structure will appear here after parsing. It includes core traumas, defense mechanisms, ideal type, and scene preferences.</p>`);
      }
      $$renderer3.push(`<!--]--></div></div></div>`);
    }
    do {
      $$settled = true;
      $$inner_renderer = $$renderer2.copy();
      $$render_inner($$inner_renderer);
    } while (!$$settled);
    $$renderer2.subsume($$inner_renderer);
    if ($$store_subs) unsubscribe_stores($$store_subs);
  });
}
export {
  _page as default
};
