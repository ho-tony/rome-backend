import globalStateManager from "./globalState.js";
import playerGlobalStateManager from "./playerGlobalState.js";

export const playerState = playerGlobalStateManager().getInstance();
export const gameState = globalStateManager().getInstance();