import { d as dedupedFetch } from "../../chunks/client.js";
class HeroineService {
  constructor() {
    this.basePath = "/api/v1/heroine";
  }
  async create(request) {
    return dedupedFetch(`${this.basePath}/create`, {
      method: "POST",
      body: JSON.stringify(request)
    });
  }
  async get() {
    return dedupedFetch(`${this.basePath}/`, {
      cacheKey: "heroine:current",
      cacheTtl: 12e4
      // 2 minutes
    });
  }
  async update(id, updates) {
    throw new Error("Not implemented");
  }
  async refine(id, feedback) {
    throw new Error("Not implemented");
  }
}
const heroineService = new HeroineService();
class BeadService {
  constructor() {
    this.basePath = "/api/v1/beads";
  }
  async getTimeline(branch, limit = 100, offset = 0) {
    const params = new URLSearchParams({
      limit: limit.toString(),
      offset: offset.toString(),
      ...branch && { branch }
    });
    return dedupedFetch(`${this.basePath}/timeline?${params}`, {
      cacheKey: `beads:timeline:${branch || "main"}:${limit}:${offset}`,
      cacheTtl: 6e4
      // 1 minute
    });
  }
  async create(data) {
    return dedupedFetch(this.basePath, {
      method: "POST",
      body: JSON.stringify(data)
    });
  }
  async createBranch(branchName, fromBeadId) {
    return dedupedFetch(`${this.basePath}/branch`, {
      method: "POST",
      body: JSON.stringify({ branch_name: branchName, from_bead_id: fromBeadId })
    });
  }
  async diff(beadId1, beadId2) {
    return dedupedFetch(`${this.basePath}/diff/${beadId1}/${beadId2}`);
  }
  async listBranches() {
    return dedupedFetch(`/${this.basePath}/branches`, {
      cacheKey: "branches:all",
      cacheTtl: 12e4
      // 2 minutes
    });
  }
  async getBead(id) {
    throw new Error("Not implemented");
  }
}
const beadService = new BeadService();
const load = async () => {
  try {
    const [heroine, timeline] = await Promise.allSettled([
      heroineService.get(),
      beadService.getTimeline("main", 10)
    ]);
    const heroineData = heroine.status === "fulfilled" ? heroine.value : null;
    const timelineData = timeline.status === "fulfilled" ? timeline.value : [];
    return {
      heroine: heroineData,
      initialBeads: timelineData
    };
  } catch (error) {
    console.error("Failed to preload initial state:", error);
    return {
      heroine: null,
      initialBeads: []
    };
  }
};
export {
  load
};
