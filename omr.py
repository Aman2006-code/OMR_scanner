import cv2

import utills

img = cv2.imread("test_1.jpg")
questionNumber = 30  # Make it user input if layout of answer sheet changes.
# Resizing to 500x500 for ease of processing
if img.shape[0] > 500 or img.shape[1] > 500:
    img = cv2.resize(img, (500, 500))


def main(image):
    if image is not None:
        # Pre-Processing
        cleaned = utills.preprocess(image)

        # Shape detection
        contours = cv2.findContours(
            cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )[0]

        # Data extraction of detected shapes
        contour_data = utills.extractContourData(contours)

        # Cropping out shapes in the answer layout with details about positions of options
        bound_region, option_a, last_quest, option, section, question_dist = (
            utills.boundRegion(contour_data, questionNumber)
        )

        # Cleaning up the Answer layout to remove noise and irrelevant contours
        valid_contours = utills.validator(
            bound_region, option_a, option, section, question_dist
        )

        # Getting answers using y position and x position mapping
        answers = utills.fixFalsePositives(valid_contours, last_quest, question_dist)
        # Display of output yet found...

        answer_map = utills.answer(answers, option_a, option, section, last_quest, question_dist, questionNumber)
        print(answer_map)
        for contour in answers:
            x, y, w, h = contour
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow("Valid Contours", image)
        cv2.waitKey(0)

        # Returning the identified answers with relevant data(Location of option 'A', option distance,seciton distance)
        if answers is not None:
            return answers
        else:
            print("Failed to load answer layout")
            return -1

    else:
        print("Failed to load image")
        return -1


answer_sheet = main(img)
