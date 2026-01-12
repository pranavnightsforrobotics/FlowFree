import open3d as o3d
import numpy as np
from scipy.spatial.transform import Rotation as R_scipy

def create_custom_triangular_prism(sideLen: float,  height: float, center: np.ndarray,  xFlip: bool = True) -> o3d.geometry.TriangleMesh:
  # --- 1. Define Vertices for a standard prism centered at (0, 0, 0) ---
  
  # Coordinates for an equilateral triangle base centered at (0, 0, 0) in the XY plane.
  h = np.sqrt(3) / 2 * sideLen  # Height of the equilateral triangle
  
  # Define base vertices (Z = -height/2)
  v0Bot = np.array([sideLen / 2, -h / 3, -height / 2])
  v1Bot = np.array([-sideLen / 2, -h / 3, -height / 2])
  v2Bot = np.array([0.0, 2 * h / 3, -height / 2])

  # Define top vertices (Z = +height/2)
  v0Top = v0Bot + np.array([0.0, 0.0, height / 2])
  v1Top = v1Bot + np.array([0.0, 0.0, height / 2])
  v2Top = v2Bot + np.array([0.0, 0.0, height / 2])
  
  vertices_array = np.array([v0Bot, v1Bot, v2Bot, v0Top, v1Top, v2Top])
  
  vertices = o3d.utility.Vector3dVector(vertices_array)

  # --- 2. Define Triangles (Faces) (Same as before) ---
  
  triangles = np.array([
    # Bottom Triangle Cap 
    [0, 1, 2],
    
    # Top Triangle Cap 
    [3, 5, 4], 
    
    # Rectangular Sides (3 sides, 2 triangles each)
    [0, 1, 4], [0, 4, 3], # Side 1
    [1, 2, 5], [1, 5, 4], # Side 2
    [2, 0, 3], [2, 3, 5]  # Side 3
  ])
  
  triangle_indices = o3d.utility.Vector3iVector(triangles)

  # --- 3. Create the Mesh ---
  mesh = o3d.geometry.TriangleMesh(vertices, triangle_indices)
  
  # Compute normals for correct rendering
  mesh.compute_vertex_normals()
  
  # --- 4. Apply Transformations ---
  
  # A. Flip on X-axis (180-degree rotation around the X-axis)
  if xFlip:
    # Rotation matrix for 180 degrees (pi radians) around the X-axis
    R = mesh.get_rotation_matrix_from_xyz((np.pi, 0, 0))
    # Rotate the mesh
    mesh.rotate(R, center=(0, 0, 0))

  # B. Translate to desired position
  mesh.translate(center)
  
  return mesh

def create_custom_pipe(radius: float, start: np.ndarray, end: np.ndarray):
  length = np.linalg.norm(end - start)
  direction = end - start
  center = start + direction / 2

  dirNorm = direction / np.linalg.norm(direction)
  up = np.array([0, 0, 1])
  
  mesh = o3d.geometry.TriangleMesh.create_cylinder(radius, length)

  r = R_scipy.align_vectors(dirNorm.reshape(1, 3), up.reshape(1, 3))[0]

  R = r.as_matrix()

  mesh.rotate(R, center=(0, 0, 0))
  mesh.translate(center)
  mesh.compute_vertex_normals()

  return mesh

def create_custom_parallelogram(radius: float, top: np.ndarray, bot: np.ndarray, diffVec: np.ndarray):
  topL = top - diffVec
  topR = top + diffVec
  botL = bot - diffVec
  botR = bot + diffVec

  mesh1 = create_custom_pipe(radius, topL, topR)
  mesh2 = create_custom_pipe(radius, topL, botL)
  mesh3 = create_custom_pipe(radius, topR, botR)
  mesh4 = create_custom_pipe(radius, botL, botR)
  
  return mesh1 + mesh2 + mesh3 + mesh4

# flipped_prism = create_custom_triangular_prism(
#   side_length=2.0, 
#   height=5.0, 
#   center_x=5.0, 
#   center_y=3.0, 
#   center_z=0.0, 
#   flip_x=True
# )

# standard_prism = create_custom_triangular_prism(
#   side_length=1.0, 
#   height=2.0, 
#   center_x=0.0, 
#   center_y=0.0, 
#   center_z=0.0, 
#   flip_x=False
# )

# custPipe = create_custom_pipe(0.1, np.array([0, 0, 0]), np.array([5, 5, 5]))

# custParl = create_custom_parallelogram(0.1, np.array([10, 10, 10]), np.array([10, 15, 15]), np.array([1, 0, 0]))

# coordinate_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=1.0)
# o3d.visualization.draw_geometries([flipped_prism, standard_prism, custPipe, custParl, coordinate_frame])