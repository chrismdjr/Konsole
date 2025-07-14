#!/usr/bin/env python3

from klib import konsole_controller
from klib import konsole_renderer

import time
import random

TARGET_FRAMERATE = 60

renderer = konsole_renderer.Renderer()

class Particle:
    def __init__(self):
        self.x = 32
        self.y = 32
        self.velocity = (
            random.uniform(-2, 2),
            random.uniform(-2, 2)
        )
        self.size = 10
        self.init_health = 100
        self.health = self.init_health
        self.color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

particles = []
ticks_per_spawn = 1
ticks_until_next_spawn = 0

delta_time = 0
while True:
    frame_start_time = time.time()

    renderer.clear()

    ticks_until_next_spawn -= 1
    if ticks_until_next_spawn <= 0:
        ticks_until_next_spawn = ticks_per_spawn
        particles.append(Particle())

    for particle in particles:
        particle.health -= 1

        if particle.health <= 0:
            particles.remove(particle)
            continue

        particle.size = (particle.health / particle.init_health) * particle.size

        particle.x += particle.velocity[0]
        particle.y += particle.velocity[1]

        renderer.draw_ellipse(
            particle.x - particle.size / 2,
            particle.y - particle.size / 2,
            particle.size,
            particle.size,
            particle.color
        )

    renderer.present()

    # calculate delta time
    delta_time = time.time() - frame_start_time
    time_to_sleep = max(1 / TARGET_FRAMERATE - delta_time, 0)
    time.sleep(time_to_sleep)
    delta_time += time_to_sleep