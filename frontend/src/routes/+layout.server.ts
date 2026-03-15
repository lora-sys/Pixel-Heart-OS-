/**
 * Main layout server load function
 * Preloads initial application state from backend
 */
import type { LayoutServerLoad } from './$types';
import { heroineService } from '$lib/services/heroine.service';
import { beadService } from '$lib/services/bead.service';

export const load: LayoutServerLoad = async () => {
  try {
    // Preload initial data in parallel
    const [heroine, timeline] = await Promise.allSettled([
      heroineService.get(),
      beadService.getTimeline('main', 10)
    ]);

    const heroineData = heroine.status === 'fulfilled' ? heroine.value : null;
    const timelineData = timeline.status === 'fulfilled' ? timeline.value : [];

    return {
      heroine: heroineData,
      initialBeads: timelineData
    };
  } catch (error) {
    console.error('Failed to preload initial state:', error);
    return {
      heroine: null,
      initialBeads: []
    };
  }
};
