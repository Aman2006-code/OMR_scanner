import cv2


def average(listOfItems):
    try:
        return sum(listOfItems) // len(listOfItems)
    except ZeroDivisionError:
        return 0


def extractContourData(contours):
    contourData = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 10:
            x, y, w, h = cv2.boundingRect(contour)
            perimeter = cv2.arcLength(contour, True)
            contourData.append([perimeter, x, y, w, h])
    return contourData


def detectAnswerLayout(contour_data):
    avg_perimeter = average([data[0] for data in contour_data])
    y_avg = average([data[2] for data in contour_data])

    answers = []
    x_list = set()

    for data in contour_data:
        if (
            data[0] <= avg_perimeter
            and data[2] >= y_avg - 70
            and data[2] <= y_avg + 140
        ):
            x, y, w, h = data[1], data[2], data[3], data[4]
            answers.append((x, y, w, h))
            x_list.add(x)
        else:
            continue

    answers = sorted(answers, key=lambda x: x[1])

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
        x_min = [x_min + tolerence]
    else:
        print("Error occured in option detection")
        return []

    answerLayout = [answers, x_min, option_dist, section_dist]

    return answerLayout
