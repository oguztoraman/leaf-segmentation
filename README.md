# Leaf Segmentation

A leaf segmentation algorithm written in Python3 using OpenCV

## Requirements

+ Git
+ Python3
+ Numpy
+ OpenCV
+ Scipy

## Usage

1. Install requirements

> For Debian/Ubuntu
```
sudo apt install python3-opencv python3-scipy python3-numpy git
```

> For Fedora
```
sudo dnf install python3-opencv python3-scipy python3-numpy git
```

2. Clone this repo
```
git clone https://github.com/oguztoraman/leaf-segmentation
```

3. Run test.py
```
cd leaf-segmentation && python3 test.py
```

## License

+ GPLv3. See the COPYING file for details.

## References

[stackoverflow segmentation problem](https://stackoverflow.com/questions/54723141/segmentation-problem-for-tomato-leaf-images-in-plantvillage-dataset#54726481)

## Sample Output from Google Colab

```
===================================
RGB image
```
![](./rgb/1.jpg)
```
Resulted image
```
![](./sample_output/1.jpg)
```
Segmented image
```
![](./segmented/1.jpg)
```
Success rate: % 91.900634765625
Elapsed time: 0.2488720417022705 s
===================================
Average success rate: % 91.900634765625
Average elapsed time: 0.2488720417022705 s
```
