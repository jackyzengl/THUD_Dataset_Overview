# THUD
![plot](docs/ICRA24_Poster.png)
We present a mobile robot oriented large-scale indoor dataset, denoted as THUD (Tsinghua University Dynamic) robotic dataset, for training and evaluating their dynamic scene understanding algorithms. Specifically,
the THUD dataset construction is first detailed, including organization, acquisition, and annotation methods. It comprises
both real-world and synthetic data, collected with a real robot platform and a physical simulation platform, respectively. Our current dataset includes 13 larges-scale dynamic scenarios, 90K image frames, 20M 2D/3D bounding boxes of static and dynamic objects, camera poses, and IMU. The dataset is still continuously expanding. Then, the performance of mainstream indoor scene understanding tasks, e.g. 3D object detection, semantic segmentation, and robot relocalization, is evaluated on our THUD dataset. These experiments reveal serious challenges for some robot scene understanding tasks in dynamic scenes. By sharing this dataset, we aim to foster and iterate new mobile robot algorithms quickly for robot actual working dynamic environment, i.e. complex crowded dynamic scenes.

## Homepage
### Website
You can have a detailed understanding of our project from this [website](https://jackyzengl.github.io/THUD-Robotic-Dataset.github.io/).

### Download
If you want to use our dataset, please carefully read our instructions (see Homepage) and truthfully fill in the required information, which is important for us.

## Dataset structure
The THUD dataset contains 8 real scenes and 5 synthetic Scenes. For ease of use, we have uniformly processed the structure of the dataset. For most scenarios, they have similar structures:
##
- THUD
  - Real_Scenes
    - Store
      - static
        - Capture_1
          - Camera_intrinsics
            - camera-intrinsics.txt
          - Depth
            - frame-000000.depth.png
            - frame-000001.depth.png
            - ...
          - Label
            - 2D_Object_Detection
              - frame-000000.json
              - frame-000001.json
              - ...
            - 3D_Object_Detection
              - frame-000000.txt
              - frame-000001.txt
              - ...
            - Pose
              - frame-000000.pose.txt
              - frame-000001.pose.txt
              - ...
            - Semantic
              - frame-000000.png
              - frame-000000.png
              - ...
          - Pointcloud
            - frame-000000.point.ply
            - frame-000001.point.ply
            - ...
          - RGB
            - frame-000000.color.png
            - frame-000001.color.png
            - ...
        - Capture_2(Same structure as Capture_1)
      - dynamic(Same structure as static)
  - Synthetic_Scenes
##








Clone the repository
```
git clone https://github.com/jackyzengl/GRID.git
cd ./GRID
```
Setup conda environment
```
conda create --name grid python=3.8.16
conda activate grid
pip install -r requirements.txt
```
### Instructor embedding installation
Install instructor from source code
```
pip install -e instructor-embedding/.
```

## Download dataset
Download our [dataset](https://github.com/jackyzengl/GRID_Dataset) to path ```dataset/```.


## Preprocess dataset
The parameter required by the data preprocessor is defined in ```${workspace}/hparams.cfg``` [data_preprocessor] section. 
Run data preprocessor to obtain all text embeddings required during training, 
and save the data to the disk. The path of data to be preprocessed is ```${workspace}/dataset/``` by default. The pre-processor saves each processed sample as a ```.pt``` file under the directory ```${workspace}/preprocess_data/```.
Please give one device only as instructor does not support multiple devices.
```
python run_preprocess_data.py --gpu_devices <your device>
```
If you want to specify the dataset location, pass it by argument ```--data_path``` 
```
python run_preprocess_data.py --gpu_devices <your device> --data_path /path/to/data
```
Use``` python run_preprocess_data.py --help``` to see more available options.

## Train a new model
### step 1 setup configuration
set up configuration in ```hparams.cfg```

### step 2 start training
This will fit and predict a model from data preprocessed in ```${workspace}/preprocess_data/```
```
python train.py 
```
If your preprocessed dataset is placed somewhere else, parse the data location into the script by
```
python train.py --preprocessed_data_path /path/to/data
```
Use ```python train.py --help``` to see more arguments such as setting your gpu devices for training.

## Continue training from a checkpoint
This will continue training, and predict output from the training result.

A checkpoint generated by a trained model is saved to ```${workspace}/logs/${experiment_name}/${version_name}/checkpoints/{checkpoint_name}``` with an extension ```.ckpt``` by default.

To run from the checkpoint, the model automatically reads the hyper-parameter which was generated along with the checkpoint. It is usually saved in ```${workspace}/logs/${experiment_name}/${version_name}/hparams.yaml```. 

With the default pre-processed data location, use:
```
python train.py --fit_flag True --from_ckpt_flag True --ckpt_path /path/to/checkpoint
```
Specify the dataset location by argument ```--preprocessed_data_path``` if necessary.
<br/>


## Predict from a checkpoint
This will not train any models but directly predict results from the checkpoint. 

The checkpoint file path requires a ```hparams.cfg``` or ```hparams.yaml``` at related path ```checkpoints/../..``` Typically, ```hparams.yaml``` is generated automatically when running ```train.py```.

With the default data location, use:
```
python train.py --fit_flag False --from_ckpt_flag True --ckpt_path /path/to/checkpoint
```
Specify the dataset location by argument ```--preprocessed_data_path``` if necessary.

## Evaluation
### Subtask accuracy
Our network takes an instruction, a scene graph and a robot graph as input, and predicts a subtask which consists of an action and an object. We use subtask accuracy to evaluate the accuracy of each prediction.

#### Calculate subtask accuracy
Running a prediction automatically calculates the subtask accuracy. 
**Please use only one gpu device to infer results** to log the complete prediction labels.
The prediction creates the ```sub_task_label.xlsx``` and ```accuracy.xlsx``` files in the new checkpoint directory ```logs/{experiment name}/version_{version_number}/```.

```sub_task_label.xlsx``` shows the prediction result for each sample, and ```accuracy.xlsx``` gives the overall accuracy calculation for all subtasks.

### Task accuracy
Each task is associated with a series of subtasks. A task is considered as successful when all predicted subtasks associated with the task are correct. 

#### Calculate task accuracy
To obtain task accuracy, change the ```raw_data_path_``` and ```output_root_path_``` variables in your ```run_evaluation.py``` file. 

```raw_data_path_:```is the path of the raw dataset instead of the preprocessed data.

```output_root_path_:```  the folder of the subtask accuracy file generated in the prediction we made in the previous step.

Run
```
python run_evaluation.py
```
The task accuracy is updated in ```accuracy.xlsx```. 

The new file ```sub_task_accuracy.xlsx``` gives the task accuracies for tasks associated with different numbers of subtasks.

## TODO
- [x] Release training codes.
- [ ] Release checkpoints.
- [ ] Release inference codes.


## Citation
If you find the code useful, please consider citing:
```
@article{ni2024grid,
      title={GRID: Scene-Graph-based Instruction-driven Robotic Task Planning}, 
      author={Zhe Ni and Xiaoxin Deng and Cong Tai and Xinyue Zhu and Qinghongbing Xie and Weihang Huang and Xiang Wu and Long Zeng},
      journal={arXiv preprint arXiv:2309.07726},
      year={2024}
}
```
