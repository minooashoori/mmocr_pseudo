# Copyright (c) OpenMMLab. All rights reserved.
from numbers import Number
from typing import List, Optional, Sequence, Tuple, Union

import torch
import torch.nn as nn
from mmengine.model import ImgDataPreprocessor

from mmocr.registry import MODELS


@MODELS.register_module()
class TextRecogDataPreprocessor(ImgDataPreprocessor):
    """Image pre-processor for recognition tasks.

    Comparing with the :class:`mmengine.ImgDataPreprocessor`,

    1. It supports batch augmentations.
    2. It will additionally append batch_input_shape and valid_ratio
    to data_samples considering the object recognition task.

    It provides the data pre-processing as follows

    - Collate and move data to the target device.
    - Pad inputs to the maximum size of current batch with defined
      ``pad_value``. The padding size can be divisible by a defined
      ``pad_size_divisor``
    - Stack inputs to batch_inputs.
    - Convert inputs from bgr to rgb if the shape of input is (3, H, W).
    - Normalize image with defined std and mean.
    - Do batch augmentations during training.

    Args:
        mean (Sequence[Number], optional): The pixel mean of R, G, B channels.
            Defaults to None.
        std (Sequence[Number], optional): The pixel standard deviation of
            R, G, B channels. Defaults to None.
        pad_size_divisor (int): The size of padded image should be
            divisible by ``pad_size_divisor``. Defaults to 1.
        pad_value (Number): The padded pixel value. Defaults to 0.
        bgr_to_rgb (bool): whether to convert image from BGR to RGB.
            Defaults to False.
        rgb_to_bgr (bool): whether to convert image from RGB to RGB.
            Defaults to False.
        batch_augments (list[dict], optional): Batch-level augmentations
    """

    def __init__(self,
                 mean: Sequence[Number] = None,
                 std: Sequence[Number] = None,
                 pad_size_divisor: int = 1,
                 pad_value: Union[float, int] = 0,
                 bgr_to_rgb: bool = False,
                 rgb_to_bgr: bool = False,
                 batch_augments: Optional[List[dict]] = None):
        super().__init__(
            mean=mean,
            std=std,
            pad_size_divisor=pad_size_divisor,
            pad_value=pad_value,
            bgr_to_rgb=bgr_to_rgb,
            rgb_to_bgr=rgb_to_bgr)
        if batch_augments is not None:
            self.batch_augments = nn.ModuleList(
                [MODELS.build(aug) for aug in batch_augments])
        else:
            self.batch_augments = None

    def forward(self,
                data: Sequence[dict],
                training: bool = False) -> Tuple[torch.Tensor, Optional[list]]:
        """Perform normalization、padding and bgr2rgb conversion based on
        ``BaseDataPreprocessor``.

        Args:
            data (Sequence[dict]): data sampled from dataloader.
            training (bool): Whether to enable training time augmentation.

        Returns:
            Tuple[torch.Tensor, Optional[list]]: Data in the same format as the
            model input.
        """
        batch_inputs, batch_data_samples = super().forward(
            data=data, training=training)

        if batch_data_samples is not None:
            batch_input_shape = tuple(batch_inputs[0].size()[-2:])
            for data_samples in batch_data_samples:

                valid_ratio = data_samples.valid_ratio * \
                    data_samples.img_shape[1] / batch_input_shape[1]
                data_samples.set_metainfo(
                    dict(
                        valid_ratio=valid_ratio,
                        batch_input_shape=batch_input_shape))

        if training and self.batch_augments is not None:
            for batch_aug in self.batch_augments:
                batch_inputs, batch_data_samples = batch_aug(
                    batch_inputs, batch_data_samples)

        return batch_inputs, batch_data_samples
