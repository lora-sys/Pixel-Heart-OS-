import * as server from '../entries/pages/_layout.server.ts.js';

export const index = 0;
let component_cache;
export const component = async () => component_cache ??= (await import('../entries/pages/_layout.svelte.js')).default;
export { server };
export const server_id = "src/routes/+layout.server.ts";
export const imports = ["_app/immutable/nodes/0.hwII-1IU.js","_app/immutable/chunks/R877U7Uo.js","_app/immutable/chunks/Bk7iIqpG.js","_app/immutable/chunks/D7z-YRkH.js","_app/immutable/chunks/DGSb-iIt.js","_app/immutable/chunks/DpWp-lt_.js","_app/immutable/chunks/-h97gLd5.js","_app/immutable/chunks/B119w5cv.js","_app/immutable/chunks/CGnvKsNS.js","_app/immutable/chunks/CSLvq1rF.js","_app/immutable/chunks/C_AcyxYy.js","_app/immutable/chunks/CBvjmynT.js"];
export const stylesheets = ["_app/immutable/assets/0.BsC_OcXo.css"];
export const fonts = [];
