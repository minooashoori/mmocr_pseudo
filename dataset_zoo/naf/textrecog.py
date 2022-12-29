# The transcription of NAF dataset is annotated from Tessaract OCR, which is
# not accurate. The test/valid set ones were hand corrected, but the train set
# was only hand corrected a little. They aren't very good results. Better
# not to use them for recognition and text spotting.

_base_ = ['textdet.py']
data_root = 'data/naf'

data_converter = dict(
    type='TextRecogCropConverter',
    parser=dict(
        type='NAFAnnParser', data_root=data_root, ignore=['¿', '§'],
        det=False),
    delete=['temp_images', 'naf_anno', 'data_split.json', 'annotations'])

config_generator = dict(
    type='TextRecogConfigGenerator',
    data_root=data_root,
    val_anns=[dict(ann_file='textrecog_val.json', dataset_postfix='')])
