# Copyright (c) OpenMMLab. All rights reserved.
from abc import ABCMeta, abstractmethod
from typing import Dict, List, Optional, Tuple, Union

import torch
from mmengine.config import ConfigDict
from mmengine.model.base_model import BaseModel

from mmocr.data import TextRecogDataSample

# Type hint of config data
ConfigType = Union[ConfigDict, dict]
OptConfigType = Optional[ConfigType]
# Type hint of one or more config data
MultiConfig = Union[ConfigType, List[ConfigType]]
OptMultiConfig = Optional[MultiConfig]

ForwardResults = Union[Dict[str, torch.Tensor], List[TextRecogDataSample],
                       Tuple[torch.Tensor], torch.Tensor]
SampleList = List[TextRecogDataSample]
OptSampleList = Optional[SampleList]


class BaseRecognizer(BaseModel, metaclass=ABCMeta):
    """Base class for recognizer.

    Args:
        data_preprocessor (dict or ConfigDict, optional): The pre-process
            config of :class:`BaseDataPreprocessor`.  it usually includes,
            ``pad_size_divisor``, ``pad_value``, ``mean`` and ``std``.
        init_cfg (dict or ConfigDict or List[dict], optional): the config
            to control the initialization. Defaults to None.
    """

    def __init__(self,
                 data_preprocessor: Optional[Union[ConfigDict, dict]] = None,
                 init_cfg: OptMultiConfig = None):
        super().__init__(
            data_preprocessor=data_preprocessor, init_cfg=init_cfg)

    @property
    def with_backbone(self):
        """bool: whether the recognizer has a backbone"""
        return hasattr(self, 'backbone')

    @property
    def with_encoder(self):
        """bool: whether the recognizer has an encoder"""
        return hasattr(self, 'encoder')

    @property
    def with_preprocessor(self):
        """bool: whether the recognizer has a preprocessor"""
        return hasattr(self, 'preprocessor')

    @property
    def with_dictionary(self):
        """bool: whether the recognizer has a dictionary"""
        return hasattr(self, 'dictionary')

    @property
    def with_decoder(self):
        """bool: whether the recognizer has a decoder"""
        return hasattr(self, 'decoder')

    @abstractmethod
    def extract_feat(self, inputs: torch.Tensor) -> torch.Tensor:
        """Extract features from images."""
        pass

    def forward(self,
                batch_inputs: torch.Tensor,
                batch_data_samples: OptSampleList = None,
                mode: str = 'tensor',
                **kwargs) -> ForwardResults:
        """The unified entry for a forward process in both training and test.

        The method should accept three modes: "tensor", "predict" and "loss":

        - "tensor": Forward the whole network and return tensor or tuple of
        tensor without any post-processing, same as a common nn.Module.
        - "predict": Forward and return the predictions, which are fully
        processed to a list of :obj:`DetDataSample`.
        - "loss": Forward and return a dict of losses according to the given
        inputs and data samples.

        Note that this method doesn't handle neither back propagation nor
        optimizer updating, which are done in the :meth:`train_step`.

        Args:
            batch_inputs (torch.Tensor): The input tensor with shape
                (N, C, ...) in general.
            batch_data_samples (list[:obj:`DetDataSample`], optional): The
                annotation data of every samples. Defaults to None.
            mode (str): Return what kind of value. Defaults to 'tensor'.

        Returns:
            The return type depends on ``mode``.

            - If ``mode="tensor"``, return a tensor or a tuple of tensor.
            - If ``mode="predict"``, return a list of :obj:`DetDataSample`.
            - If ``mode="loss"``, return a dict of tensor.
        """
        if mode == 'loss':
            return self.loss(batch_inputs, batch_data_samples, **kwargs)
        elif mode == 'predict':
            return self.predict(batch_inputs, batch_data_samples, **kwargs)
        elif mode == 'tensor':
            return self._forward(batch_inputs, batch_data_samples, **kwargs)
        else:
            raise RuntimeError(f'Invalid mode "{mode}". '
                               'Only supports loss, predict and tensor mode')

    @abstractmethod
    def loss(self, batch_inputs: torch.Tensor, batch_data_samples: SampleList,
             **kwargs) -> Union[dict, tuple]:
        """Calculate losses from a batch of inputs and data samples."""
        pass

    @abstractmethod
    def predict(self, batch_inputs: torch.Tensor,
                batch_data_samples: SampleList, **kwargs) -> SampleList:
        """Predict results from a batch of inputs and data samples with post-
        processing."""
        pass

    @abstractmethod
    def _forward(self,
                 batch_inputs: torch.Tensor,
                 batch_data_samples: OptSampleList = None,
                 **kwargs):
        """Network forward process.

        Usually includes backbone, neck and head forward without any post-
        processing.
        """
        pass
