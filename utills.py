from collections import defaultdict
from statistics import median

import cv2


def average(listOfItems):
    try:
        return sum(listOfItems) // len(listOfItems)
    except ZeroDivisionError:
        return 0


def extractContourData(contours):
    contourData = []
    area_list = []
    for contour in contours:
        area_list.append(cv2.contourArea(contour))
    avg_area = median(area_list)

    for contour in contours:
        area = cv2.contourArea(contour)
        if 1.5 * avg_area < area:
            x, y, w, h = cv2.boundingRect(contour)
            perimeter = cv2.arcLength(contour, True)
            contourData.append([perimeter, x, y, w, h])
    return contourData


def cluster_boundaries_y(ans):
    ans = sorted(ans, key=lambda x: x[0])
    y = [data[1] for data in ans]
    x_count = defaultdict(int)
    for s in y:
        x_count[s] += 1
    y_boundary = []
    for key, value in x_count.items():
        if value > 2:
            y_boundary.append(key)
    y_max = max(y_boundary)
    y_min = (min(y_boundary) + y_max) // 2

    if len(y_boundary) > 1:
        return [y_min, y_max]
    return None


def detectAnswerLayout(contour_data):
    avg_perimeter = average([data[0] for data in contour_data])
    answers = []
    x_list = set()
    cluster_y = cluster_boundaries_y(
        [[data[1], data[2], data[3], data[4]] for data in contour_data]
    )
    print(cluster_y)
    if cluster_y is not None:
        y_min = cluster_y[0]
        y_max = cluster_y[1]
    else:
        return None
    for data in contour_data:
        if data[0] <= 1.1 * avg_perimeter and y_min <= data[2] < y_max:
            x, y, w, h = data[1], data[2], data[3], data[4]
            answers.append((x, y, w, h))
            x_list.add(x)
        else:
            continue

    answers = sorted(answers, key=lambda x: (x[1], x[0]))

    x_list = sorted(x_list)
    x_min = x_list[0]
    diffs = {b - a for a, b in zip(x_list, x_list[1:]) if b - a > 5}

    sorted_x = []
    least_val = float("-inf")
    for i in sorted(diffs):
        if i - least_val > 5:
            sorted_x.append(i)
            least_val = i

    if len(sorted_x) == 2:
        option_dist = sorted_x[0]
        section_dist = sorted_x[1]
        tolerence = option_dist // 2
        x_min = x_min + tolerence
    else:
        print("Error occured in option detection")
        return []

    answer_layout = [answers, x_min, option_dist, section_dist]
    return answer_layout


def longest_continous_strip(contour_data):
    data_strip = []
    for data in contour_data:
        data_strip.append([data[1], data[2]])
    data_strip = sorted(data_strip, key=lambda x: x[0])
    count = defaultdict(int)
    for data in data_strip:
        count[data[0]] += 1

    max_x = 0
    for key, value in count.items():
        if value == max(count.values()):
            max_x = key

    return max_x
