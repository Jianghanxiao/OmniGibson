from omnigibson.utils.constants import PrimType
from omnigibson.object_states import Folded, Unfolded
from omnigibson.macros import gm
import numpy as np

import omnigibson as og
import json

# Make sure object states and GPU dynamics are enabled (GPU dynamics needed for cloth)
gm.ENABLE_OBJECT_STATES = True
gm.USE_GPU_DYNAMICS = True


def main(random_selection=False, headless=False, short_exec=False):
    """
    Demo of cloth objects that can potentially be folded.
    """
    og.log.info(f"Demo {__file__}\n    " + "*" * 80 + "\n    Description:\n" + main.__doc__ + "*" * 80)

    # Read the json file
    with open("/home/hanxiao/Desktop/Research/behavior/OmniGibson/cloth_models.json") as f:
        cloth_objects = json.load(f)

    for cloth in cloth_objects:
        category = cloth["category"]
        model = cloth["model"]
        if model != "sehjcp":
             continue
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
                },
            ],
        }

        # Create the environment
        env = og.Environment(configs=cfg)

        # Grab object references
        carpet = env.scene.object_registry("name", model)
        objs = [carpet]

        # Set viewer camera
        og.sim.viewer_camera.set_position_orientation(
            position=np.array([0.46382895, -2.66703958, 1.22616824]),
            orientation=np.array([0.58779174, -0.00231237, -0.00318273, 0.80900271]),
        )

        for _ in range(100):
            og.sim.step()

        print("\nCloth state:\n")

        if not short_exec:
            obj = objs[0]
            pos = obj.root_link.compute_particle_positions()
            x_min = np.min(pos[:, 0])
            x_max = np.max(pos[:, 0])
            x_mid = (x_min + x_max) / 2
            indices = np.argsort(pos, axis=0)[:, 0][-len(pos)//2:]
            start = np.copy(pos[indices])
            end = np.copy(start)
            end[:, 0] = 2*x_mid - end[:, 0]

            increments = 100
            for ctrl_pts in np.linspace(start, end, increments):
                    obj.root_link.set_particle_positions(ctrl_pts, idxs=indices)
                    og.sim.step()


            pos = obj.root_link.compute_particle_positions()
            y_min = np.min(pos[:, 1])
            y_max = np.max(pos[:, 1])
            y_mid = (y_min + y_max) / 2
            indices = np.argsort(pos, axis=0)[:, 1][-len(pos)//2:]
            start = np.copy(pos[indices])
            end = np.copy(start)
            end[:, 1] = 2*y_mid - end[:, 1]

            increments = 100
            for ctrl_pts in np.linspace(start, end, increments):
                    obj.root_link.set_particle_positions(ctrl_pts, idxs=indices)
                    og.sim.step()

            while True:
                print(f"\nCategory: {category}, Model: {model}!!!!!!!!!!!!!!!!!!!!!!!!!!")
                # obj.root_link.set_particle_positions(end, idxs=indices)
                env.step(np.array([]))

        # Shut down env at the end
        print()
        env.close()


if __name__ == "__main__":
    main()
