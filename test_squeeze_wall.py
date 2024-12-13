from omnigibson.utils.constants import PrimType
from omnigibson.object_states import Folded, Unfolded
from omnigibson.macros import gm
import numpy as np

import omnigibson as og
import omnigibson.lazy as lazy
import json
import torch
import time
import trimesh 
from scipy.spatial import cKDTree
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
            for i in range(4):
                plane_prim = plane_prims[i]
                plane_motion = plane_motions[i]
                position = plane_prim.get_position()
  
                end_position = np.array(position) + 0.9 * np.array(plane_motion)

                increments = 10
                for ctrl_pts in np.linspace(position, end_position, increments):
                    plane_prim.set_position(ctrl_pts)
                    og.sim.step()

            # # Deal with x
            # obj = objs[0]
            # pos = obj.root_link.compute_particle_positions()
            # x_min = np.min(pos[:, 0])
            # x_max = np.max(pos[:, 0])
            # x_mid = (x_min + x_max) / 2
            # y_min = np.min(pos[:, 1])
            # y_max = np.max(pos[:, 1])
            # y_mid = (y_min + y_max) / 2
            # z_min = np.min(pos[:, 2])
            # start = np.copy(pos)
            # end = np.copy(start)
            # end[:, 0] = (end[:, 0] - x_mid) / 10 + x_mid 
            # end[:, 1] = (end[:, 1] - y_mid) / 10 + y_mid 
            # end[:, 2] = (end[:, 2] - z_min) / 10 + z_min

            # increments = 100
            # for ctrl_pts in np.linspace(start, end, increments):
            #     obj.root_link.set_particle_positions(ctrl_pts)
            #     og.sim.step()


            # while True:
            for i in range(100):
                # print(f"\nCategory: {category}, Model: {model}!!!!!!!!!!!!!!!!!!!!!!!!!!")
                # obj.root_link.set_particle_positions(end)
                
                env.step(np.array([]))

        obj = objs[0]
        pos = obj.root_link.compute_particle_positions()


        old_mesh = trimesh.load_mesh("test_origin.obj")
        new_initial = trimesh.load_mesh("after.obj")

        old_vertices = np.asarray(old_mesh.vertices)
        new_vertices = np.asarray(new_initial.vertices)

        # Get the correspondence between these two, for each vertice in old_mesh find the neightbours in new_initial, and save the weight
        # Then leverage the saved neightbour index and weigth to get the new postion from current pos
        # Build a KD-Tree for the new vertices
        tree = cKDTree(new_vertices)

        # Number of nearest neighbors
        k = 10

        # Find k nearest neighbors for each vertex in old_mesh
        distances, indices = tree.query(old_vertices, k=k)

        # Calculate weights based on inverse distances
        weights = 1 / (distances + 1e-8)  # Adding a small value to avoid division by zero
        weights /= weights.sum(axis=1, keepdims=True)

        # Initialize array for new positions
        new_positions = np.zeros_like(old_vertices)

        # Interpolate new positions using the neighbors and weights
        for i in range(old_vertices.shape[0]):
            new_positions[i] = np.dot(weights[i], pos[indices[i]])

        # Change the vertice position of the old mesh
        old_mesh.vertices = new_positions

        import pdb
        pdb.set_trace()
        
        old_mesh.export("test_squeeze.obj")
        # Shut down env at the end
        print()
        env.close()


if __name__ == "__main__":
    main()
