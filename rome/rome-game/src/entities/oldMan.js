export function generateOldManComponents(k, pos) {
    return [
        k.sprite("assets", {
          anim: "oldman-down",
        }),
        k.area({ shape: new k.Rect(k.vec2(2, 4), 12, 12) }),
        k.body({ isStatic: true }),
        k.pos(pos),
        {},
        "oldMan"
      ];
}