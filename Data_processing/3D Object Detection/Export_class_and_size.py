import os
import numpy as np



def Export_class_and_size(output_file_path, split='train'):
    class_and_size = {}
    for capture_num in range(1, 20):
        for step_num in range(3000):
            if not os.path.exists(os.path.join(output_file_path, split, f'{capture_num}_{step_num+2}_BB.npy')):
                # print(f'Error index: {capture_num}_{step_num+2}')
                continue
            Bounding_Box_3D = np.load(os.path.join(output_file_path, split, f'{capture_num}_{step_num + 2}_BB.npy'))
            for obj in Bounding_Box_3D:
                # obj = list(map(float, obj[0:7]))
                if obj[7] not in class_and_size:
                    class_and_size[obj[7]] = list(map(float, obj[3:6]))
    return class_and_size
