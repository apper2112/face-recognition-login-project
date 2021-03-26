
********** FACE RECOGNITION ***********

#NOTES
This program was written and tested on Linux
You may need to alter minor things for Windows

You will need to alter the wallpaper image and geometry dimensions
to suit your screen.

To remove a user manually:
    delete users image from images folder
    delete users entry in registered.csv file

Dragging photos into images folder wont work here.
Create photos from webcam

****************************************

#DEPENDENCIES
pip install cmake
pip install dlib -vvv
pip install opencv-python
pip install face_recognition


# pip list LOOKS LIKE IN MY VENV 
Package                 Version
----------------------- ------------
click                   7.1.2
cmake                   3.18.4.post1
dlib                    19.21.1
face-recognition        1.3.0
face-recognition-models 0.3.0
numpy                   1.19.5
opencv-python           4.5.1.48
Pillow                  8.1.0
pip                     21.0.1
setuptools              50.3.0
wheel                   0.35.1


#LINUX
sudo apt-get install python3-tk


#USING CUSTOM FONTS LINUX EXAMPLE
unzip fontname.zip

mkdir ~/.fonts
cp ~/Downloads/fontname.ttf ~/.fonts/
