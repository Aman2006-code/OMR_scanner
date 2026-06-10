import cv2
import utills

img = cv2.imread("omr_answerd.jpg")


def main(image):

    if image is not None:
        # Pre-Processing
        grayed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(grayed, (5, 5), 0)
        edged = cv2.Canny(blurred, 100, 500)

        # countour detection
        countours = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        countours = countours[0] if len(countours) == 2 else countours[1]
        contour_data = utills.extractContourData(countours)

        answer_layout = utills.detectAnswerLayout(contour_data)
        if answer_layout:
            answers = answer_layout[0]
            x_min = answer_layout[1]
            option_dist = answer_layout[2]
            section_dist = answer_layout[3]
        else:
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
            else:
                print("0")

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
                print("0")
    else:
        print("Failed to load image")
        return -1


main(img)

# For values of x we processed minimum value of x, the difference between two options and the difference between two sections...
# Similarly we should do for y so that just by getting y_min and number of questions we should be able to get all y values that have options corresponding
# The most natural response is to write a util function for both since most actions are repetative
# Thus removing the ambiguity of unanswered questions
