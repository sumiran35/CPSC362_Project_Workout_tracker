import ultralytics
import cv2
from ultralytics import solutions
from ultralytics.utils.downloads import safe_download
import os
import time
import numpy as np

#exercise_list = ["Legextention", "Legpress", "Squats", "Pushups"]

#only for test
# for exercise in exercise_list:
#     safe_download(f"https://github.com/ultralytics/assets/releases/download/v0.0.0/{exercise}.demo.video.mp4")

def track_pushups():
    cap = cv2.VideoCapture(0)
    assert cap.isOpened(), "Error reading video file (push up)"

    #to write for the video het height, weight, fps
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
    video_writer = cv2.VideoWriter("Pushups.demo.video.output.avi", 0x7634706d, fps, (w,h)) #cv2.VideoWriter_fourcc(*"mp4v") <-- this didnyt work had to use
                                                                                            #0x7634... which is the mp4 codec
                                                                                            #if this shit doesnt work change the fucking shit to avi
    #for AI GYM
    gym = solutions.AIGym(show = True, #display frame
                          kpts = [5,7,9], #keypoint index to figure specific exercise (for pups 5,7,9)
                          model="yolo11n-pose.pt", #yolo 1 model
                          line_width=4, #line width for bounding boxes and text display
                          verbose=True
                          )
    results = None
    #process video
    start = time.time()
    diff_time = 0
    while cap.isOpened() and diff_time < 60:

        success, im0 = cap.read() #im0 captures bgr format raw frame data in numpy array
        if not success:
            print("Video frame is empty or video processing is over")
            break
        results = gym(im0) #monitor workout on each frame
        video_writer.write(results.plot_im) #write the output frame in file
        print("THIS IS THE RESULT YOU DUMBASS: ", ">>>>>>>>>",results, "<<<<<<<<<<")
        end = time.time()
        diff_time = end - start
    cv2.destroyAllWindows()
    video_writer.release()
    if results is not None:
        return results.workout_count[0]
    else:
        return 0

def track_leg_extension(): #PROBLEM HERE #FIXED B-)
    cap = cv2.VideoCapture(0)
    assert cap.isOpened(), "Error reading video file (leg ext)"

    #to write for the video het height, weight, fps
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
    video_writer = cv2.VideoWriter("leg_extension_output.avi.", 0x7634706d, fps, (w,h)) #cv2.VideoWriter_fourcc(*"mp4v") <-- this didnyt work had to use
     #videowriter takes input from mp4 video file and
    #  something is wrong with video. #0x7634... which is the mp4 codec
    #this woeks now

    #for AI GYM
    gym = solutions.AIGym(show = True, #display frame
                          kpts = [12,14,16], #keypoint index to figure specific exercise (for pups 5,7,9)
                          model="yolo11n-pose.pt", #yolo 1 model
                          line_width=4, #line width for bounding boxes and text display
                          verbose=True
                          )
    results = None
    #process video
    start = time.time()
    diff_time = 0
    while cap.isOpened() and diff_time < 60:

        success, im0 = cap.read()  # im0 captures bgr format raw frame data in numpy array
        if not success:
            print("Video frame is empty or video processing is over")
            break
        results = gym(im0)  # monitor workout on each frame
        video_writer.write(results.plot_im)  # write the output frame in file
        print("THIS IS THE RESULT YOU DUMBASS: ", ">>>>>>>>>", results, "<<<<<<<<<<")
        end = time.time()
        diff_time = end - start
    cv2.destroyAllWindows()
    video_writer.release()
    if results is not None:
        return results.workout_count[0]
    else:
        return 0

def track_squats():
    cap = cv2.VideoCapture(0)
    assert cap.isOpened(), "Error reading video file (squats)"

    # to write for the video het height, weight, fps
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
    video_writer = cv2.VideoWriter("Squats.demo.video.output.avi.", 0x7634706d, fps,(w, h))  # cv2.VideoWriter_fourcc(*"mp4v") <-- this didnyt work had to use
    # videowriter takes input from mp4 video file and
     #0x7634... which is the mp4 codec

    # for AI GYM
    gym = solutions.AIGym(show=True,  # display frame
                          kpts=[5, 11, 13, 15],  # keypoint index to figure specific exercise (for pups 5,7,9)
                          model="yolo11n-pose.pt",  # yolo 1 model
                          line_width=4,
                          up_angle = 160,
                          down_angle = 90,# line width for bounding boxes and text display
                          verbose=True
                          )
    hip_knee_states = {'hip_down': False, 'knee_down': False, 'counted': False}
    rep_count = 0
    results = None
    # process video
    start = time.time()
    diff_time = 0
    while cap.isOpened(): # and diff_time < 60:

        success, im0 = cap.read()  # im0 captures bgr format raw frame data in numpy array
        if not success:
            print("Video frame is empty or video processing is over")
            break
        results = gym(im0)  # monitor workout on each frame
        video_writer.write(results.plot_im)
        if hasattr(results, 'keypoints') and results.keypoints is not None:
            try:
                kpts = results.keypoints[0].xy[0].cpu().numpy()  # First person's keypoints

                # Get required points (COCO format)
                left_shoulder = kpts[5][:2]
                left_hip = kpts[11][:2]
                left_knee = kpts[13][:2]
                left_ankle = kpts[15][:2]

                # Calculate both angles
                hip_angle = calculate_angle(left_shoulder, left_hip, left_knee)
                knee_angle = calculate_angle(left_hip, left_knee, left_ankle)

                # Update states (using AIGym's thresholds)
                hip_knee_states['hip_down'] = hip_angle < gym.down_angle
                hip_knee_states['knee_down'] = knee_angle < gym.down_angle

                # Count reps only when both angles return to up position
                if all(hip_knee_states.values()[:2]):  # Both angles in down position
                    hip_knee_states['counted'] = False
                elif not any(hip_knee_states.values()[:2]) and not hip_knee_states['counted']:
                    rep_count += 1
                    hip_knee_states['counted'] = True

            except IndexError:
                pass  # No person detected

        print(f"Current Squat Count: {rep_count}")
        # write the output frame in file
        print("THIS IS THE RESULT YOU DUMBASS: ", ">>>>>>>>>", results, "<<<<<<<<<<")
        end = time.time()
        diff_time = end - start
    cv2.destroyAllWindows()
    video_writer.release()
    if results is not None:
        return results.workout_count[0]
    else:
        return 0

def track_legpress():
    cap = cv2.VideoCapture(0)
    assert cap.isOpened(), "Error reading video file (legpress)"

    # to write for the video het height, weight, fps
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
    video_writer = cv2.VideoWriter("Legpress.demo.video.output.avi.", 0x7634706d, fps,
                                   (w, h))  # cv2.VideoWriter_fourcc(*"mp4v") <-- this didnyt work had to use
    # videowriter takes input from mp4 video file and
    # 0x7634... which is the mp4 codec

    # for AI GYM
    gym = solutions.AIGym(show=True,  # display frame
                          kpts=[11, 13, 15],  # keypoint index to figure specific exercise (for pups 5,7,9)
                          model="yolo11n-pose.pt",  # yolo 1 model
                          line_width=4,  # line width for bounding boxes and text display
                          # up_angle = 140,
                          # down_angle = 120,
                          verbose=True
                          )
    results = None
    # process video
    start = time.time()
    diff_time = 0
    while cap.isOpened() and diff_time < 60:

        success, im0 = cap.read()  # im0 captures bgr format raw frame data in numpy array
        if not success:
            print("Video frame is empty or video processing is over")
            break
        results = gym(im0)  # monitor workout on each frame
        video_writer.write(results.plot_im)  # write the output frame in file
        print("THIS IS THE RESULT YOU DUMBASS: ", ">>>>>>>>>", results, "<<<<<<<<<<")
        end = time.time()
        diff_time = end - start
    cv2.destroyAllWindows()
    video_writer.release()
    if results is not None:
        return results.workout_count[0]
    else:
        return 0

def track_abs(): #nned to figure out up and down angle because its not executing nice/ very slow so we need to know what we can do here / trackinng is all fukn weird
    cap = cv2.VideoCapture(0)
    assert cap.isOpened(), "Error reading video file (legpress)"

    # to write for the video het height, weight, fps
    w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
    video_writer = cv2.VideoWriter("abs.output.avi.", 0x7634706d, fps,
                                   (w, h))  # cv2.VideoWriter_fourcc(*"mp4v") <-- this didnyt work had to use
    # videowriter takes input from mp4 video file and
    # 0x7634... which is the mp4 codec

    # for AI GYM
    gym = solutions.AIGym(show=True,  # display frame
                          kpts=[6, 12 , 14, 7, 13, 15],  # keypoint index to figure specific exercise (for pups 5,7,9)
                          model="yolo11n-pose.pt",  # yolo 1 model
                          line_width=4,  # line width for bounding boxes and text display
                          # up_angle = 140,
                          # down_angle = 120,
                          verbose=True
                          )
    results = None
    # process video
    start = time.time()
    diff_time = 0
    while cap.isOpened() and diff_time < 60:

        success, im0 = cap.read()  # im0 captures bgr format raw frame data in numpy array
        if not success:
            print("Video frame is empty or video processing is over")
            break
        results = gym(im0)  # monitor workout on each frame
        video_writer.write(results.plot_im)  # write the output frame in file
        print("THIS IS THE RESULT YOU DUMBASS: ", ">>>>>>>>>", results, "<<<<<<<<<<")
        end = time.time()
        diff_time = end - start
    cv2.destroyAllWindows()
    video_writer.release()
    if results is not None:
        return results.workout_count[0]
    else:
        return 0
def track_pullups():

        # Force FFMPEG logging

        # os.environ["OPENCV_FFMPEG_DEBUG"] = "1"
        # os.environ["OPENCV_VIDEOIO_DEBUG"] = "1"

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_HW_ACCELERATION, cv2.VIDEO_ACCELERATION_ANY)
        assert cap.isOpened(), "Error reading video file (pullups)"

        w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH,
                                               cv2.CAP_PROP_FRAME_HEIGHT,
                                               cv2.CAP_PROP_FPS))

        # Use XVID codec for AVI
        video_writer = cv2.VideoWriter("pullups_output.avi",0x7634706d,
                                       fps, (w, h))

        gym = solutions.AIGym(
            show=True,  # Disable GUI
            kpts=[6, 8, 10, 7, 9, 11],
            model='yolo11n-pose.pt',
            line_width=4,
            verbose=True
        )
        results = None
        start = time.time()
        diff_time = 0
        while cap.isOpened() and diff_time < 60:

            success, im0 = cap.read()  # im0 captures bgr format raw frame data in numpy array
            if not success:
                print("Video frame is empty or video processing is over")
                break
            results = gym(im0)  # monitor workout on each frame
            video_writer.write(results.plot_im)  # write the output frame in file
            print("THIS IS THE RESULT YOU DUMBASS: ", ">>>>>>>>>", results, "<<<<<<<<<<")
            end = time.time()
            diff_time = end - start
        cv2.destroyAllWindows()
        video_writer.release()
        if results is not None:
            return results.workout_count[0]
        else:
            return 0
def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(np.degrees(radians))
    return angle if angle <= 180 else 360 - angle
def detect_pose():
    """
    go through every angle change happening;
    calculate the highest degree of change,
    depening upon where the change is happening, try to short list of workouts
    then select the best option out of the shorted lisr.
    1) detect one side (right or left) look at kpts where angle change is massive
    2) then if change is in the elbow kpts, its probably a upper body workout
    3) if change is at the hips or knees then its a lower body workout
    :return:
    The correct pose hopefully :godspeed:
    """
    cap = cv2.VideoCapture("pullups_coverted.mp4")
    assert cap.isOpened(), "Error reading video file (pose)"
    w, h, fps  =(int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
    video_writer = cv2.VideoWriter("pose.output.avi", 0x7634706d,fps, (w,h))

    gym = solutions.AIGym(show=True, kpts = [10,8,6,12,14,16], model = "yolo11n-pose.pt", line_width=4, verbose=True)
    upper_body_workouts = ["pushups", "pullups"]
    lower_body_workouts = ["squats", "legpress", "legextension"]
    start = time.time()
    diff_time = 0
    while cap.isOpened() and diff_time < 10:
        success, im0 = cap.read()
        if not success:
            print("Video frame is empty or video processing is over")
            break
        # if im0 is None:
        #     continue
        results = gym(im0)
        video_writer.write(results.plot_im)
        print(">>>>>>>>>>>>>>>" , type(results) ,  "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        if hasattr(results, 'keypoints') and results.keypoints is not None:
            try:
                kpts = results.keypoints[0].xy[0].cpu().numpy()
                right_wrist = kpts[10][:2]
                right_elbow = kpts[8][:2]
                right_shoulder = kpts[6][:2]
                right_hip = kpts[12][:2]
                right_knee = kpts[14][:2]
                right_ankle = kpts[16][:2]

                elbow_angle = calculate_angle(right_wrist, right_elbow, right_shoulder)
                print("ELBOW ANGLE: ", elbow_angle)
                hip_angle = calculate_angle(right_shoulder, right_hip, right_knee)
                print("HIP ANGLE: ", hip_angle)
                knee_angle = calculate_angle(right_hip, right_knee, right_ankle)
                print("KNEE ANGLE: ", knee_angle)


            except IndexError:
                raise "this never went to the try block"
            end = time.time()
            diff_time = end - start
            # if not success:
            #     print("Video frame is empty or video processing is over")
            #     break

    cv2.destroyAllWindows()
    video_writer.release()

if __name__ == "__main__":
    detect_pose()
#track_squats()