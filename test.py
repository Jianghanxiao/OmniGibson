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


# {
#     "bandana": {"wbhliu"},
#     "curtain": {"ohvomi"},
#     "cardigan": {"itrkhr"},
#     "sweatshirt": {"nowqqh"},
#     "jeans": {"nmvvil", "pvzxyp"},
#     "pajamas": {"rcgdde"},
#     "polo_shirt": {"vqbvph"},
#     "vest": {"girtqm"}, # bddl NOT FIXED
#     "onesie": {"pbytey"},
#     "dishtowel": {"ltydgg"},
#     "dress": {"gtghon"},
#     "hammock": {'aiftuk', 'fglfga', 'klhkgd', 'lqweda', 'qewdqa'},
#     'jacket': {'kiiium', 'nogevo', 'remcyk'},
#     "quilt": {"mksdlu", "prhems"},
#     "pennant": {"tfnwti"},
#     "pillowcase": {"dtoahb", "yakvci"},
#     "rubber_glove": {"leuiso"},
#     "scarf": {"kclcrj"},
#     "sock": {"vpafgj"},
#     "tank_top": {"fzldgi"},
#     "curtain": {"shbakk"}
# }


# cloth_category_models = [
#     ("bandana", "wbhliu"),
# ]

# cloth_category_models = [
#     ("curtain", "ohvomi"),
# ]

# cloth_category_models = [
#     ("cardigan", "itrkhr"),
# ]

# cloth_category_models = [
#     ("sweatshirt", "nowqqh"),
# ]

# cloth_category_models = [
#     ("jeans", "nmvvil"),
#     ("jeans", "pvzxyp"),
# ]

# cloth_category_models = [
#     ("pajamas", "rcgdde"),
# ]

cloth_category_models = [
    ("polo_shirt", "vqbvph"),
]

# cloth_category_models = [
#     ("vest", "girtqm"),
# ]

# cloth_category_models = [
#     ("onesie", "pbytey"),
# ]

# cloth_category_models = [
#     ("dishtowel", "ltydgg"),
# ]

# cloth_category_models = [
#     ("dress", "gtghon"),
# ]

# cloth_category_models = [
#     ("hammock", "aiftuk"),
#     ("hammock", "fglfga"),
#     ("hammock", "klhkgd"),
#     ("hammock", "lqweda"),
#     ("hammock", "qewdqa"),
# ]

# cloth_category_models = [
#     ("jacket", "kiiium"),
#     ("jacket", "nogevo"),
#     ("jacket", "remcyk"),
# ]

# cloth_category_models = [
#     ("quilt", "mksdlu"),
#     ("quilt", "prhems"),
# ]

# cloth_category_models = [
#     ("pennant", "tfnwti"),
# ]

# cloth_category_models = [
#     ("pillowcase", "dtoahb"),
#     ("pillowcase", "yakvci"),
# ]

# cloth_category_models = [
#     ("rubber_glove", "leuiso"),
# ]

# cloth_category_models = [
#     ("scarf", "kclcrj"),
# ]

# cloth_category_models = [
#     ("sock", "vpafgj"),
# ]

# cloth_category_models = [
#     ("tank_top", "fzldgi"),
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
    # obj = DatasetObject(name="obj", category=category, model=model, prim_type=PrimType.RIGID)
    # obj = DatasetObject(name="obj", category=category, model=model, prim_type=PrimType.RIGID, scale=0.5)
    env.scene.add_object(obj)
    obj.set_position([-obj.aabb_center[0], -obj.aabb_center[1], -obj.aabb_center[2] + obj.aabb_extent[2] / 2.0])
    print(f"Simulating {category} {model}...")
    # pdb.set_trace()
    og.sim.play()
    # for _ in range(1000):
    while True:
        og.sim.step()

    og.sim.stop()
    og.sim.remove_object(obj)