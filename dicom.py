# import h5py
# import numpy as np
# import os
# import scipy.ndimage as ndimage
#
#
# def get_dataset_from_txt_file(file_path):
#
#     with open(file_path, 'r') as f:
#
#         content = f.readlines()
#
#         return [i.strip() for i in content]
#
#
# def load_file(file_path):
#
#     hdf5 = h5py.File(file_path, 'r')
#
#     ct_data = np.asarray(hdf5['ct'], dtype=np.float32) # 256, 256, 256
#
#     hdf5.close()
#
#     return ct_data
#
#
# def get_image_path(root, index_name):
#
#     img_path = os.path.join(root, index_name, 'ct_xray_data.h5')
#
#     assert os.path.exists(img_path), 'Path do not exist: {}'.format(img_path)
#
#     return img_path
#
#
# data_name = get_dataset_from_txt_file("C:/Users/Daisy/Desktop/Mdata/alldata.txt")
#
# for i in range(len(data_name)):
#
#     # Load original datasets
#
#     img_dir = get_image_path(r"C:\Users\Daisy\Desktop\Mdata\LIDC-HDF5-256", data_name[i])
#
#     ct_data = load_file(img_dir)
#
#     # folder name will store the datasets
#
#     folder_name = os.path.join(r'C:\Users\Daisy\Desktop\analysisdata\LIDC-IDRI', data_name[i])
#
#     os.mkdir(folder_name)
#
#     for j in range(64):
#         # os.path.join('/content/test', "dataname_{0}.dcm".format(i))
#
#         img = sitk.GetImageFromArray(ct_data[j, :, :])
#
#         sitk.WriteImage(img, os.path.join(folder_name, "{0}.dcm".format(j)))






import matplotlib.pyplot as plt
import h5py
import numpy as np
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import ExplicitVRLittleEndian
import pydicom._storage_sopclass_uids


def load_file(file_path):

    hdf5 = h5py.File(file_path, 'r')

    ct_data = np.asarray(hdf5['ct'], dtype=np.float32) # 256, 256, 256

    hdf5.close()

    return ct_data


image3d = image2d.astype(np.uint16)

image3d = load_file(r"C:\Users\Daisy\Desktop\Mdata\LIDC-HDF5-256\LIDC-IDRI-0001.20000101.3000566.1\ct_xray_data.h5")

np.save('LIDC-IDRI-0001.20000101.3000566.1.npy', image3d)

print(image3d.shape)

test = np.load('LIDC-IDRI-0001.20000101.3000566.1.npy')

print(test.shape)

plt.imshow(test[30, :, :], cmap='gray')  # input X-ray

plt.show()

study = pydicom.uid.generate_uid()

series = pydicom.uid.generate_uid()

for i in range(256):

    # os.path.join('/content/test', "dataname_{0}.dcm".format(i))

    image2d = image3d[i, :, :]

    image2d = image2d.astype(np.uint16)

    print("Setting file meta information...")
    # Populate required values for file meta information

    meta = pydicom.Dataset()
    meta.MediaStorageSOPClassUID = pydicom._storage_sopclass_uids.CTImageStorage
    meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
    meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian

    ds = Dataset()
    ds.file_meta = meta

    ds.is_little_endian = True
    ds.is_implicit_VR = False

    ds.SOPClassUID = pydicom._storage_sopclass_uids.CTImageStorage
    ds.PatientName = "Leo"
    ds.PatientID = "0002.20000101.3000522.1"
    ds.StudyDate = "20220218"
    ds.StudyTime = "134258.921270"

    ds.Modality = "CT"
    ds.SeriesInstanceUID = series
    ds.StudyInstanceUID = study
    ds.SOPInstanceUID = pydicom.uid.generate_uid()
    ds.FrameOfReferenceUID = pydicom.uid.generate_uid()

    ds.BitsStored = 16
    ds.BitsAllocated = 16
    ds.SamplesPerPixel = 1
    ds.HighBit = 15

    ds.ImagesInAcquisition = "1"

    ds.Rows = image2d.shape[0]
    ds.Columns = image2d.shape[1]
    ds.InstanceNumber = 1

    ds.ImagePositionPatient = r"0\0\1"
    ds.ImageOrientationPatient = r"1\0\0\0\-1\0"
    ds.ImageType = r"ORIGINAL\PRIMARY\AXIAL"

    ds.RescaleIntercept = "0"
    ds.RescaleSlope = "1"
    ds.PixelSpacing = r"1\1"
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PixelRepresentation = 1

    pydicom.dataset.validate_file_meta(ds.file_meta, enforce_standard=True)

    print("Setting pixel data...")
    ds.PixelData = image2d.tobytes()

    ds.save_as(r"{0}.dcm".format(i))










