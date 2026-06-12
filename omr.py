import cv2
import utills

img = cv2.imread("test_omr_1.jpeg")
if img.shape[0] > 500 or img.shape[1] > 500:
    img = cv2.resize(img, (500, 500))


def main(image):
    if image is not None:
        # Pre-Processing
        grayed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(grayed, (5, 5), 0)
        thresh = cv2.threshold(
            blurred, 150, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
        edged = cv2.Canny(closed, 250, 400)

        # contours detection
        contours = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour_data = utills.extractContourData(contours[0])
        answers = utills.detectAnswerLayout(contour_data)
        print(answers)

        for data in contour_data:
            x, y, w, h = data[1], data[2], data[3], data[4]
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow("image", image)
        cv2.waitKey(0)

        if answers is not None:
            return answers
        else:
            print("Failed to load answer layout")
            return -1

    else:
        print("Failed to load image")
        return -1


def answer(answer_layout):
    if len(answer_layout) == 4:
        answers = answer_layout[0]
        x_min = answer_layout[1]
        option_dist = answer_layout[2]
        section_dist = answer_layout[3]
    else:
        print("Failed to load answer layout")
        return -1
    section_a = []
    section_b = []

    for i in range(0, len(answers), 2):
        x1, y1, w1, h1 = answers[i]

        if x1 < x_min:
            section_a.append("A")
        elif x1 < (x_min + option_dist):
            section_a.append("B")
        elif x1 < (x_min + (2 * option_dist)):
            section_a.append("C")
        elif x1 < (x_min + (3 * option_dist)):
            section_a.append("D")
        else:
            section_a.append("0")

    for i in range(1, len(answers), 2):
        x2, y2, w2, h2 = answers[i]

        if x2 < (x_min + section_dist + (3 * option_dist)):
            section_b.append("A")
        elif x2 < (x_min + section_dist + (4 * option_dist)):
            section_b.append("B")
        elif x2 < (x_min + section_dist + (5 * option_dist)):
            section_b.append("C")
        elif x2 < (x_min + section_dist + (6 * option_dist)):
            section_b.append("D")
        else:
            section_b.append("0")

    print(section_a + section_b)


def answer_base(image):
    # code
    return -1


answer_sheet = main(img)
answered = answer(answer_sheet)
