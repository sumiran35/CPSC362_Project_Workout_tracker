# import cv2
# print(cv2.__version__)
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