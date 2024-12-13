from omnigibson.utils.constants import PrimType
from omnigibson.object_states import Folded, Unfolded
from omnigibson.macros import gm
import numpy as np

import omnigibson as og
import omnigibson.lazy as lazy
import json
import torch
import time
# Make sure object states and GPU dynamics are enabled (GPU dynamics needed for cloth)
gm.ENABLE_OBJECT_STATES = True
gm.USE_GPU_DYNAMICS = True



def main(random_selection=False, headless=False, short_exec=False):
    """
    Demo of cloth objects that can potentially be folded.
    """
    og.log.info(f"Demo {__file__}\n    " + "*" * 80 + "\n    Description:\n" + main.__doc__ + "*" * 80)

    # Read the json file
    with open("./cloth_models.json") as f:
        cloth_objects = json.load(f)

    # generate_box()

    for cloth in cloth_objects:
        category = cloth["category"]
        model = cloth["model"]
        if model != "sehjcp":
             continue
        # if model != "agftpm":
        #      continue
        print(f"\nCategory: {category}, Model: {model}!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # Create the scene config to load -- empty scene + custom cloth object
        cfg = {
            "scene": {
                "type": "Scene",
            },
            "objects": [
                {
                    "type": "DatasetObject",
                    "name": model,
                    "category": category,
                    "model": model,
                    # "bounding_box": [0.897, 0.568, 0.012],
                    "prim_type": PrimType.CLOTH,
                    "abilities": {"cloth": {}},
                    # "position": [0, 0, 0.5],
                    # "orientation": [0.7071, 0., 0.7071, 0.],
                },
            ],
        }

        # Create the environment
        env = og.Environment(configs=cfg)

        # Grab object references
        carpet = env.scene.object_registry("name", model)
        objs = [carpet]
        plane_prims = env.scene.plane_prims
        plane_motions = env.scene.plane_motions

        # Set viewer camera
        og.sim.viewer_camera.set_position_orientation(
            position=np.array([0.46382895, -2.66703958, 1.22616824]),
            orientation=np.array([0.58779174, -0.00231237, -0.00318273, 0.80900271]),
        )

        for _ in range(100):
            og.sim.step()

        print("\nCloth state:\n")

        if not short_exec:
            # Calculate end positions for all walls
            end_positions = []
            for i in range(4):
                plane_prim = plane_prims[i]
                position = plane_prim.get_position()
                end_positions.append(np.array(position) + 0.9 * np.array(plane_motions[i]))

            increments = 1000
            for step in range(increments):
                # Move all walls a small amount
                for i in range(4):
                    plane_prim = plane_prims[i]
                    current_pos = np.linspace(plane_prim.get_position(), end_positions[i], increments)[step]
                    plane_prim.set_position(current_pos)
                
                og.sim.step()

                # Check cloth height
                cloth_positions = objs[0].root_link.compute_particle_positions()
                max_height = np.max(cloth_positions[:, 2])
                
                # Get distance between facing walls (assuming walls 0-2 and 1-3 are facing pairs)
                wall_dist_1 = np.linalg.norm(plane_prims[0].get_position() - plane_prims[2].get_position())
                wall_dist_2 = np.linalg.norm(plane_prims[1].get_position() - plane_prims[3].get_position())
                min_wall_dist = min(wall_dist_1, wall_dist_2)

                # Stop if cloth height exceeds wall distance
                if max_height > min_wall_dist:
                    print(f"Stopping: Cloth height ({max_height:.3f}) exceeds wall distance ({min_wall_dist:.3f})")
                    break


        # Shut down env at the end
        print()
        env.close()


if __name__ == "__main__":
    main()