import os
import numpy as np



def Del_empty_bbx(output_file_path, split='train'):
    empty_num = 0
    emptylist = []
    for capture_num in range(1, 20):
        for step_num in range(3000):
            if not os.path.exists(os.path.join(output_file_path, split, f'{capture_num}_{step_num+2}_BB.npy')):
                continue
            Bounding_Box_3D = np.load(os.path.join(output_file_path, split, f'{capture_num}_{step_num + 2}_BB.npy'))
            if Bounding_Box_3D.shape[0] == 0:
                empty_num += 1
                print(f'Found Empty BBx: {capture_num}_{step_num + 2}_BB.npy')
                os.remove(os.path.join(output_file_path, split, f'{capture_num}_{step_num + 2}_BB.npy'))
                print(f'Remove: {capture_num}_{step_num + 2}_BB.npy')
                os.remove(os.path.join(output_file_path, split, f'{capture_num}_{step_num + 2}_pc.npz'))
                print(f'Remove: {capture_num}_{step_num + 2}_pc.npz')


    return empty_num
