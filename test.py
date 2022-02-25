#/bin/python3

import project

leafs = project.leaf_segmentation('./rgb', './segmented', 20)
leafs.segment()
