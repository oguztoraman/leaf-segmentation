#/bin/python3

import leaf_segmentation

leafs = leaf_segmentation.leaf_segmentation('./rgb', './segmented', 20)
leafs.segment()
