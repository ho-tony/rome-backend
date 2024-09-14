import {
  colorizeBackground,
  drawTiles,
  fetchMapData,
  drawBoundaries,
  onAttacked,
  onCollideWithPlayer,
} from "../utils.js";

import { generatePlayerComponents, setPlayerMovement } from "../entities/player.js";

import { gameState, playerState } from "../state/stateManager.js";
import { generateGhostComponents, onGhostDestroyed, setGhostAI } from "../entities/boss.js";
import { healthBar } from "../uiComponents/healthBar.js";

export default async function dungeon(k, entities) {
  colorizeBackground(k, 27, 29, 52);
  const mapData = await fetchMapData("./maps/dungeon.json");

  const map = k.add([k.pos(420, 111)]);

  const layers = mapData.layers;
  for (const layer of layers) {
    if (layer.name === "Boundaries") {
      drawBoundaries(k, map, layer);
      continue;
    }

    if (layer.name === "SpawnPoints") {
      for (const object of layer.objects) {
        if (object.name === "player") {
          entities.player = map.add(
            generatePlayerComponents(k, k.vec2(object.x, object.y))
          );
        }

        if (object.name === "ghost" && !gameState.getIsGhostDefeated()) {
          entities.ghost = map.add(
            generateGhostComponents(k, k.vec2(object.x, object.y)));
        }

        if (object.name === "prison-door") {
          map.add([
            k.sprite("assets", { frame: playerState.getHasKey() ? 506 : 505 }),
            !playerState.getHasKey() && k.area(),
            !playerState.getHasKey() && k.body({ isStatic: true }),
            k.pos(object.x, object.y),
            "prison-door",
          ]);
        }
      }
      continue;
    }

    drawTiles(k, map, layer, mapData.tileheight, mapData.tilewidth);
  }

  setPlayerMovement(k, entities.player, entities.projectile, map);
  
  entities.player.onCollide("door-exit", () => {
    gameState.setPreviousScene("dungeon");
    k.go("world");
  });

  entities.player.onCollide("door-entrance", async () => {
    gameState.setFreezePlayer(true);
    await slideCamY(k, -180, 1);
    entities.player.pos.y -= 64;
    gameState.setFreezePlayer(false);
  });

  entities.player.onCollide("door-exit-2", async () => {
    gameState.setFreezePlayer(true);
    await slideCamY(k, 180, 1);
    entities.player.pos.y += 48;
    gameState.setFreezePlayer(false);
  });

  if (entities.ghost) {
    setGhostAI(k, entities.ghost, entities.player);
    onAttacked(k, entities.ghost, entities.player);
    onCollideWithPlayer(k, entities.ghost);
    onGhostDestroyed(k);
  }

  k.camScale(4);
  healthBar(k);
}

async function slideCamY(k, range, duration) {
    const currentCamPos = k.camPos();
    await k.tween(
        currentCamPos.y,
        currentCamPos.y + range,
        duration,
        (newPosY) => k.camPos(currentCamPos.x, newPosY),
        k.easings.linear,
    );
}