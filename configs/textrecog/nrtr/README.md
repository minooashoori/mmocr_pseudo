# NRTR

> [NRTR: A No-Recurrence Sequence-to-Sequence Model For Scene Text Recognition](https://arxiv.org/abs/1806.00926)

<!-- [ALGORITHM] -->

## Abstract

Scene text recognition has attracted a great many researches due to its importance to various applications. Existing methods mainly adopt recurrence or convolution based networks. Though have obtained good performance, these methods still suffer from two limitations: slow training speed due to the internal recurrence of RNNs, and high complexity due to stacked convolutional layers for long-term feature extraction. This paper, for the first time, proposes a no-recurrence sequence-to-sequence text recognizer, named NRTR, that dispenses with recurrences and convolutions entirely. NRTR follows the encoder-decoder paradigm, where the encoder uses stacked self-attention to extract image features, and the decoder applies stacked self-attention to recognize texts based on encoder output. NRTR relies solely on self-attention mechanism thus could be trained with more parallelization and less complexity. Considering scene image has large variation in text and background, we further design a modality-transform block to effectively transform 2D input images to 1D sequences, combined with the encoder to extract more discriminative features. NRTR achieves state-of-the-art or highly competitive performance on both regular and irregular benchmarks, while requires only a small fraction of training time compared to the best model from the literature (at least 8 times faster).

<div align=center>
<img src="https://user-images.githubusercontent.com/22607038/142797203-d9df6c35-868f-4848-8261-c286751fd342.png"/>
</div>

## Dataset

### Train Dataset

| trainset  | instance_num | repeat_num | source |
| :-------: | :----------: | :--------: | :----: |
| SynthText |   7266686    |     1      | synth  |
|  Syn90k   |   8919273    |     1      | synth  |

### Test Dataset

| testset | instance_num |   type    |
| :-----: | :----------: | :-------: |
| IIIT5K  |     3000     |  regular  |
|   SVT   |     647      |  regular  |
|  IC13   |     1015     |  regular  |
|  IC15   |     2077     | irregular |
|  SVTP   |     645      | irregular |
|  CT80   |     288      | irregular |

## Results and Models

Coming Soon!

|                               Methods                                |   Backbone   |        | Regular Text |      |     |      | Irregular Text |      |         download         |
| :------------------------------------------------------------------: | :----------: | :----: | :----------: | :--: | :-: | :--: | :------------: | :--: | :----------------------: |
|                                                                      |              | IIIT5K |     SVT      | IC13 |     | IC15 |      SVTP      | CT80 |                          |
| [NRTR](/configs/textrecog/nrtr/nrtr_resnet31-1by16-1by8_6e_st_mj.py) | R31-1/16-1/8 |        |              |      |     |      |                |      | [model](<>) \| [log](<>) |
| [NRTR](/configs/textrecog/nrtr/nrtr_resnet31-1by8-1by4_6e_st_mj.py)  | R31-1/8-1/4  |        |              |      |     |      |                |      | [model](<>) \| [log](<>) |

## Citation

```bibtex
@inproceedings{sheng2019nrtr,
  title={NRTR: A no-recurrence sequence-to-sequence model for scene text recognition},
  author={Sheng, Fenfen and Chen, Zhineng and Xu, Bo},
  booktitle={2019 International Conference on Document Analysis and Recognition (ICDAR)},
  pages={781--786},
  year={2019},
  organization={IEEE}
}
```
