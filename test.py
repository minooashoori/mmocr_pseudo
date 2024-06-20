from mmocr.apis import MMOCRInferencer
import mmengine

save_dir = 'test_outputs/'

ocr = MMOCRInferencer(det='DBNetpp', device='cuda:0')

ocr('COCO_train2014_000000014446.jpg', out_dir='test_output/', save_pred=True, save_vis=True)
