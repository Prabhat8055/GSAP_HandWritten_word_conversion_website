from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import glob
import cv2
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from keras.models import load_model
import warnings
import tkinter as tk 
from tkinter import filedialog 

warnings.filterwarnings('ignore')
# Load the pre-trained model and define the word_dict
model = load_model('model_hand.h5')

word_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M',
             13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y',
             25: 'Z'}
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}



app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

location_set = False
select_path = ""

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
# function for user to selecting the folder 
def select_folder():
    global location_set, select_path
    if not location_set:
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        folder_path = filedialog.askdirectory(title="Select Folder")
        print("Selected folder path:", folder_path)
        select_path = folder_path
        location_set = True  # Set the flag to True once the location is set
    return select_path

# image processing and detecting  function


def processing(filename):
    p = cv2.imread(f"uploads/{filename}")

    # p = cv2.cvtColor(p, cv2.COLOR_BGR2RGB)
    h, w, c = p.shape
    if w > 1000:
        new_w = 1000
        ar = w / h
        new_h = int(new_w / ar)
        p = cv2.resize(p, (new_w, new_h), interpolation=cv2.INTER_AREA)
    plt.imshow(p)

    # plt.show()

    def thresholding(image):
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(img_gray, 100, 150, cv2.THRESH_BINARY_INV)
        plt.imshow(thresh, cmap='gray')
        return thresh

    thresh_img = thresholding(p)
    # plt.show()

    # Dilation operation
    kernal = np.ones((1, 30), np.int8)  # changed
    dilated = cv2.dilate(thresh_img, kernal, iterations=1)
    plt.imshow(dilated, cmap='gray')
    # plt.show()

    # find contours
    (contours, heirarchy) = cv2.findContours(
        dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    sorted_contours_lines = sorted(
        contours, key=lambda ctr: cv2.boundingRect(ctr)[1])  # (x,y,w,h)

    img2 = p.copy()
    for ctr in sorted_contours_lines:
        x, y, w, h = cv2.boundingRect(ctr)
        cv2.rectangle(img2, (x, y), (x + w, y + h), (40, 100, 250), 2)
    plt.imshow(img2)
    # plt.show()

    # Dilation operation
    kernal = np.ones((1, 6), np.int8)  # changed
    dilated2 = cv2.dilate(thresh_img, kernal, iterations=1)
    plt.imshow(dilated2, cmap='gray')
    # plt.show()

    img3 = p.copy()
    characters_list = []
    for line in sorted_contours_lines:

        # roi of each character
        x, y, w, h = cv2.boundingRect(line)
        roi_line = dilated2[y:y + w, x:x + w]
        # draw contours on each character
        (cnt, heirarchy) = cv2.findContours(
            roi_line.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        sorted_contour_words = sorted(
            cnt, key=lambda cntr: cv2.boundingRect(cntr)[0])
        for word in sorted_contour_words:
            x2, y2, w2, h2 = cv2.boundingRect(word)
            characters_list.append([x + x2, y + y2, x + x2 + w2, y + y2 + h2])
            cv2.rectangle(img3, (x + x2, y + y2), (x + x2 +
                          w2, y + y2 + h2), (255, 255, 100), 2)
    plt.imshow(img3)
    # plt.show()
    select_path = select_folder()

    for i in range(len(characters_list)):
        fift_char = characters_list[i]
        roi_4 = p[fift_char[1]:fift_char[3], fift_char[0]:fift_char[2]]
        plt.imshow(roi_4)
        # plt.show()
        cwd = os.getcwd()
        cv2.imwrite(
            f"{select_path}/char{i}.png", roi_4)
        print("image saved...")

    # Build the predicted word from character predictions
    final_word = []

    for j in range(len(characters_list)):
        images = [cv2.imread(file) for file in sorted(
            glob.glob(f"{select_path}\\*.png"))]

        img = images[j]
        img_copy = img.copy()

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (400, 440))

        img_copy = cv2.GaussianBlur(img_copy, (7, 7), 0)
        img_gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
        _, img_thresh = cv2.threshold(
            img_gray, 100, 255, cv2.THRESH_BINARY_INV)

        img_final = cv2.resize(img_thresh, (28, 28))
        img_final = np.reshape(img_final, (1, 28, 28, 1))

        img_pred = word_dict[np.argmax(model.predict(img_final))]

        cv2.putText(img, "Dataflair _ _ _ ", (20, 25),
                    cv2.FONT_HERSHEY_TRIPLEX, 0.7, color=(0, 0, 230))
        cv2.putText(img, "Prediction: " + img_pred, (20, 410),
                    cv2.FONT_HERSHEY_DUPLEX, 1.3, color=(255, 0, 30))
        # cv2.imshow('Dataflair handwritten character recognition _ _ _ ', img)
        final_word.append(img_pred)
        word_string = ''.join(final_word)
        print("Your predected word is -", word_string)
    return word_string


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.form.get("file")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "ERROR!"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "please upload the image"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            word_string = processing(filename)
            flash(f"<p>{word_string}</p>")
            return render_template('predict.html')

    return render_template('predict.html')


if __name__ == '__main__':
    app.run(port=8000, debug=True)
