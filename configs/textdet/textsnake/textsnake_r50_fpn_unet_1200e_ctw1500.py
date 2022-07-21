_base_ = [
    '../../_base_/default_runtime.py',
    '../../_base_/schedules/schedule_sgd_1200e.py',
    '../../_base_/det_models/textsnake_r50_fpn_unet.py',
]

train_pipeline = [
    dict(type='LoadImageFromFile', color_type='color_ignore_orientation'),
    dict(
        type='LoadOCRAnnotations',
        with_bbox=True,
        with_polygon=True,
        with_label=True),
    dict(
        type='TorchVisionWrapper',
        op='ColorJitter',
        brightness=32.0 / 255,
        saturation=0.5),
    dict(
        type='RandomApply',
        transforms=[dict(type='RandomCrop', min_side_ratio=0.3)],
        prob=0.65),
    dict(
        type='RandomRotate',
        max_angle=20,
        pad_with_fixed_color=False,
        use_canvas=True),
    dict(
        type='BoundedScaleAspectJitter',
        long_size_bound=800,
        short_size_bound=480,
        ratio_range=(0.7, 1.3),
        aspect_ratio_range=(0.9, 1.1)),
    dict(
        type='RandomChoice',
        transforms=[[
            dict(type='Resize', scale=800, keep_ratio=True),
            dict(type='SourceImagePad', target_scale=800)
        ],
                    dict(type='Resize', scale=800, keep_ratio=False)],
        prob=[0.4, 0.6]),
    dict(type='RandomFlip', prob=0.5, direction='horizontal'),
    dict(
        type='PackTextDetInputs',
        meta_keys=('img_path', 'ori_shape', 'img_shape'))
]

test_pipeline = [
    dict(type='LoadImageFromFile', color_type='color_ignore_orientation'),
    dict(type='Resize', scale=(1333, 736), keep_ratio=True),
    dict(
        type='PackTextDetInputs',
        meta_keys=('img_path', 'ori_shape', 'img_shape', 'scale_factor',
                   'instances'))
]

dataset_type = 'OCRDataset'
data_root = 'data/ctw1500'

train_dataset = dict(
    type=dataset_type,
    data_root=data_root,
    ann_file='instances_training.json',
    data_prefix=dict(img_path='imgs/'),
    filter_cfg=dict(filter_empty_gt=True, min_size=32),
    pipeline=train_pipeline)

test_dataset = dict(
    type=dataset_type,
    data_root=data_root,
    ann_file='instances_test.json',
    data_prefix=dict(img_path='imgs/'),
    test_mode=True,
    pipeline=test_pipeline)

train_dataloader = dict(
    batch_size=4,
    num_workers=4,
    persistent_workers=False,
    sampler=dict(type='DefaultSampler', shuffle=True),
    dataset=train_dataset)
val_dataloader = dict(
    batch_size=1,
    num_workers=4,
    persistent_workers=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=test_dataset)
test_dataloader = val_dataloader

val_evaluator = dict(type='HmeanIOUMetric')
test_evaluator = val_evaluator

visualizer = dict(type='TextDetLocalVisualizer', name='visualizer')
