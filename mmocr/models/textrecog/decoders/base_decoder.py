# Copyright (c) OpenMMLab. All rights reserved.
from typing import Dict, List, Optional, Sequence, Union

import torch
from mmcv.runner import BaseModule

from mmocr.core.data_structures import TextRecogDataSample
from mmocr.registry import MODELS


@MODELS.register_module()
class BaseDecoder(BaseModule):
    """Base decoder for text recognition, build the loss and postprocessor.

    Args:
        loss (dict, optional): Config to build loss. Defaults to None.
        postprocessor (dict, optional): Config to build postprocessor.
            Defaults to None.
        init_cfg (dict or list[dict], optional): Initialization configs.
            Defaults to None.
    """

    def __init__(self,
                 loss: Optional[Dict] = None,
                 postprocessor: Optional[Dict] = None,
                 init_cfg: Optional[Union[Dict, List[Dict]]] = None) -> None:
        super().__init__(init_cfg=init_cfg)
        self.loss = None
        self.postprocessor = None

        if loss is not None:
            assert isinstance(loss, dict)
            self.loss = MODELS.build(loss)

        if postprocessor is not None:
            assert isinstance(postprocessor, dict)
            self.postprocessor = MODELS.build(postprocessor)

    def forward_train(
        self,
        feat: Optional[torch.Tensor] = None,
        out_enc: Optional[torch.Tensor] = None,
        datasamples: Optional[Sequence[TextRecogDataSample]] = None
    ) -> torch.Tensor:
        """Forward for training.

        Args:
            feat (torch.Tensor, optional): The feature map from backbone of
                shape :math:`(N, E, H, W)`. Defaults to None.
            out_enc (torch.Tensor, optional): Encoder output. Defaults to None.
            datasamples (Sequence[TextRecogDataSample]): Batch of
                TextRecogDataSample, containing gt_text information. Defaults
                to None.
        """
        raise NotImplementedError

    def forward_test(
        self,
        feat: Optional[torch.Tensor] = None,
        out_enc: Optional[torch.Tensor] = None,
        datasamples: Optional[Sequence[TextRecogDataSample]] = None
    ) -> torch.Tensor:
        """Forward for testing.

        Args:
            feat (torch.Tensor, optional): The feature map from backbone of
                shape :math:`(N, E, H, W)`. Defaults to None.
            out_enc (torch.Tensor, optional): Encoder output. Defaults to None.
            datasamples (Sequence[TextRecogDataSample]): Batch of
                TextRecogDataSample, containing gt_text information. Defaults
                to None.
        """
        raise NotImplementedError

    def forward(self,
                feat: Optional[torch.Tensor] = None,
                out_enc: Optional[torch.Tensor] = None,
                datasamples: Optional[Sequence[TextRecogDataSample]] = None,
                train_mode: bool = True) -> torch.Tensor:
        """

        Args:
            feat (torch.Tensor, optional): The feature map from backbone of
                shape :math:`(N, E, H, W)`. Defaults to None.
            out_enc (torch.Tensor, optional): Encoder output. Defaults to None.
            datasamples (Sequence[TextRecogDataSample]): Batch of
                TextRecogDataSample, containing gt_text information. Defaults
                to None.
            train_mode (bool): Train or test. Defaults to True.

        Returns:
            torch.Tensor: Decoder output
        """
        self.train_mode = train_mode
        if train_mode:
            return self.forward_train(feat, out_enc, datasamples)

        return self.forward_test(feat, out_enc, datasamples)
