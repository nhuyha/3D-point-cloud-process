import open3d as o3d
import numpy as np
import random

def robust_floor_segmentation(pcd, distance_threshold=0.02, ransac_n=3, num_iterations=1000, trials=5, seed=42):
    np.random.seed(seed)
    random.seed(seed)
    o3d.utility.random.seed(seed)

    best_z = None
    best_inliers = None
    best_plane_model = None

    for t in range(trials):
        plane_model, inliers = pcd.segment_plane(
            distance_threshold=distance_threshold,
            ransac_n=ransac_n,
            num_iterations=num_iterations
        )
        inlier_cloud = pcd.select_by_index(inliers)
        z_mean = np.mean(np.asarray(inlier_cloud.points)[:, 2])

        if best_z is None or z_mean < best_z:  # chọn mặt phẳng thấp nhất
            best_z = z_mean
            best_inliers = inliers
            best_plane_model = plane_model

    floor_cloud = pcd.select_by_index(best_inliers)
    pcd_wo_floor = pcd.select_by_index(best_inliers, invert=True)

    return floor_cloud, pcd_wo_floor, best_z, best_plane_model

def main():
    pcd = o3d.io.read_point_cloud("data/pcd.ply")
    floor, pcd_wo_floor, floor_z, plane_model = robust_floor_segmentation(pcd, trials=1)
    print(f"Estimated floor height (z): {floor_z}")
    

if __name__ == "__main__":
    main()