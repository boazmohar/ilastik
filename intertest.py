from collections import defaultdict

from PIL import Image as PilImage
from ilastik.array5d.array5D import Array5D, Image, ScalarImage
from ilastik.array5d.point5D import Point5D, Slice5D, Shape5D
from ilastik.features.feature_extractor import FeatureCollection
from ilastik.features.vigra_features import GaussianSmoothing, HessianOfGaussian
from ilastik.annotations import Annotation
from ilastik.classifiers.pixel_classifier import PixelClassifier


import vigra
import numpy as np

raw_data1 = np.asarray(PilImage.open("/home/tomaz/ilastikTests/SampleData/c_cells/cropped/cropped1.png"))
scribblings = np.asarray(PilImage.open("/home/tomaz/ilastikTests/SampleData/c_cells/cropped/cropped1_fake_annotations.png"))

raw_data1 = Array5D(raw_data1, axiskeys='yxc')
annotation = Annotation(scribblings.astype(np.uint32), axiskeys='yx', raw_data=raw_data1)

fc = FeatureCollection(GaussianSmoothing(sigma=0.3), HessianOfGaussian(sigma=1.2), GaussianSmoothing(sigma=1.7))
classifier = PixelClassifier(feature_collection=fc, annotations=[annotation])
predictions = classifier.predict(raw_data1)

pil_images = [c.as_pil_image() for img in predictions.as_uint8().images() for c in img.channels()]
