# besoin de
#pip install scenedetect[opencv]
#pip install opencv-python
# avec numpy, Click et tqdm

# la vitesse d'opération est d'environ 80-90frames/S

import json
import numpy
import cv2

# Standard PySceneDetect imports:
from scenedetect import VideoManager
from scenedetect import SceneManager

# For content-aware scene detection:
from scenedetect.detectors import ContentDetector

def find_scenes(video_path, threshold=20):
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

def time_to_sec(time_str):
    timer = float(time_str[6:12])
    timer += float(time_str[3:5])*60
    timer += float(time_str[0:2])*3600
    return round(timer,3)


scenes_raw = find_scenes("C:/Users/Simon/Desktop/Stage d'Application/Vidéos/2021_Budapest_brasse_hommes_200_finale_broadcast.mp4")
scenes = scenes_raw.get_cut_list()


# Affichage brut
for i in scenes:
    print(i)


template = {"start":0,
            "end":time_to_sec(scenes[0].get_timecode()),
            "camera":"",
            "subject":"",
            "around":"",
            "distance":"",
            "angle":"",
            "movement":"",
            "position":""}

data =[template.copy()]
for i in range(0,len(scenes)-1):
    template["start"]=time_to_sec(scenes[i].get_timecode())
    template["end"]=time_to_sec(scenes[i+1].get_timecode())
    data.append(template.copy())


path = "C:/Users/Simon/Desktop/Stage d'Application/scene cut detection"
with open(path+"/shotlist.json", 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4,sort_keys=True)