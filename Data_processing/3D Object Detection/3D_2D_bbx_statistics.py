import os
import json



def AnnotationStatistics(dataset_file_path):
    '''
    :param dataset_file_path: 'customized path/.../Label'
    :return: Statistic_3DBBX = {}; Statistic_2DBBX = {}
    '''
    Statistic_3DBBX = {}
    Statistic_2DBBX = {}
    for i in range(1000):
        num = "{:03d}".format(i)
        json_file_path = os.path.join(dataset_file_path, f'captures_{num}.json')
        print(json_file_path)
        if not os.path.exists(json_file_path):
            break
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        step_index = 0

        for STEPS in data['captures']:
            step_index += 1
            step_num = STEPS['step']

            for TASK in data['captures'][step_index-1]['annotations']:
                if TASK['id'] == 'bounding box 3D':
                    values = TASK['values']
                    for indx in range(len(values)):
                        obj = values[indx]['label_name']
                        if obj in Statistic_3DBBX:
                            Statistic_3DBBX[obj] += 1
                        else:
                            Statistic_3DBBX[obj] = 1

                if TASK['id'] == 'bounding box':
                    values = TASK['values']
                    for indx in range(len(values)):
                        obj = values[indx]['label_name']
                        if obj in Statistic_2DBBX:
                            Statistic_2DBBX[obj] += 1
                        else:
                            Statistic_2DBBX[obj] = 1

    return Statistic_3DBBX, Statistic_2DBBX



Statistic_3DBBX = {}
Statistic_2DBBX = {}
Statistic_Semantic = {}
Statistic_Instance = {}

for num in range(20):
    dataset_file_path_dynamic = f'/media/idesignlab/Ivan/TUHD_ROBOT/THUD_Robot/Supermarket_2/dynamic/Capture_{num+1}/Dataset/'
    if not os.path.exists(dataset_file_path_dynamic):
        break
    AnnotationStatistics(dataset_file_path_dynamic, Statistic_3DBBX, Statistic_2DBBX)
for num in range(20):
    dataset_file_path_static = f'/media/idesignlab/Ivan/TUHD_ROBOT/THUD_Robot/Supermarket_2/static/Capture_{num + 1}/Dataset/'
    if not os.path.exists(dataset_file_path_static):
        break
    AnnotationStatistics(dataset_file_path_static, Statistic_3DBBX, Statistic_2DBBX)

with open('Supermarket_2_3d_bbox_statistic.json', 'w') as f:
    json.dump(Statistic_3DBBX, f)
with open('Supermarket_2_2d_bbox_statistic.json', 'w') as f:
    json.dump(Statistic_2DBBX, f)