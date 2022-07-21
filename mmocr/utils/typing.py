# Copyright (c) OpenMMLab. All rights reserved.
"""Collecting some commonly used type hint in MMOCR."""

from typing import Dict, List, Optional, Tuple, Union

import torch
from mmengine.config import ConfigDict

from mmocr.data import KIEDataSample, TextDetDataSample, TextRecogDataSample

# Config
ConfigType = Union[ConfigDict, Dict]
OptConfigType = Optional[ConfigType]
MultiConfig = Union[ConfigType, List[ConfigType]]
OptMultiConfig = Optional[MultiConfig]
InitConfigType = Union[Dict, List[Dict]]
OptInitConfigType = Optional[InitConfigType]

# Data
RecSampleList = List[TextRecogDataSample]
DetSampleList = List[TextDetDataSample]
KIESampleList = List[KIEDataSample]
OptRecSampleList = Optional[RecSampleList]
OptDetSampleList = Optional[DetSampleList]
OptKIESampleList = Optional[KIESampleList]

OptTensor = Optional[torch.Tensor]

RecForwardResults = Union[Dict[str, torch.Tensor], List[TextRecogDataSample],
                          Tuple[torch.Tensor], torch.Tensor]

# Visualization
ColorType = Union[str, Tuple, List[str], List[Tuple]]
