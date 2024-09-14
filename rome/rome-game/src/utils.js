import { playerState } from "./state/stateManager.js";
import { healthBar } from "./uiComponents/healthBar.js";
import { gameState } from "./state/stateManager.js";

export function playAnimIfNotPlaying(gameObj, animName) {
    if (gameObj.curAnim() !== animName) gameObj.play(animName);
}

export function areAnyKeysDown(k, keys) {
    for (const key of keys) {
        if (k.isKeyDown(key)) return true;
    }

    return false;
}

export function areAllKeysDown(k, keys) {
    for (const key of keys) {
        if (!k.isKeyDown(key)) return false;
    }

    return true;
}

export function colorizeBackground(k, r, g, b) {
  k.add([k.rect(k.canvas.width, k.canvas.height), k.color(r, g, b), k.fixed()]);
}

export async function fetchMapData(mapName) {
    const response = await fetch(mapName);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  }

export function drawTiles(k, map, layer, tileHeight, tileWidth) {
    for (let y = 0; y < layer.height; y++) {
        for (let x = 0; x < layer.width; x++) {
            const tileIndex = y * layer.width + x;
            const tile = layer.data[tileIndex];

            if (tile === 0) continue;

            const tilePos = k.vec2(x * tileWidth, y * tileHeight);

            map.add([
                k.sprite("assets", {frame: tile - 1}),
                k.pos(tilePos.x, tilePos.y),
                k.offscreen()
            ]);
        }
    }
}

// For things like boundaries, doors, things you cannot pass through
export function getColliderBoxComponents(k, width, height, pos, tag) {
    return [
        k.area({shape: new k.Rect(k.vec2(0), width, height)}),
        k.pos(pos),
        k.body({isStatic: true}),
        k.offscreen(),
        tag
    ]
}

export function drawBoundaries(k, map, layer) {
    for (const object of layer.objects) {
        map.add(getColliderBoxComponents(k, object.width, object.height, k.vec2(object.x, object.y), object.name));
    }
}

export async function blinkEffect(k, entity) {
    await k.tween(entity.opacity, 0, 0.1, (val) => (entity.opacity = val), k.easings.linear);
    await k.tween(entity.opacity, 1, 0.1, (val) => (entity.opacity = val), k.easings.linear);
}

// entity is an enemy entity
export function onAttacked(k, entity, player) {
    /*
    entity.onCollide("swordHitBox", async () => {
        if (entity.isAttacking) return;

        await blinkEffect(k, entity);
        entity.hurt(player.attackPower);

        if (entity.hp() <= 0) {
            k.destroy(entity);
            return;
        }
    });
    */

    entity.onCollide("projectile", async () => {
        if (entity.isAttacking) return;

        await blinkEffect(k, entity);
        entity.hurt(player.attackPower);

        if (entity.hp() <= 0) {
            k.destroy(entity);
            return;
        }
    })
}

export function onCollideWithPlayer(k, entity) {
    entity.onCollide("player", async (player) => {
        if (player.isAttacking) return;

        playerState.setHealth(playerState.getHealth() - entity.attackPower);
        k.destroyAll("healthContainer");
        healthBar(k, player);
        await blinkEffect(k, player);

        if (playerState.getHealth() <= 0) {
            gameState.setPreviousScene("house");
            k.go("world");

            gameState.setHasRespawned(true);
            playerState.setHealth(playerState.getMaxHealth());
            playerState.setIsSwordEquipped(false);
        }
    });
}