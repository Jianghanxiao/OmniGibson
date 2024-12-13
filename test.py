import trimesh
import numpy as np
import open3d as o3d

# mesh = trimesh.load_mesh('test_origin.obj')
# color = np.array([0, 0, 255, 255], dtype=np.uint8)

# mesh_2 = trimesh.load_mesh('after.obj')
# color = np.array([255, 0, 0, 255], dtype=np.uint8)

# import pdb
# pdb.set_trace()
# mesh += mesh_2

# # Visualize both meshes
# mesh.show()

# mesh = trimesh.load_mesh('test_squeeze.obj', process=False)
# print(len(mesh.vertices))

# # Enable double-sided rendering by modifying the visual properties
# mesh.visual.face_colors = [200, 200, 200, 255]  # Set a color with full opacity
# mesh.visual.material = trimesh.visual.material.SimpleMaterial(image=None, double_sided=True)

# mesh.show()

o3d_mesh = o3d.io.read_triangle_mesh('test_squeeze.obj')
# Makeeach face double-sided
o3d_mesh.compute_vertex_normals()
o3d_mesh.compute_triangle_normals()

print(len(o3d_mesh.vertices))
o3d.visualization.draw_geometries([o3d_mesh])