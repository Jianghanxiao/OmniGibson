from omnigibson.objects import USDObject
import omnigibson as og
from omnigibson.utils.constants import PrimType
from omnigibson.macros import gm
# Make sure object states and GPU dynamics are enabled (GPU dynamics needed for cloth)
gm.ENABLE_OBJECT_STATES = True
gm.USE_GPU_DYNAMICS = True



cfg = {
            "scene": {
                "type": "Scene",
            },
            "objects": [
                {
                    "type": "USDObject", # (2)!
                    "name": "test_pant", # (3)!
                    "usd_path": f"/home/hanxiao/Downloads/SL_Skirt194-20241213T184516Z-001/SL_Skirt194/SL_Skirt194_obj.usd",
                    "category": "pant", # (4)!
                    # "visual_only": True, # (5)!
                    "prim_type": PrimType.CLOTH,
                    # "scale": [1/10, 1/10, 1/10], # (6)!
                    # "position": [1.0, 2.0, 0.001], # (7)!
                    # "orientation": [0, 0, 0, 1.0], # (8)!
                }
            ],
        }

# # Create the environment
env = og.Environment(configs=cfg)

while True:
    og.sim.step()