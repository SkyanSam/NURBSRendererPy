cd C:\Python310\Scripts\
pyinstaller -c --onedir --noconfirm C:\Users\samue\OneDrive\Documents\GitHub\NURBSRendererPy\main.py --add-data C:\Users\samue\OneDrive\Documents\GitHub\NURBSRendererPy\bezierpatch3.obj;. --hidden-import scipy --hidden-import multiprocessing