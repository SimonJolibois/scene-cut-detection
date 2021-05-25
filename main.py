# besoin de
#pip install scenedetect[opencv]
#pip install opencv-python
# avec numpy, Click et tqdm

# le temps d'opération est d'environ 18 secondes pour 1 minute de vidéo à 25fps
import json
import numpy
import cv2

# Standard PySceneDetect imports:
from scenedetect import VideoManager
from scenedetect import SceneManager

# For content-aware scene detection:
from scenedetect.detectors import ContentDetector

def find_scenes(video_path, threshold=30.0):
    # Create our video & scene managers, then add the detector.
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold))

    # Improve processing speed by downscaling before processing.
    video_manager.set_downscale_factor()

    # Start the video manager and perform the scene detection.
    video_manager.start()
    scene_manager.detect_scenes(frame_source=video_manager, end_time=None, frame_skip=0, show_progress=True)

    # Each returned scene is a tuple of the (start, end) timecode.
    return scene_manager

scenes_raw = find_scenes('C:/Users/Simon/Downloads/2021_Budapest_freestyle_dames_50_finale_broadcast.mp4')
scenes = scenes_raw.get_cut_list()


# Affichage brut
for i in scenes:
    print(i)


template = {"start":0,
            "end":scenes[0].get_frames(),
            "camera":"",
            "subject":"",
            "around":"",
            "distance":"",
            "angle":"",
            "movement":"",
            "position":""}

data =[template.copy()]
for i in range(0,len(scenes)-1):
    template["start"]=scenes[i].get_frames()
    template["end"]=scenes[i+1].get_frames()
    data.append(template.copy())


path = "C:/Users/Simon/Desktop/Stage d'Application/scene cut detection"
with open(path+"/shotlist.json", 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4,sort_keys=True)