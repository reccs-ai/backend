import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

from pose import getAngleList
from metrics import compare_angle_lists
ref1 = "videos/RobotDance.mov"
ref2 = "videos/VenushaDance.mov"

def compareVideos(ref1, ref2):
    # Step 1 - Get angle lists for Input A and Input B
    list1 = getAngleList(ref1, showVideo=False, draw=False)
    list2 = getAngleList(ref2, showVideo=False, draw=False)

    # Step 2 - Pass through Dynamic Time Wraping (DTW) Algorithm
    _, path = fastdtw(np.array(list1), np.array(list2), dist=euclidean)

    # Step 3 - Use Path to get aggregate Percent Error Difference per frame!
    result = compare_angle_lists(list1, list2, path)

    percentErrorList = result[0]
    flaggedTimeStamps = result[1]
    danceScore = abs(100 - round(result[2], 2))

    return danceScore, flaggedTimeStamps, percentErrorList

def main():
    compareVideos(ref1, ref2)

if __name__ == "__main__":
    main()
