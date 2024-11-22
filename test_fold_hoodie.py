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
        if model != "agftpm":
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
                    "orientation": [0.7071, 0., 0.7071, 0.],
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
            # Deal with x
            # obj = objs[0]
            # pos = obj.root_link.compute_particle_positions()
            # x_min = np.min(pos[:, 0])
            # x_max = np.max(pos[:, 0])
            # x_mid = (x_min + x_max) / 2
            # indices = np.argsort(pos, axis=0)[:, 0][-len(pos)//2:]
            # start = np.copy(pos[indices])
            # end = np.copy(start)
            # end[:, 0] = 2*x_mid - end[:, 0]

            # increments = 100
            # for ctrl_pts in np.linspace(start, end, increments):
            #     obj.root_link.set_particle_positions(ctrl_pts, idxs=indices)
            #     og.sim.step()
            
            
            # Get particle positions
            # obj = objs[0]
            # pos = obj.root_link.compute_particle_positions()

            # # Calculate x-coordinate boundaries and midpoints
            # x_min = np.min(pos[:, 0])
            # x_max = np.max(pos[:, 0])
            # x_mid_left = x_min + (x_max - x_min) / 3
            # x_mid_right = x_min + 2 * (x_max - x_min) / 3

            # # Indices for left, middle, and right thirds
            # left_indices = np.where(pos[:, 0] < x_mid_left)[0]
            # right_indices = np.where(pos[:, 0] > x_mid_right)[0]

            # # Fold the left third towards the middle
            # left_start = np.copy(pos[left_indices])
            # left_end = np.copy(left_start)
            # left_end[:, 0] = 2 * x_mid_left - left_end[:, 0]  # Mirror left to the right of x_mid_left

            # # Perform the left fold
            # increments = 100
            # for ctrl_pts in np.linspace(left_start, left_end, increments):
            #     obj.root_link.set_particle_positions(ctrl_pts, idxs=left_indices)
            #     og.sim.step()

            # # Fold the right third towards the middle
            # right_start = np.copy(pos[right_indices])
            # right_end = np.copy(right_start)
            # right_end[:, 0] = 2 * x_mid_right - right_end[:, 0]  # Mirror right to the left of x_mid_right

            # # Perform the right fold
            # for ctrl_pts in np.linspace(right_start, right_end, increments):
            #     obj.root_link.set_particle_positions(ctrl_pts, idxs=right_indices)
            #     og.sim.step()
            
            
            # Get particle positions
            obj = objs[0]
            pos = obj.root_link.compute_particle_positions()

            # Calculate y-coordinate boundaries and midpoints
            y_min = np.min(pos[:, 1])
            y_max = np.max(pos[:, 1])
            y_mid_bottom = y_min + (y_max - y_min) / 3
            y_mid_top = y_min + 2 * (y_max - y_min) / 3

            # Indices for bottom, middle, and top thirds
            bottom_indices = np.where(pos[:, 1] < y_mid_bottom)[0]
            top_indices = np.where(pos[:, 1] > y_mid_top)[0]

            # Fold the bottom third towards the middle
            bottom_start = np.copy(pos[bottom_indices])
            bottom_end = np.copy(bottom_start)
            bottom_end[:, 1] = 2 * y_mid_bottom - bottom_end[:, 1]  # Mirror bottom to the above of y_mid_bottom

            # Perform the bottom fold
            increments = 1000
            for ctrl_pts in np.linspace(bottom_start, bottom_end, increments):
                obj.root_link.set_particle_positions(ctrl_pts, idxs=bottom_indices)
                og.sim.step()

            # Fold the top third towards the middle
            top_start = np.copy(pos[top_indices])
            top_end = np.copy(top_start)
            top_end[:, 1] = 2 * y_mid_top - top_end[:, 1]  # Mirror top to the below of y_mid_top

            # Perform the top fold
            for ctrl_pts in np.linspace(top_start, top_end, increments):
                obj.root_link.set_particle_positions(ctrl_pts, idxs=top_indices)
                og.sim.step()



            # pos = obj.root_link.compute_particle_positions()
            # indices = np.argsort(pos, axis=0)[:, 0][:-int(len(pos)/5*4)]
            # start = np.copy(pos[indices])
            # for i in range(30):
            #     obj.root_link.set_particle_positions(start, idxs=indices)
            #     og.sim.step()
            

            # Deal with y
            # pos = obj.root_link.compute_particle_positions()
            # y_min = np.min(pos[:, 1])
            # y_max = np.max(pos[:, 1])
            # y_mid = (y_min + y_max) / 2
            # indices = np.argsort(pos, axis=0)[:, 1][-len(pos)//2:]
            # start = np.copy(pos[indices])
            # end = np.copy(start)
            # end[:, 1] = 2*y_mid - end[:, 1]

            # increments = 100
            # for ctrl_pts in np.linspace(start, end, increments):
            #     obj.root_link.set_particle_positions(ctrl_pts, idxs=indices)
            #     og.sim.step()
            
            # Get particle positions
            pos = obj.root_link.compute_particle_positions()

            # Calculate x-coordinate boundaries and midpoint
            x_min = np.min(pos[:, 0])
            x_max = np.max(pos[:, 0])
            x_mid = (x_min + x_max) / 2

            # Select indices of the right half of the particles
            indices = np.argsort(pos, axis=0)[:, 0][-len(pos) // 2:]

            # Define the start and end positions for folding
            start = np.copy(pos[indices])
            end = np.copy(start)
            end[:, 0] = 2 * x_mid - end[:, 0]  # Mirror positions along the x-axis

            # Perform the folding operation in increments
            increments = 1000
            for ctrl_pts in np.linspace(start, end, increments):
                obj.root_link.set_particle_positions(ctrl_pts, idxs=indices)
                og.sim.step()


            # pos = obj.root_link.compute_particle_positions()
            # indices = np.argsort(pos, axis=0)[:, 1][:-int(len(pos)/5*4)]
            # start = np.copy(pos[indices])
            # for i in range(30):
            #     obj.root_link.set_particle_positions(start, idxs=indices)
            #     og.sim.step()


            while True:
                print(f"\nCategory: {category}, Model: {model}!!!!!!!!!!!!!!!!!!!!!!!!!!")
                # obj.root_link.set_particle_positions(end, idxs=indices)
                env.step(np.array([]))

        # Shut down env at the end
        print()
        env.close()


if __name__ == "__main__":
    main()
