from collections import defaultdict
from statistics import median

import cv2
import numpy as np


def average(listOfItems):
    try:
        return sum(listOfItems) // len(listOfItems)
    except ZeroDivisionError:
        return 0


# Image pre-processing
def preprocess(image):
    grayed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Grayscale conversion
    blurred = cv2.GaussianBlur(grayed, (3, 3), 0)  # Blured
    thresh = cv2.threshold(
        blurred,
        0,
        255,
        cv2.THRESH_BINARY_INV
        | cv2.THRESH_OTSU,  # Converting to an inverted binary image(Black for pixels above threshold);
    )[
        1
    ]  # Applied with otsu thresholding - algorithm automatically decides the optimal threshold value....
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))  # Defined a 3x3 kernel
    final = cv2.morphologyEx(
        thresh, cv2.MORPH_OPEN, kernel
    )  # removed black regions less than kernel (3x3)
    return final


# Contour data extraction (edges)
def extractContourData(contours):
    contourData = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(
            contour
        )  # cordinates (x,y), width, height of the rectangle around detected contour
        area = cv2.contourArea(contour)  # area enclosed by the detected contour
        perimeter = cv2.arcLength(contour, True)  # Perimeter of the detected contour
        cover = cv2.contourArea(cv2.convexHull(contour)) / area
        contourData.append([x, y, w, h, area, perimeter, cover])  # Listing
    return contourData


def boundRegion(contour_data, questionNumber):
    x_list = defaultdict(
        list
    )  # Dictionary of all Y - cordinates that has a recognised contour at a particular X (X : [value of Ys])
    y_list = defaultdict(
        list
    )  # Dictionary of all X - cordinates that has a recognised contour at a particular Y (Y : [value of Xs])
    for contour in contour_data:
        x_list[contour[0]].append(contour[1])
        y_list[contour[1]].append(contour[0])
    strip_vertical_x = max(x_list, key=lambda k: len(x_list[k]))
    strip_horizontal_y = max(
        [key for key, value in y_list.items() if len(value) == 4], default=0
    )

    strip_vertical = x_list[strip_vertical_x]  # The left margin
    strip_horizontal = y_list[
        strip_horizontal_y
    ]  # The bottom strip (That has a,c,d,D positions identified for optical detection aid)

    strip_vertical.sort()
    strip_horizontal.sort()
    a_posit = strip_horizontal[0]  # Position of option a
    option_dist = (
        strip_horizontal[2] - strip_horizontal[1]
    )  # Distance between any two options
    section_dist = (
        strip_horizontal[3] - strip_horizontal[2]
    )  # Distance between the two sections
    question_dist = median(
        [
            strip_vertical[i] - strip_vertical[i - 1]
            for i in range(1, len(strip_vertical))
        ]
    )  # Assumed distance between two questions

    last_quest = strip_horizontal_y - question_dist

    min_x, max_x = strip_vertical_x + 5, strip_horizontal[-1] + 5
    max_y = strip_horizontal_y
    min_y = max_y - ((questionNumber // 2) * question_dist) - 10

    answerLayout = []
    for contour in contour_data:
        cover = contour[5]
        if min_x <= contour[0] <= max_x and min_y <= contour[1] < max_y:
            if cover > 0.98:
                answerLayout.append(contour)  # Answer layout cropped out
    return answerLayout, a_posit, last_quest, option_dist, section_dist, question_dist


def validator(data, option_a, option, section, question):
    options = []
    for i in range(2):
        for j in range(4):
            options.append(
                option_a + i * section + j * option
            )  # All possible x cordinates of options available(a,b,c,d,A,B,C,D)
    valid_contours = []
    average_area = average([x[4] for x in data])  # Average area of the contours
    for contour in data:
        if (
            average_area <= contour[4] <= 2 * average_area
        ):  # Making up for false positives that are small noises
            if any(
                x - 5 <= contour[0] <= x + 5 for x in options
            ):  # Making up for false positives that lay outside expected answer positions
                valid_contours.append(contour[:4])  # Final detected answer contours
    return valid_contours


def fixFalsePositives(valid_contours, last_quest, question):
    if not valid_contours:
        return [], last_quest

    # Average Contour Area (Approximation)
    avg_area = average([x[2] * x[3] for x in valid_contours])

    # Sort contours by their Y-coordinate
    valid_contours.sort(key=lambda x: x[1])

    def cleanRow(row):
        # If there are more than 2 bubbles =>  we have noise (Since layout is two layered)
        if len(row) > 2:
            row.sort(
                key=lambda area: abs((area[2] * area[3]) - avg_area)
            )  # Sort bubbles by their closeness to average area
            row = row[:2]  # Two most similar bubbles get selected.

        row.sort(key=lambda x: x[0])  # Final Sort by X-coordinate
        return row

    answer_list = []  # Initialising an empty answer list
    current_row = [valid_contours[0]]  # First data of intrest is the first row
    y_tolerance = (
        question / 2.0
    )  # Less than half way from one question is no next question..
    for contour in valid_contours[1:]:
        if abs(contour[1] - current_row[0][1]) <= y_tolerance:  # If same line
            current_row.append(contour)  # Append to a temperory current line column
        else:  # Current line ends
            answer_list.extend(
                cleanRow(current_row)
            )  # Process the data in the temoporary current line clean it and add to answer
            current_row = [
                contour
            ]  # Make the current line empty and add the next line(This contour) to it..

    if current_row:
        answer_list.extend(cleanRow(current_row))  # Final row

    return answer_list


def answer(contours, optionA, option_dist, section_dist, row_dist, last_question):
    pass
