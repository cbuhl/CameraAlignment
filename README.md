# Alignment script for two cameras

The problem that is solved, is to align two samples, using something similar to backside alignment.
Two cameras are employed, and the image from the two is overlaid in the script.


### Dependencies:
 - opencv 4.1.2
 - pyqt 5.9.2
 - Python 3.7
 
It's written and developed on macOS 10.14.


## Bresser MikrOkular cameras
The Bresser MikrOkular cameras has been used here, and they provide a very low cost full-HD sensor. 
There's a filter (UV/IR) in front that I anticipate is very easy to remove if that is an issue.

Entirely helplessly, the software arrives on a small disc, and I have not been able to find it online. No worries, though. 
It runs natively with opencv, so you'll have a grand ol' time if you need to implement it in a setup somewhere.

This might also be relevant for the astronomy community; if you need an unimpressive, low-cost, compact and easily interfaced camera, this has my recommendations. It fits well into python.
