import numpy as np
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

from pose import createAngleList
from metrics import compare_angle_lists

def compareVideos(ref1, ref2):
    # Step 1 - Get angle lists for Input A and Input B
    all_angle_list1 = createAngleList(ref1)
    all_angle_list2 = createAngleList(ref2)

    all_angle_array1 = np.array(all_angle_list1)
    all_angle_array2 = np.array(all_angle_list2)

    # Step 2 - Pass through Dynamic Time Wraping (DTW) Algorithm
    _, path = fastdtw(all_angle_array1, all_angle_array2, dist=euclidean)

    # Step 3 - Use Path to get aggregate Percent Error Difference per frame!
    result = compare_angle_lists(all_angle_list1, all_angle_list2, path)

    percentErrorList = result[0]
    flaggedTimeStamps = result[1]
    danceScore = abs(100 - round(result[2], 2))

    return danceScore, flaggedTimeStamps, percentErrorList

def main():
    ref1 = "landmarks/RobotDance.txt"
    ref2 = "landmarks/StudentDance.txt"
    danceScore, flaggedTimeStamps, percentErrorList = compareVideos(ref1, ref2)
    print(danceScore)
    print(flaggedTimeStamps)
    print(percentErrorList)

if __name__ == "__main__":
    main()
