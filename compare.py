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

    # print('\n\n Printing List1:   ')
    # print(list1)

    # print('\n Printing List2:   ')
    # print(list2)

    # print('Done with Step 1 in Compare.py!!')

    # print('\n\n\n\n\n\n\n')

    # print('Length of List1: ' + str(len(list1)))
    # print('Length of List2: ' + str(len(list2)))


    # Step 2 - Pass through Dynamic Time Wraping (DTW) Algorithm
    _, path = fastdtw(np.array(list1), np.array(list2), dist=euclidean)

    # print('\n---------Printing Path Array (Index Match Ups)---------')
    # print(path)

    # print('Length of Path: ' + str(len(path))) # this is equal to or greater than (why?) the length of the biggest list


    # Step 3 - Use Path to get aggregate Percent Error Difference per frame!
    result = compare_angle_lists(list1, list2, path)

    percentErrorList = result[0]
    flaggedTimeStamps = result[1]
    danceScore = abs(100 - round(result[2], 2))

    return danceScore, flaggedTimeStamps, percentErrorList

    # print('\n\nPercentErrorList: ')
    # print(percentErrorList)

    # print('\n\nFlaggedTimeStamps: ')
    # print(list(set(flaggedTimeStamps)))

    # print('\n\nDance Score: ')
    # print(danceScore)

def main():
    compareVideos(ref1, ref2)

if __name__ == "__main__":
    main()
