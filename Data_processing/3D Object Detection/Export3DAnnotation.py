import os
import json
import math
import numpy as np


def Export3DAnnotation(dataset_file_path, output_file_path,capture_num, class_and_size, class_and_index, split='train'):
    '''
    :param dataset_file_path:
    :param output_file_path:
    :param capture_num:
    :param class_and_size:
    :param class_and_index:
    :param split: train or test
    :return: 3D Bounding Box (N,8): center(x,y,z), size(lx,ly,lz), angle, class.
             Saved as .npy file.
    '''
    output_folder = os.path.join(output_file_path, split)
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    for i in range(1000):
        num = "{:03d}".format(i)
        json_file_path = os.path.join(dataset_file_path, f'captures_{num}.json')
        if not os.path.exists(json_file_path):
            break
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        step_index = 0

        for STEPS in data['captures']:
            step_index += 1
            step_num = STEPS['step']
            Bounding_Box_3D = []
            if split == 'train':
                if (step_num+2)%3 == 0:
                    continue
            if split == 'test':
                if (step_num+2)%3 != 0:
                    continue
            # print(step_num)
            camera_intrinsic = data['captures'][step_index-1]['sensor']['camera_intrinsic']

            for TASK in data['captures'][step_index-1]['annotations']:
                if TASK['id'] == 'bounding box 3D':

                    values = TASK['values']
                    for indx in range(len(values)):
                        obj = values[indx]['label_name']
                        # print(label_name)
                        translation = [values[indx]['translation']['x'], values[indx]['translation']['z'],
                                                         values[indx]['translation']['y']]
                        size = [values[indx]['size']['x'], values[indx]['size']['z'],
                                                         values[indx]['size']['y']]

                        rotation_x = round(values[indx]['rotation']['x'], 4)
                        rotation_y = round(values[indx]['rotation']['y'], 4)
                        rotation_z = round(values[indx]['rotation']['z'], 4)
                        rotation_w = round(values[indx]['rotation']['w'], 4)

                        x_angle = math.atan2(2 * (rotation_w * rotation_x + rotation_y * rotation_z),
                                             1 - 2 * (rotation_x * rotation_x + rotation_y * rotation_y))
                        # z_angle = math.atan2(2 * (rotation_w * rotation_z + rotation_x * rotation_y),
                        #                      1 - 2 * (rotation_y * rotation_y + rotation_z * rotation_z))
                        # y_angle = math.asin(2 * (rotation_w * rotation_y - rotation_z * rotation_x))
                        angle = rotation_w * rotation_y - rotation_z * rotation_x
                        if angle >= 0.5:
                            angle = 0.4999
                        elif angle <= -0.5:
                            angle = -0.4999

                        if int(x_angle) > 0 :
                            heading_angle = [math.asin(2 * angle)]
                        else:
                            heading_angle = [-math.asin(2 * angle)]

                        if obj not in class_and_size:
                            class_and_size[obj] = list(map(float, size))
                            for lable, name in enumerate(class_and_size):
                                class_and_index[name] = lable
                        bounding_box_3D = translation + size + heading_angle + [class_and_index[obj]]

                        Bounding_Box_3D.append(bounding_box_3D)


                    np.save(os.path.join(output_file_path, split, f'{capture_num}_{step_num+2}_BB.npy'), np.array(Bounding_Box_3D))
                    print(f'{split} {capture_num}_{step_num+2} 3DBBox_File has been saved in : ' + os.path.join(output_file_path, split, f'{capture_num}_{step_num+2}_BB.npy'))

    return Bounding_Box_3D
