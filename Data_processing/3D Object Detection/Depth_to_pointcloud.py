import numpy as np


def get_point_cloud_from_z(depth, camera_matrix):
    x, z = np.meshgrid(np.arange(depth.shape[-1]),
                       np.arange(depth.shape[-2] - 1, -1, -1))

    X = (x[:, :] - camera_matrix.xc) * depth[:, :] / camera_matrix.fx
    Z = (z[:, :] - camera_matrix.zc) * depth[:, :] / camera_matrix.fy

    point_cloud = np.concatenate((X[..., np.newaxis] / 2.5, depth[:, :][..., np.newaxis] / 6.5 + 200
                                  , Z[..., np.newaxis] / 2 + 300), axis=X.ndim)
    return point_cloud


