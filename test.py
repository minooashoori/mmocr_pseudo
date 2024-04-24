from mmocr.apis import MMOCRInferencer
import mmengine

save_dir = 'test_output/'

ocr = MMOCRInferencer(det='DBNetpp', device='cuda:0')

ocr('7270332546569817350-1_1.jpg', out_dir='test_output/', save_pred=True, save_vis=True)
