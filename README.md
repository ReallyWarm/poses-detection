# Human Poses Detection
Human poses detection in joint research on drone project.

Only detects human pose with the arms' angle.

### Pose Type
- Strong pose
- T pose
- Lifted up right
- Lifted up left
- Raised up
- Raised right
- Raised left
- Dab right
- Dab left

### Libraries
- opencv
- mediapipe

## Set variables
``` bash
> Detection.py
# set MODE = 0 -> use webcam
#     MODE = 1 -> use image
MODE = 0 # default

# set INFO = range(number_of_landmarks) -> show landmarks informations in the terminal.
INFO = 0 # default

# set START_DEBUG = True -> show fps, arms angles, and pose type on the webcam window.
START_DEBUG = True # default
```
## Example Images
[1.jpg](https://unsplash.com/photos/v4zceVZ5HK8)

[2.jpg](https://unsplash.com/photos/e_rhazQLaSs)
