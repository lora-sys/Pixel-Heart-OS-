/**
 * Frontend Services - Unified API clients
 */
export { heroineService } from './heroine.service';
export { npcService } from './npc.service';
export { beadService } from './bead.service';
export { sceneService } from './scene.service';
export { simulationService } from './simulation.service';
export type { CreateHeroineRequest, HeroineResponse } from './heroine.service';
export type { NPCResponse, NPCRefineRequest, NPCRefineResponse } from './npc.service';
export type { BeadCreate, BeadResponse, BranchCreate, BranchResponse, BeadDiffChange, BeadDiffResponse } from './bead.service';
export type { SceneResponse } from './scene.service';
export type { SimulationTurnRequest, SimulationTurnResponse, SimulationStateResponse } from './simulation.service';
