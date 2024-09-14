import { generatePlayerComponents, setPlayerMovement } from "../entities/player.js";
import { generateSlimeComponents, setSlimeAI } from "../entities/minion.js";
import { gameState } from "../state/stateManager.js";
import { healthBar } from "../uiComponents/healthBar.js";
import { colorizeBackground, drawBoundaries, drawTiles, fetchMapData, onAttacked, onCollideWithPlayer } from "../utils.js";



export default async function world(k, entities) {
    const previousScene = gameState.getPreviousScene();
    colorizeBackground(k, 76, 170, 255);
    const mapData = await fetchMapData("./maps/world.json");

    const map = k.add([k.pos(0, 0)]);

    const layers = mapData.layers;
    for (const layer of layers) {
        if (layer.name === "Boundaries") {
            drawBoundaries(k, map, layer);
            continue;
        }

        if (layer.name === "SpawnPoints") {
            for (const object of layer.objects) {
                if (object.name === "player-dungeon" && previousScene === "dungeon") {
                    entities.player = map.add(
                        generatePlayerComponents(k, k.vec2(object.x, object.y))
                    );
                }
                
                if (object.name === "player" && (!previousScene || previousScene === "house")) {
                    entities.player = map.add(generatePlayerComponents(k, k.vec2(object.x, object.y)));
                }

                if (object.name === "slime") {
                    entities.slimes.push(map.add(generateSlimeComponents(k, k.vec2(object.x, object.y))));
                }
            }
            continue;
        }

        drawTiles(k, map, layer, mapData.tileheight, mapData.tilewidth);
    }

    k.camScale(4);
    k.camPos(entities.player.worldPos());
    k.onUpdate(() => {
        if (entities.player.pos.dist(k.camPos())) {
            k.tween(
                k.camPos(),
                entities.player.worldPos(),
                0.15,
                (newPos) => {
                    k.camPos(newPos)
                },
                k.easings.linear,
            );
        }
    });

    setPlayerMovement(k, entities.player, entities.projectile, map);

    for (const slime of entities.slimes) {
        setSlimeAI(k, slime);
        onAttacked(k, slime, entities.player);
        onCollideWithPlayer(k, slime);
    }

    entities.player.onCollide("door-entrance", () => {
        gameState.setPreviousScene("world");
        k.go("house");
    });
    entities.player.onCollide("dungeon-door-entrance", () => {
        gameState.setPreviousScene("world");
        k.go("dungeon");
    });

    healthBar(k);
}
