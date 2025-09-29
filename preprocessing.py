import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

def clustering_and_remove(pcd, eps=0.03, min_samples=20, n_jobs=-1):
    # DBSCAN clustering
    points = np.asarray(pcd.points)

    clustering = DBSCAN(eps=eps, min_samples=min_samples, n_jobs=n_jobs).fit(points)
    labels = clustering.labels_
    unique_labels = set(labels)

    # Remove small clusters
    indices_to_keep = []
    for label in unique_labels:
        if label == -1:
            continue  # noise
        cluster_indices = np.where(labels == label)[0]
        if len(cluster_indices) > 100:  # keep only large clusters
            indices_to_keep.extend(cluster_indices)

    pcd_filtered = pcd.select_by_index(indices_to_keep)
    
    return pcd_filtered
            
def main():
    pcd = o3d.io.read_point_cloud("data/pcd.ply")

    # downsample and remove noise
    pcd_uniform = pcd.uniform_down_sample(every_k_points=5)
    pcd_statistic, ind = pcd_uniform.remove_statistical_outlier(nb_neighbors=30,
                                                                std_ratio=1.0)      
    pcd_radius, ind = pcd_statistic.remove_radius_outlier(nb_points=3, radius=0.02)

    o3d.io.write_point_cloud("data/pcd_preprocess.ply", pcd_radius)                                       
    print("Số điểm sau tiền xử lý:", len(pcd_radius.points))
    print("Giảm so với số điểm ban đầu:", len(pcd.points)-len(pcd_radius.points))

    pcd_filtered = clustering_and_remove(pcd_radius, eps=0.03, min_samples=20, n_jobs=-1)
    print("Số điểm sau lọc cụm nhỏ:", len(pcd_filtered.points))
    o3d.io.write_point_cloud("data/pcd_filtered.ply", pcd_filtered)
    o3d.visualization.draw_geometries([pcd_filtered])

if __name__ == "__main__":
    main()

    

