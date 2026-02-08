import math
import random

import pygame
from pygame import Surface
from pygame.math import Vector2

from entities.obstacle.geometric import GeometricObstacle


# Single particle spawned from a destroyed geometric obstacle
class DisintegrationParticle:
    __slots__ = ("pos", "vel", "life", "maxLife", "radius", "color", "angVel")

    def __init__(self, pos: Vector2, vel: Vector2, life: float,
                 radius: float, color: tuple[int, int, int], angVel: float) -> None:
        self.pos = pos.copy()
        self.vel = vel
        self.life = life
        self.maxLife = life
        self.radius = radius
        self.color = color
        self.angVel = angVel  # spiral rotation speed

    def update(self, dt: float) -> bool:
        # scaled by angVel
        tangent = Vector2(-self.vel.y, self.vel.x)
        if tangent.length_squared() > 0.01:
            tangent = tangent.normalize() * self.angVel
        self.vel += tangent * dt
        self.pos += self.vel * dt
        self.vel *= 0.96 ** (dt * 60)  # air drag
        self.vel.y += 40.0 * dt  # light gravity pull
        self.life -= dt
        return self.life > 0


class DisintegrationEffect:
    gridStep: int = 8  # pixel sampling interval
    maxParticles: int = 120

    def __init__(self, obstacle: GeometricObstacle) -> None:
        self.particles: list[DisintegrationParticle] = []
        self._sample(obstacle)

    def _sample(self, obs: GeometricObstacle) -> None:
        # Rotate sprite so it can match the obstacle angle
        rotated = pygame.transform.rotate(obs.image, obs.rotation)
        rw, rh = rotated.get_size()
        cx, cy = obs.rect.center
        ox, oy = cx - rw // 2, cy - rh // 2  # = top left on the screen
        size = max(rw, rh) / 2

        candidates: list[DisintegrationParticle] = []
        for gx in range(0, rw, self.gridStep):
            for gy in range(0, rh, self.gridStep):
                c = rotated.get_at((gx, gy))
                if c.a < 10:
                    continue

                worldPos = Vector2(ox + gx, oy + gy)
                offset = worldPos - Vector2(cx, cy)
                dist = offset.length()

                if dist > 0.1:
                    direction = offset.normalize()
                else:
                    direction = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()

                # Particles from the center are faster, it's giving a explosion feel
                baseSpeed = 120.0 + 180.0 * min(dist / max(size, 1), 1.0)
                vel = direction * baseSpeed * random.uniform(0.7, 1.3)
                
                angle = math.atan2(offset.y, offset.x)
                angVel = 3.0 * math.sin(angle * 3)
                life = random.uniform(0.5, 0.8)
                radius = random.uniform(2.5, 4.5)

                candidates.append(DisintegrationParticle(
                    worldPos, vel, life, radius, (c.r, c.g, c.b), angVel
                ))

        if len(candidates) > self.maxParticles:
            self.particles = random.sample(candidates, self.maxParticles)
        else:
            self.particles = candidates

    def update(self, dt: float) -> None:
        self.particles = [p for p in self.particles if p.update(dt)]

    @property
    def bDone(self) -> bool:
        return not self.particles

    def draw(self, screen: Surface) -> None:
        for p in self.particles:
            frac = p.life / p.maxLife  # 1.0 = just spawned, 0.0 = going to die
            alpha = int(255 * (frac ** 0.6))  # fade out
            r = max(1, int(p.radius * (0.3 + 0.7 * frac)))  # shrink over time

            # flash effect
            w = min(1.0, (1.0 - frac) * 0.5)
            rc = int(p.color[0] + (255 - p.color[0]) * w)
            gc = int(p.color[1] + (255 - p.color[1]) * w)
            bc = int(p.color[2] + (255 - p.color[2]) * w)

            ix, iy = int(p.pos.x), int(p.pos.y)

            # Drawing a small glow effect behind the particle
            if r >= 3:
                gr = r * 2
                gSurf = Surface((gr * 2, gr * 2), pygame.SRCALPHA)
                pygame.draw.circle(gSurf, (rc, gc, bc, max(1, alpha // 4)), (gr, gr), gr)
                screen.blit(gSurf, (ix - gr, iy - gr))

            # Our particle here
            if r <= 1:
                screen.set_at((ix, iy), (rc, gc, bc, alpha))
            else:
                pSurf = Surface((r * 2, r * 2), pygame.SRCALPHA)
                pygame.draw.circle(pSurf, (rc, gc, bc, alpha), (r, r), r)
                screen.blit(pSurf, (ix - r, iy - r))
