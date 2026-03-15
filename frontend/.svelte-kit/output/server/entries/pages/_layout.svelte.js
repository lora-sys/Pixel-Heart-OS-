import { g as getContext, e as ensure_array_like, a as attr, b as attr_class, s as stringify, c as store_get, d as escape_html, u as unsubscribe_stores, f as setContext, h as slot } from "../../chunks/root.js";
import "clsx";
import "@sveltejs/kit/internal";
import "../../chunks/exports.js";
import "../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../chunks/state.svelte.js";
import { a as apiStore } from "../../chunks/api-store.js";
import { u as uiStore } from "../../chunks/app-store.js";
const getStores = () => {
  const stores$1 = getContext("__svelte__");
  return {
    /** @type {typeof page} */
    page: {
      subscribe: stores$1.page.subscribe
    },
    /** @type {typeof navigating} */
    navigating: {
      subscribe: stores$1.navigating.subscribe
    },
    /** @type {typeof updated} */
    updated: stores$1.updated
  };
};
const page = {
  subscribe(fn) {
    const store = getStores().page;
    return store.subscribe(fn);
  }
};
function Navigation($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    var $$store_subs;
    const navItems = [
      { href: "/create", label: "Create" },
      { href: "/universe", label: "Universe" },
      { href: "/simulate", label: "Simulate" },
      { href: "/timeline", label: "Timeline" }
    ];
    $$renderer2.push(`<nav class="bg-bg-mid border-b border-border px-6 py-3"><div class="flex items-center justify-between"><a href="/" class="text-accent-1 font-pixel text-lg no-underline hover:text-accent-2">Pixel Heart OS</a> <ul class="flex space-x-2"><!--[-->`);
    const each_array = ensure_array_like(navItems);
    for (let $$index = 0, $$length = each_array.length; $$index < $$length; $$index++) {
      let item = each_array[$$index];
      $$renderer2.push(`<li><a${attr("href", item.href)}${attr_class(`px-3 py-1 font-pixel text-sm no-underline transition-all ${stringify(store_get($$store_subs ??= {}, "$page", page).url.pathname.startsWith(item.href) ? "bg-accent-2 text-white shadow-pixel" : "text-text-dim hover:text-text-main hover:border-border border border-transparent")}`)}>${escape_html(item.label)}</a></li>`);
    }
    $$renderer2.push(`<!--]--></ul> <div class="text-text-dim text-xs">`);
    if (store_get($$store_subs ??= {}, "$apiStore", apiStore).heroine) {
      $$renderer2.push("<!--[0-->");
      $$renderer2.push(`<span class="text-accent-1">Heroine: ${escape_html(store_get($$store_subs ??= {}, "$apiStore", apiStore).heroine.identity.name)}</span>`);
    } else {
      $$renderer2.push("<!--[-1-->");
      $$renderer2.push(`<span>No heroine</span>`);
    }
    $$renderer2.push(`<!--]--></div></div></nav>`);
    if ($$store_subs) unsubscribe_stores($$store_subs);
  });
}
function _layout($$renderer, $$props) {
  $$renderer.component(($$renderer2) => {
    setContext("uiStore", uiStore);
    setContext("apiStore", apiStore);
    $$renderer2.push(`<div class="min-h-screen bg-bg-dark text-text-main font-mono">`);
    Navigation($$renderer2);
    $$renderer2.push(`<!----> <main class="container mx-auto px-4 py-8"><!--[-->`);
    slot($$renderer2, $$props, "default", {});
    $$renderer2.push(`<!--]--></main> <footer class="text-center py-4 text-text-dim text-sm">Pixel Heart OS v0.1.0</footer></div>`);
  });
}
export {
  _layout as default
};
