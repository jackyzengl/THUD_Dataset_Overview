import os
import json
from PIL import Image
import numpy as np
from argparse import Namespace
import pc_util
import Depth_to_pointcloud


def ExportPointCloud(dataset_file_path, depth_file_path, rgb_file_path, output_file_path, capture_num, split='train', num_sample=40000,):
    '''

    :param dataset_file_path:
    :param depth_file_path:
    :param rgb_file_path:
    :param output_file_path:
    :param capture_num:
    :param split: train or test
    :return: point_cloud_subsampled, default 40000 points. Saved as .npz file.
    '''

    output_folder = os.path.join(output_file_path, split)
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    json_file_path = os.path.join(dataset_file_path, f'captures_000.json')
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    camera_intrinsic = data['captures'][0]['sensor']['camera_intrinsic']
    # camera_matrix = {'xc': camera_intrinsic[0][2], 'zc': camera_intrinsic[1][2],
                     # 'fx': camera_intrinsic[0][0], 'fy': camera_intrinsic[1][1]}
    camera_matrix = {'xc': 365, 'zc': 265,
                     'fx': camera_intrinsic[0][0], 'fy': camera_intrinsic[1][1]}

    camera_matrix = Namespace(**camera_matrix)


    for i in range(3000):
        num = i+2
        depth_file = os.path.join(depth_file_path, f'depth_{num}.png')
        rgb_file = os.path.join(rgb_file_path, f'rgb_{num}.png')
        if not os.path.exists(depth_file):
            break
        if not os.path.exists(rgb_file):
            break

        if split == 'train':
            if num % 3 == 0:
                continue
        if split == 'test':
            if num % 3 != 0:
                continue

        depth_image = Image.open(depth_file)
        depth = np.asarray(depth_image)


        rgb_image = Image.open(rgb_file)
        rgb = (np.array(rgb_image.convert("RGB"))/255).reshape((4 * int(camera_matrix.xc) * int(camera_matrix.zc), 3))

        point_cloud = Depth_to_pointcloud.get_point_cloud_from_z(depth, camera_matrix)
        point_cloud = point_cloud.reshape((4 * int(camera_matrix.xc) * int(camera_matrix.zc), 3))

        point_cloud = point_cloud/1000
        point_cloud = np.concatenate([point_cloud, rgb], axis=1)

        point_cloud_subsampled = pc_util.random_sampling(point_cloud, num_sample)


        np.savez_compressed(os.path.join(output_file_path, split, f'{capture_num}_{num}_pc.npz'),
                            pc=point_cloud_subsampled)
        print(f'{split} {capture_num}_{num} PC_File has been saved in : ' + os.path.join(output_file_path, split, f'{capture_num}_{num}_pc.npz'))

    return point_cloud_subsampled

