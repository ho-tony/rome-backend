const directionStates = ["left", "right", "up", "down"];

export function generateProjectileComponents(k, pos, direction) {
    console.log("generating projectile")
    const projectileHitBoxPosX = {
        left: pos.x,
        right: pos.x,
        up: pos.x,
        down: pos.x + 16,
    };

    const projectileHitBoxPosY = {
        left: pos.y,
        right: pos.y,
        up: pos.y,
        down: pos.y + 12,
    };

    return [
      k.sprite("projectile", {
        anim: "projectile-air",
      }),
      k.area({ shape: new k.Rect(k.vec2(0), 16, 16) }),
      k.body(),
      k.pos(projectileHitBoxPosX[direction], projectileHitBoxPosY[direction]),
      k.offscreen(),
      k.opacity(),
      k.rotate(0),
      k.state(direction, directionStates),
      k.health(3),
      {
          speed: 200,
          attackPower: 0.5,
          direction,
      },
      "projectile"
    ];
}
  
export async function startProjectile(k, projectile) {
    console.log("starting projectile");
    k.onUpdate(() => {
        if (!projectile) return;

        switch (projectile.state) {
        case "right":
            console.log("projectile right", projectile);
            projectile.move(projectile.speed, 0);
            break;
        case "left":
            console.log("projectile left", projectile);
            projectile.flipX = true;
            projectile.move(-projectile.speed, 0);
            break;
        case "up":
            console.log("projectile up", projectile);
            projectile.angle = 270;
            projectile.move(0, -projectile.speed);
            break;
        case "down":
            console.log("projectile down", projectile);
            projectile.angle = 90;
            projectile.move(0, projectile.speed);
            break;
        }
    });

    setTimeout(() => {
        projectile.onCollide((ignored) => {
            console.log({projectile, ignored});
            if (projectile.exists()) {
                k.destroy(projectile);
              }
        });
    }, 5);
}