import k from "./kaboomContext.js";
import world from "./scenes/world.js";
import house from "./scenes/house.js";
import dungeon from "./scenes/dungeon.js";

import minionImage from "../assets/minion.png";
import bossImage from "../assets/boss.png";
import projectileImage from "../assets/projectile.png";
import spriteSheet from "../assets/topdownasset.png";

k.loadSprite("minion", minionImage, {
  sliceX: 1,
  sliceY: 1,
  anims: {
    "minion-idle": 0,
    "minion-side": 0,
    "minion-up": 0,
    "minion-down": 0,
  }
});

k.loadSprite("boss", bossImage, {
  sliceX: 1,
  sliceY: 1,
  anims: {
    "boss-down": 0
  }
});

k.loadSprite("projectile", projectileImage, {
  sliceX: 1,
  sliceY: 1,
  anims: {
    "projectile-air": 0
  }
});

k.loadSprite("assets", spriteSheet, {
  sliceX: 39, // there are 39 columns in the sprite sheet
  sliceY: 31, // there are 31 rows in the sprite sheet
  anims: {
    "player-idle-down": 936,
    "player-down": {
      from: 936,
      to: 939,
      loop: true,
    },
    "player-idle-side": 976,
    "player-side": {
      from: 976,
      to: 978,
      loop: true,
    },
    "player-idle-up": 1014,
    "player-up": {
      from: 1014,
      to: 1017,
      loop: true,
    },
    // "slime-idle-down": 858,
    // "slime-down": { from: 858, to: 859, loop: true },
    // "slime-idle-side": 860,
    // "slime-side": { from: 860, to: 861, loop: true },
    // "slime-idle-up": 897,
    // "slime-up": { from: 897, to: 898, loop: true },
    "oldman-down": 866,
    "oldman-side": 907,
    "oldman-up": 905,
    "player-attack-up": 1094,
    "player-attack-down": 1092,
    "player-attack-left": 1093,
    "player-attack-right": 1093,
    // "ghost-down": { from: 862, to: 863, loop: true },
    "tombstone": 393,
  },
});
k.loadSpriteAtlas(spriteSheet, {
  "full-heart": {
    x: 0,
    y: 224,
    width: 48,
    height: 48,
  },
  "half-heart": {
    x: 48,
    y: 224,
    width: 48,
    height: 48,
  },
  "empty-heart": {
    x: 96,
    y: 224,
    width: 48,
    height: 48,
  },
});

const scenes = {
  world,
  house,
  dungeon
};

const entities = {
  player: null,
  slimes: [],
  ghost: null,
  oldMan: null,
  projectile: []
};

for (const sceneName in scenes) {
  k.scene(sceneName, () => scenes[sceneName](k, entities));
}

k.go("world");
