import os
import ExportPointCloud
import Export3DAnnotation
import Del_empty_bbx



dataset = 'Gym'    # scene: 'Office'; 'House'; 'Supermarket_1'; 'Supermarket_2' ...
data_type = 'dynamic'    # 'dynamic' or 'static'
output_file_path = '/home/idesignlab/Desktop/test'    # file path to save export data
dataset_path = f'/media/idesignlab/Ivan1/THUD/THUD_Robot/{dataset}/{data_type}'

def Main(dataset_path, output_file_path):
    '''

    :param dataset_path:
    :param output_file_path:
    :return:
    '''

    class_and_size = {}
    class_and_index = {}

    for capture_num in range(4, 5):
        dataset_file_path = os.path.join(dataset_path, f'Capture_{capture_num}', 'Label')
        depth_file_path = os.path.join(dataset_path, f'Capture_{capture_num}', 'Depth')
        rgb_file_path = os.path.join(dataset_path, f'Capture_{capture_num}', 'RGB')
        if not os.path.exists(dataset_file_path):
            break
        if not os.path.exists(depth_file_path):
            break
        if not os.path.exists(rgb_file_path):
            break

        # Export 3d annotation for train and test
        Export3DAnnotation.Export3DAnnotation(dataset_file_path, output_file_path, capture_num, class_and_size,
                                             class_and_index, split='train')
        Export3DAnnotation.Export3DAnnotation(dataset_file_path, output_file_path, capture_num, class_and_size,
                                              class_and_index, split='test')

        # Export point cloud for train and test
        ExportPointCloud.ExportPointCloud(dataset_file_path, depth_file_path, rgb_file_path, output_file_path,
                                          capture_num, split='train', num_sample=40000)
        ExportPointCloud.ExportPointCloud(dataset_file_path, depth_file_path, rgb_file_path, output_file_path,
                                          capture_num, split='test', num_sample=40000)

    empty_train_num = Del_empty_bbx.Del_empty_bbx(output_file_path, split='train')
    empty_test_num = Del_empty_bbx.Del_empty_bbx(output_file_path, split='test')

    print('empty_train_num: ', empty_train_num)
    print('empty_test_num: ', empty_test_num)
    print('class_and_size:', class_and_size)
    print('class_and_index:', class_and_index)

    return 0

Main(dataset_path, output_file_path)