import type { LayoutLoad } from './$types';

export const load: LayoutLoad = async ({ fetch }) => {
  // Preload initial app state from backend
  try {
    const res = await fetch('/api/v1/heroine/');
    const heroine = res.ok ? await res.json() : null;

    return { heroine };
  } catch (e) {
    return { heroine: null };
  }
};
