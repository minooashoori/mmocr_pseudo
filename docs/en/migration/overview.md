# Overview

Along with the release of OpenMMLab 2.0, MMOCR 1.0 made many significant changes, resulting in less redundant, more efficient code and a more consistent overall design. However, these changes break backward compatibility. We understand that with such huge changes, it is not easy for users familiar with the old version to adapt to the new version. Therefore, we prepared a detailed migration guide to make the transition as smooth as possible so that all users can enjoy the productivity benefits of the new MMOCR and the entire OpenMMLab 2.0 ecosystem.

Next, please read the sections according to your requirements.

- If you want to migrate a model trained in version 0.x to use it directly in version 1.0, please read [Pretrained Model Migration](./model.md).
- If you want to train the model, please read [Dataset Migration](./dataset.md) and [Data Transform Migration](./transforms.md).
- If you want to develop on MMOCR, please read [Code Migration](code.md) and [Upstream Library Changes](https://github.com/open-mmlab/mmengine/tree/main/docs/en/migration).
