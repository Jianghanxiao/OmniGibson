import omnigibson as og
from omnigibson.macros import gm
from omnigibson.objects.dataset_object import DatasetObject
from omnigibson.utils.constants import PrimType
from omnigibson.utils.bddl_utils import OBJECT_TAXONOMY
from omnigibson.utils.asset_utils import get_all_object_categories, get_all_object_category_models
import pdb

gm.USE_GPU_DYNAMICS = True
all_categories = get_all_object_categories()

cloth_category_models = []
for category in all_categories:
    if OBJECT_TAXONOMY.has_ability(OBJECT_TAXONOMY.get_synset_from_category(category), "cloth"):
        for model in get_all_object_category_models(category):
            cloth_category_models.append((category, model))

# cloth_category_models = [
#     ("carpet", "ctclvd"),
# ]

cloth_category_models = [
    ("bandana", "wbhliu"),
]

# cloth_category_models = [
#     ("apron", "uxgjdv"),
# ]


cfg = {
    "scene": {
        "type": "Scene",
    },
}

env = og.Environment(cfg)

og.sim.stop()

for category, model in cloth_category_models:
    obj = DatasetObject(name="obj", category=category, model=model, prim_type=PrimType.CLOTH, load_config={"remesh": True}, scale=0.5)
    # obj = DatasetObject(name="obj", category=category, model=model, prim_type=PrimType.RIGID, scale=0.5)
    env.scene.add_object(obj)
    obj.set_position([-obj.aabb_center[0], -obj.aabb_center[1], -obj.aabb_center[2] + obj.aabb_extent[2] / 2.0])
    print(f"Simulating {category} {model}...")
    # pdb.set_trace()
    og.sim.play()
    for _ in range(1000):
        og.sim.step()

    og.sim.stop()
    og.sim.remove_object(obj)