import cv2
import numpy as np

img = cv2.imread("omr_answerd.jpg")


def average(listOfItems):
    try:
        return sum(listOfItems) // len(listOfItems)
    except ZeroDivisionError:
        return 0


def main(image):
    if image is not None:
        # Pre-Processing
        grayed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(grayed, (5, 5), 0)
        edged = cv2.Canny(blurred, 100, 500)

        # countour detection
        countours = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        countours = countours[0] if len(countours) == 2 else countours[1]

        contour_data = []
        x_list = set()
        y_list = set()
        for contour in countours:
            area = cv2.contourArea(contour)
            if area > 10:
                x, y, w, h = cv2.boundingRect(contour)
                perimeter = cv2.arcLength(contour, True)
                contour_data.append([perimeter, x, y, w, h])

        avg_perimeter = average([data[0] for data in contour_data])
        y_avg = average([data[2] for data in contour_data])

        answers = []
        for data in contour_data:
            if (
                data[0] <= avg_perimeter
                and data[2] >= y_avg - 70
                and data[2] <= y_avg + 140
            ):
                x, y, w, h = data[1], data[2], data[3], data[4]
                answers.append((x, y, w, h))
                x_list.add(x)
                y_list.add(y)
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
            x_min = x_min + tolerence
        else:
            print("Error occured in option detection")
            return -1

        print("Section A")
        for i in range(1, len(answers), 2):
            x1, y1, w1, h1 = answers[i]

            if x1 < x_min:
                print("A")
            elif x1 < (x_min + option_dist):
                print("B")
            elif x1 < (x_min + (2 * option_dist)):
                print("C")
            elif x1 < (x_min + (3 * option_dist)):
                print("D")

        print("Section B")
        for i in range(0, len(answers), 2):
            x2, y2, w2, h2 = answers[i]

            if x2 < (x_min + section_dist + (3 * option_dist)):
                print("A")
            elif x2 < (x_min + section_dist + (4 * option_dist)):
                print("B")
            elif x2 < (x_min + section_dist + (5 * option_dist)):
                print("C")
            elif x2 < (x_min + section_dist + (6 * option_dist)):
                print("D")

    else:
        print("Failed to load image")
        return -1


main(img)

# For values of x we processed minimum value of x, the difference between two options and the difference between two sections...
# Similarly we should do for y so that just by getting y_min and number of questions we should be able to get all y values that have options corresponding
# The most natural response is to write a util function for both since most actions are repetative
# Thus removing the ambiguity of unanswered questions
