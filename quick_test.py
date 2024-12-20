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
                    "scale": [1/100, 1/100, 1/100],
                    # "abilities": {"cloth": {}},
                    # "position": [0, 0, 0.5],
                    # "orientation": [0.7071, 0., 0.7071, 0.],
                },
            ],
        }

        # Create the environment
        env = og.Environment(configs=cfg)

        while True:
            og.sim.step()

if __name__ == "__main__":
    main()
