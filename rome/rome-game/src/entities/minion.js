import { playAnimIfNotPlaying } from "../utils.js";

const directionStates = ["left", "right", "up", "down"];

export function generateSlimeComponents(k, pos) {
    return [
      k.sprite("minion", {
        anim: "minion-idle",
      }),
      k.area({ shape: new k.Rect(k.vec2(0, 6), 16, 10) }),
      k.body(),
      k.pos(pos),
      k.offscreen(),
      k.opacity(),
      k.state("idle", ["idle", ...directionStates]),
      k.health(3),
      {
          speed: 30,
          attackPower: 0.5,
      },
      "slime"
    ];
  }

  const pickRandomDirection = () => {
    return directionStates[Math.floor(Math.random() * directionStates.length)];
  }
  
  export function setSlimeAI(k, slime) {
    k.onUpdate(() => {
      switch (slime.state) {
        case "idle":
          break;
        case "right":
          slime.move(slime.speed, 0);
          break;
        case "left":
          slime.move(-slime.speed, 0);
          break;
        case "up":
          slime.move(0, -slime.speed);
          break;
        case "down":
          slime.move(0, slime.speed);
          break;
      }
    });

    const idle = slime.onStateEnter("idle", async () => {
      slime.stop();
      await k.wait(3);

      slime.enterState(pickRandomDirection())
    });

    const right = slime.onStateEnter("right", async () => {
      slime.flipX = false;
      playAnimIfNotPlaying(slime, "minion-side");
      await k.wait(3);

      slime.enterState("idle");
    });

    const left = slime.onStateEnter("left", async () => {
      slime.flipX = true;
      playAnimIfNotPlaying(slime, "minion-side");
      await k.wait(3);

      slime.enterState("idle");
    });

    const up = slime.onStateEnter("up", async () => {
      playAnimIfNotPlaying(slime, "minion-up");
      await k.wait(3);

      slime.enterState("idle");
    });

    const down = slime.onStateEnter("down", async () => {
      playAnimIfNotPlaying(slime, "minion-down");
      await k.wait(3);

      slime.enterState("idle");
    });

    k.onSceneLeave(() => {
      idle.cancel();
      right.cancel();
      left.cancel();
      up.cancel();
      down.cancel();
    });
  }