import { w as writable } from "./index.js";
const apiStore = writable({
  heroine: null,
  npcs: [],
  beads: [],
  scenes: [],
  relationshipNebula: { nodes: [], edges: [] },
  lastUpdated: null
});
export {
  apiStore as a
};
