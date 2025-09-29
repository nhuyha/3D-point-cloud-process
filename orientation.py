import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import random

def correct_orientation(pcd):
        
    # Fit plane with RANSAC
    plane_model, inliers = pcd.segment_plane(distance_threshold=0.02,
                                            ransac_n=3,
                                            num_iterations=1000)
    [a, b, c, d] = plane_model
    normal = np.array([a, b, c])

    # Chuẩn hóa vector pháp tuyến
    normal /= np.linalg.norm(normal)

    # Xác định ma trận quay: đưa normal -> [0, 0, 1]
    z_axis = np.array([0,0,-1])
    v = np.cross(normal, z_axis)
    c = np.dot(normal, z_axis)
    s = np.linalg.norm(v)
    vx = np.array([[0, -v[2], v[1]],
                [v[2], 0, -v[0]],
                [-v[1], v[0], 0]])
    R = np.eye(3) + vx + vx @ vx * ((1 - c) / (s**2))

    # Áp dụng phép quay
    pcd.rotate(R, center=(0,0,0))

    return pcd


def main():
    # Load point cloud
    pcd = o3d.io.read_point_cloud("data/pointcloud_rgb_gpu.ply")

    print("Số điểm ban đầu:", len(pcd.points))

    pcd = correct_orientation(pcd)

    o3d.visualization.draw_geometries([pcd])

    o3d.io.write_point_cloud("data/pcd.ply", pcd)

if __name__ == "__main__":
    main()
