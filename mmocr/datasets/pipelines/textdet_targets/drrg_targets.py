import cv2
import numpy as np
from numpy.linalg import norm

import mmocr.utils.check_argument as check_argument
from mmdet.core import BitmapMasks
from mmdet.datasets.builder import PIPELINES
# from mmocr.models.textdet import la_nms
from .textsnake_targets import TextSnakeTargets


@PIPELINES.register_module()
class DRRGTargets(TextSnakeTargets):
    """Generate the ground truth targets of DRRG: Deep Relational Reasoning
    Graph Network for Arbitrary Shape Text Detection.

    [https://arxiv.org/abs/2003.07493]. This was partially adapted from
    https://github.com/GXYM/DRRG.

    Args:
        orientation_thr (float): The threshold for distinguishing between
            head edge and tail edge among the horizontal and vertical edges
            of a quadrangle.
        resample_step (float): The step size for resampling the text center
            line (TCL). Better not exceed half of the minimum width
            of the text component.
        min_comp_num (int): The minimum number of text components, which
            should be k_hop1 + 1 on graph.
        max_comp_num (int): The maximum number of text components.
        min_width (float): The minimum width of text components.
        max_width (float): The maximum width of text components.
        center_region_shrink_ratio (float): The shrink ratio of text center
            region.
        comp_shrink_ratio (float): The shrink ratio of text components.
        text_comp_ratio (float): The reciprocal of aspect ratio of text
            components.
        min_rand_half_height(float): The minimum half-height of random text
            components.
        max_rand_half_height (float): The maximum half-height of random
            text components.
        jitter_level (float): The jitter level of text components geometric
            features.
    """

    def __init__(self,
                 orientation_thr=2.0,
                 resample_step=8.0,
                 min_comp_num=9,
                 max_comp_num=600,
                 min_width=8.0,
                 max_width=24.0,
                 center_region_shrink_ratio=0.3,
                 comp_shrink_ratio=1.0,
                 text_comp_ratio=0.65,
                 text_comp_nms_thr=0.25,
                 min_rand_half_height=6.0,
                 max_rand_half_height=24.0,
                 jitter_level=0.2):

        super().__init__()
        self.orientation_thr = orientation_thr
        self.resample_step = resample_step
        self.max_comp_num = max_comp_num
        self.min_comp_num = min_comp_num
        self.min_width = min_width
        self.max_width = max_width
        self.center_region_shrink_ratio = center_region_shrink_ratio
        self.comp_shrink_ratio = comp_shrink_ratio
        self.text_comp_ratio = text_comp_ratio
        self.text_comp_nms_thr = text_comp_nms_thr
        self.min_rand_half_height = min_rand_half_height
        self.max_rand_half_height = max_rand_half_height
        self.jitter_level = jitter_level

    def dist_point2line(self, pnt, line):

        assert isinstance(line, tuple)
        pnt1, pnt2 = line
        d = abs(np.cross(pnt2 - pnt1, pnt - pnt1)) / (norm(pnt2 - pnt1) + 1e-8)
        return d

    def draw_center_region_maps(self, top_line, bot_line, center_line,
                                center_region_mask, top_height_map,
                                bot_height_map, sin_map, cos_map,
                                region_shrink_ratio):
        """Draw attributes on text center region.

        Args:
            top_line (ndarray): The points composing top curved sideline of
                text polygon.
            bot_line (ndarray): The points composing bottom curved sideline
                of text polygon.
            center_line (ndarray): The points composing the center line of text
                instance.
            center_region_mask (ndarray): The text center region mask.
            top_height_map (ndarray): The map on which the distance from point
                to top sideline will be drawn for each pixel in text center
                region.
            bot_height_map (ndarray): The map on which the distance from point
                to bottom sideline will be drawn for each pixel in text center
                region.
            sin_map (ndarray): The map of vector_sin(top_point -bot_point)
                that will be drawn on text center region.
            cos_map (ndarray): The map of vector_cos(top_point -bot_point)
                will be drawn on text center region.
            region_shrink_ratio (float): The shrink ratio of text center.
        """

        assert top_line.shape == bot_line.shape == center_line.shape
        assert (center_region_mask.shape == top_height_map.shape ==
                bot_height_map.shape == sin_map.shape == cos_map.shape)
        assert isinstance(region_shrink_ratio, float)

        h, w = center_region_mask.shape
        for i in range(0, len(center_line) - 1):

            top_mid_point = (top_line[i] + top_line[i + 1]) / 2
            bot_mid_point = (bot_line[i] + bot_line[i + 1]) / 2

            sin_theta = self.vector_sin(top_mid_point - bot_mid_point)
            cos_theta = self.vector_cos(top_mid_point - bot_mid_point)

            pnt_tl = center_line[i] + (top_line[i] -
                                       center_line[i]) * region_shrink_ratio
            pnt_tr = center_line[i + 1] + (
                top_line[i + 1] - center_line[i + 1]) * region_shrink_ratio
            pnt_br = center_line[i + 1] + (
                bot_line[i + 1] - center_line[i + 1]) * region_shrink_ratio
            pnt_bl = center_line[i] + (bot_line[i] -
                                       center_line[i]) * region_shrink_ratio
            current_center_box = np.vstack([pnt_tl, pnt_tr, pnt_br,
                                            pnt_bl]).astype(np.int32)

            cv2.fillPoly(center_region_mask, [current_center_box], color=1)
            cv2.fillPoly(sin_map, [current_center_box], color=sin_theta)
            cv2.fillPoly(cos_map, [current_center_box], color=cos_theta)

            # x,y order
            current_center_box[:, 0] = np.clip(current_center_box[:, 0], 0,
                                               w - 1)
            current_center_box[:, 1] = np.clip(current_center_box[:, 1], 0,
                                               h - 1)
            min_coord = np.min(current_center_box, axis=0).astype(np.int32)
            max_coord = np.max(current_center_box, axis=0).astype(np.int32)
            current_center_box = current_center_box - min_coord
            sz = (max_coord - min_coord + 1)

            center_box_mask = np.zeros((sz[1], sz[0]), dtype=np.uint8)
            cv2.fillPoly(center_box_mask, [current_center_box], color=1)

            inx = np.argwhere(center_box_mask > 0)
            inx = inx + (min_coord[1], min_coord[0])  # y, x order
            inx_xy = np.fliplr(inx)
            top_height_map[(inx[:, 0], inx[:, 1])] = self.dist_point2line(
                inx_xy, (top_line[i], top_line[i + 1]))
            bot_height_map[(inx[:, 0], inx[:, 1])] = self.dist_point2line(
                inx_xy, (bot_line[i], bot_line[i + 1]))

    def generate_center_mask_attrib_maps(self, img_size, text_polys):
        """Generate text center region mask and geometry attribute maps.

        Args:
            img_size (tuple): The image size of (height, width).
            text_polys (list[list[ndarray]]): The list of text polygons.

        Returns:
            center_lines (list): The list of text center lines.
            center_region_mask (ndarray): The text center region mask.
            top_height_map (ndarray): The distance map from each pixel in text
                center region to top sideline.
            bot_height_map (ndarray): The distance map from each pixel in text
                center region to bottom sideline.
            sin_map (ndarray): The sin(theta) map where theta is the angle
                between vector (top point - bottom point) and vector (1, 0).
            cos_map (ndarray): The cos(theta) map where theta is the angle
                between vector (top point - bottom point) and vector (1, 0).
        """

        assert isinstance(img_size, tuple)
        assert check_argument.is_2dlist(text_polys)

        h, w = img_size

        center_lines = []
        center_region_mask = np.zeros((h, w), np.uint8)
        top_height_map = np.zeros((h, w), dtype=np.float32)
        bot_height_map = np.zeros((h, w), dtype=np.float32)
        sin_map = np.zeros((h, w), dtype=np.float32)
        cos_map = np.zeros((h, w), dtype=np.float32)

        for poly in text_polys:
            assert len(poly) == 1
            polygon_points = poly[0].reshape(-1, 2)
            _, _, top_line, bot_line = self.reorder_poly_edge(polygon_points)
            resampled_top_line, resampled_bot_line = self.resample_sidelines(
                top_line, bot_line, self.resample_step)
            resampled_bot_line = resampled_bot_line[::-1]
            center_line = (resampled_top_line + resampled_bot_line) / 2

            line_head_shrink_len = np.clip(
                (norm(top_line[0] - bot_line[0]) * self.text_comp_ratio),
                self.min_width, self.max_width) / 2
            line_tail_shrink_len = np.clip(
                (norm(top_line[-1] - bot_line[-1]) * self.text_comp_ratio),
                self.min_width, self.max_width) / 2
            head_shrink_num = int(line_head_shrink_len // self.resample_step)
            tail_shrink_num = int(line_tail_shrink_len // self.resample_step)
            if len(center_line) > head_shrink_num + tail_shrink_num + 2:
                center_line = center_line[head_shrink_num:len(center_line) -
                                          tail_shrink_num]
                resampled_top_line = resampled_top_line[
                    head_shrink_num:len(resampled_top_line) - tail_shrink_num]
                resampled_bot_line = resampled_bot_line[
                    head_shrink_num:len(resampled_bot_line) - tail_shrink_num]
            center_lines.append(center_line.astype(np.int32))

            self.draw_center_region_maps(resampled_top_line,
                                         resampled_bot_line, center_line,
                                         center_region_mask, top_height_map,
                                         bot_height_map, sin_map, cos_map,
                                         self.center_region_shrink_ratio)

        return (center_lines, center_region_mask, top_height_map,
                bot_height_map, sin_map, cos_map)

    def generate_comp_attribs_from_maps(self, center_lines, center_region_mask,
                                        top_height_map, bot_height_map,
                                        sin_map, cos_map, comp_shrink_ratio):
        """Generate attributes of text components in accordance with text
        center lines and geometry attribute maps.

        Args:
            center_lines (list[ndarray]): The list of text center lines.
            center_region_mask (ndarray): The text center region mask.
            top_height_map (ndarray): The distance map from each pixel in text
                center region to top sideline.
            bot_height_map (ndarray): The distance map from each pixel in text
                center region to bottom sideline.
            sin_map (ndarray): The sin(theta) map where theta is the angle
                between vector (top point - bottom point) and vector (1, 0).
            cos_map (ndarray): The cos(theta) map where theta is the angle
                between vector (top point - bottom point) and vector (1, 0).
            comp_shrink_ratio (float): The text component shrink ratio.

        Returns:
            comp_attribs (ndarray): All text components attributes(x, y, h, w,
                cos, sin, comp_labels). The comp_labels of two text components
                from the same text instance are equal.
        """

        assert isinstance(center_lines, list)
        assert (center_region_mask.shape == top_height_map.shape ==
                bot_height_map.shape == sin_map.shape == cos_map.shape)
        assert isinstance(comp_shrink_ratio, float)

        center_lines_mask = np.zeros_like(center_region_mask)
        cv2.polylines(center_lines_mask, center_lines, 0, (1, ), 1)
        center_lines_mask = center_lines_mask * center_region_mask
        comp_centers = np.argwhere(center_lines_mask > 0)

        y = comp_centers[:, 0]
        x = comp_centers[:, 1]

        top_height = top_height_map[y, x].reshape((-1, 1)) * comp_shrink_ratio
        bot_height = bot_height_map[y, x].reshape((-1, 1)) * comp_shrink_ratio
        sin = sin_map[y, x].reshape((-1, 1))
        cos = cos_map[y, x].reshape((-1, 1))

        top_mid_x_offset = top_height * cos
        top_mid_y_offset = top_height * sin
        bot_mid_x_offset = bot_height * cos
        bot_mid_y_offset = bot_height * sin

        top_mid_pnt = comp_centers + np.hstack(
            [top_mid_y_offset, top_mid_x_offset])
        bot_mid_pnt = comp_centers - np.hstack(
            [bot_mid_y_offset, bot_mid_x_offset])

        width = (top_height + bot_height) * self.text_comp_ratio
        width = np.clip(width, self.min_width, self.max_width)

        top_left = (top_mid_pnt -
                    np.hstack([width * cos, -width * sin]))[:, ::-1]
        top_right = (top_mid_pnt +
                     np.hstack([width * cos, -width * sin]))[:, ::-1]
        bot_right = (bot_mid_pnt +
                     np.hstack([width * cos, -width * sin]))[:, ::-1]
        bot_left = (bot_mid_pnt -
                    np.hstack([width * cos, -width * sin]))[:, ::-1]
        text_comps = np.hstack([top_left, top_right, bot_right, bot_left])

        score = center_lines_mask[y, x].reshape((-1, 1))
        text_comps = np.hstack([text_comps, score]).astype(np.float32)
        # text_comps = la_nms(text_comps, self.text_comp_nms_thr)

        if text_comps.shape[0] < 1:
            return None

        img_h, img_w = center_region_mask.shape
        text_comps[:, 0:8:2] = np.clip(text_comps[:, 0:8:2], 0, img_w - 1)
        text_comps[:, 1:8:2] = np.clip(text_comps[:, 1:8:2], 0, img_h - 1)

        comp_centers = np.mean(
            text_comps[:, 0:8].reshape((-1, 4, 2)), axis=1).astype(np.int32)
        x = comp_centers[:, 0]
        y = comp_centers[:, 1]

        height = (top_height_map[y, x] + bot_height_map[y, x]).reshape((-1, 1))
        width = np.clip(height * self.text_comp_ratio, self.min_width,
                        self.max_width)

        cos = cos_map[y, x].reshape((-1, 1))
        sin = sin_map[y, x].reshape((-1, 1))

        _, comp_label_mask = cv2.connectedComponents(
            center_region_mask.astype(np.uint8), connectivity=8)
        comp_labels = comp_label_mask[y, x].reshape((-1, 1))

        x = x.reshape((-1, 1))
        y = y.reshape((-1, 1))
        comp_attribs = np.hstack([x, y, height, width, cos, sin, comp_labels])

        return comp_attribs

    def generate_rand_comp_attribs(self, comp_num, center_sample_mask):
        """Generate random text components and their attributes to ensure the
        the number text components in a text image is larger than k_hop1, which
        is the number of one hop neighbors in KNN graph.

        Args:
            comp_num (int): The number of random text components.
            center_sample_mask (ndarray): The text component centers sampling
                region mask.

        Returns:
            rand_comp_attribs (ndarray): The random text components
                attributes(x, y, h, w, cos, sin, belong_instance_label=0).
        """

        assert isinstance(comp_num, int)
        assert comp_num > 0
        assert center_sample_mask.ndim == 2

        h, w = center_sample_mask.shape

        max_rand_half_height = self.max_rand_half_height
        min_rand_half_height = self.min_rand_half_height
        max_rand_height = max_rand_half_height * 2
        max_rand_width = np.clip(max_rand_height * self.text_comp_ratio,
                                 self.min_width, self.max_width)
        margin = int(
            np.sqrt((max_rand_height / 2)**2 + (max_rand_width / 2)**2)) + 1

        if 2 * margin + 1 > min(h, w):

            assert min(h, w) > (np.sqrt(2) * (self.min_width + 1))
            max_rand_half_height = max(min(h, w) / 4, self.min_width / 2 + 1)
            min_rand_half_height = max(max_rand_half_height / 4,
                                       self.min_width / 2)

            max_rand_height = max_rand_half_height * 2
            max_rand_width = np.clip(max_rand_height * self.text_comp_ratio,
                                     self.min_width, self.max_width)
            margin = int(
                np.sqrt((max_rand_height / 2)**2 +
                        (max_rand_width / 2)**2)) + 1

        inner_center_sample_mask = np.zeros_like(center_sample_mask)
        inner_center_sample_mask[margin:h-margin, margin:w-margin] = \
            center_sample_mask[margin:h - margin, margin:w - margin]
        kernel_size = int(min(max(max_rand_half_height, 7), 17))
        inner_center_sample_mask = cv2.erode(
            inner_center_sample_mask,
            np.ones((kernel_size, kernel_size), np.uint8))

        center_candidates = np.argwhere(inner_center_sample_mask > 0)
        center_candidate_num = len(center_candidates)
        sample_inx = np.random.choice(center_candidate_num, comp_num)
        rand_centers = center_candidates[sample_inx]

        rand_top_height = np.random.randint(
            min_rand_half_height,
            max_rand_half_height,
            size=(len(rand_centers), 1))
        rand_bot_height = np.random.randint(
            min_rand_half_height,
            max_rand_half_height,
            size=(len(rand_centers), 1))

        rand_cos = 2 * np.random.random(size=(len(rand_centers), 1)) - 1
        rand_sin = 2 * np.random.random(size=(len(rand_centers), 1)) - 1
        scale = np.sqrt(1.0 / (rand_cos**2 + rand_sin**2 + 1e-8))
        rand_cos = rand_cos * scale
        rand_sin = rand_sin * scale

        height = (rand_top_height + rand_bot_height)
        width = np.clip(height * self.text_comp_ratio, self.min_width,
                        self.max_width)

        rand_comp_attribs = np.hstack([
            rand_centers[:, ::-1], height, width, rand_cos, rand_sin,
            np.zeros_like(rand_sin)
        ])

        return rand_comp_attribs

    def jitter_comp_attribs(self, comp_attribs, jitter_level):
        """Jitter text components attributes.

        Args:
            comp_attribs (ndarray): The text components attributes.
            jitter_level (float): The jitter level of text components
                attributes.

        Returns:
            jittered_comp_attribs (ndarray): The jittered text components
                attributes(x, y, h, w, cos, sin, belong_instance_label).
        """

        assert comp_attribs.shape[1] == 7
        assert comp_attribs.shape[0] > 0
        assert isinstance(jitter_level, float)

        x = comp_attribs[:, 0].reshape((-1, 1))
        y = comp_attribs[:, 1].reshape((-1, 1))
        h = comp_attribs[:, 2].reshape((-1, 1))
        w = comp_attribs[:, 3].reshape((-1, 1))
        cos = comp_attribs[:, 4].reshape((-1, 1))
        sin = comp_attribs[:, 5].reshape((-1, 1))
        belong_label = comp_attribs[:, 6].reshape((-1, 1))

        # max jitter offset of (x, y) should be
        # ((h * abs(cos) + w * abs(sin)) / 2,
        # (h * abs(sin) + w * abs(cos)) / 2)
        x += (np.random.random(size=(len(comp_attribs), 1)) -
              0.5) * (h * np.abs(cos) + w * np.abs(sin)) * jitter_level
        y += (np.random.random(size=(len(comp_attribs), 1)) -
              0.5) * (h * np.abs(sin) + w * np.abs(cos)) * jitter_level

        # max jitter offset of (h, w) should be (h, w)
        h += (np.random.random(size=(len(comp_attribs), 1)) -
              0.5) * h * jitter_level
        w += (np.random.random(size=(len(comp_attribs), 1)) -
              0.5) * w * jitter_level

        # max jitter offset of (cos, sin) should be (1, 1)
        cos += (np.random.random(size=(len(comp_attribs), 1)) -
                0.5) * 2 * jitter_level
        sin += (np.random.random(size=(len(comp_attribs), 1)) -
                0.5) * 2 * jitter_level

        scale = np.sqrt(1.0 / (cos**2 + sin**2 + 1e-8))
        cos = cos * scale
        sin = sin * scale

        jittered_comp_attribs = np.hstack([x, y, h, w, cos, sin, belong_label])

        return jittered_comp_attribs

    def generate_comp_attribs(self, center_lines, text_mask,
                              center_region_mask, top_height_map,
                              bot_height_map, sin_map, cos_map):
        """Generate text components attributes.

        Args:
            center_lines (list[ndarray]): The text center lines list.
            text_mask (ndarray): The text region mask.
            center_region_mask (ndarray): The text center region mask.
            top_height_map (ndarray): The distance map from each pixel in text
                center region to top sideline.
            bot_height_map (ndarray): The distance map from each pixel in text
                center region to bottom sideline.
            sin_map (ndarray): The sin(theta) map where theta is the angle
                between vector (top point - bottom point) and vector (1, 0).
            cos_map (ndarray): The cos(theta) map where theta is the angle
                between vector (top point - bottom point) and vector (1, 0).

        Returns:
            pad_comp_attribs (ndarray): The padded text components attributes
                with a fixed size.
        """

        assert isinstance(center_lines, list)
        assert (text_mask.shape == center_region_mask.shape ==
                top_height_map.shape == bot_height_map.shape == sin_map.shape
                == cos_map.shape)

        comp_attribs = self.generate_comp_attribs_from_maps(
            center_lines, center_region_mask, top_height_map, bot_height_map,
            sin_map, cos_map, self.comp_shrink_ratio)

        if comp_attribs is not None:
            comp_attribs = self.jitter_comp_attribs(comp_attribs,
                                                    self.jitter_level)

            if comp_attribs.shape[0] < self.min_comp_num:
                rand_sample_num = self.min_comp_num - comp_attribs.shape[0]
                rand_comp_attribs = self.generate_rand_comp_attribs(
                    rand_sample_num, 1 - text_mask)
                comp_attribs = np.vstack([comp_attribs, rand_comp_attribs])
        else:
            comp_attribs = self.generate_rand_comp_attribs(
                self.min_comp_num, 1 - text_mask)

        comp_num = (
            np.ones((comp_attribs.shape[0], 1), dtype=np.float32) *
            comp_attribs.shape[0])
        comp_attribs = np.hstack([comp_num, comp_attribs])

        if comp_attribs.shape[0] > self.max_comp_num:
            comp_attribs = comp_attribs[:self.max_comp_num, :]
            comp_attribs[:, 0] = self.max_comp_num

        pad_comp_attribs = np.zeros((self.max_comp_num, comp_attribs.shape[1]))
        pad_comp_attribs[:comp_attribs.shape[0], :] = comp_attribs

        return pad_comp_attribs

    def generate_targets(self, results):
        """Generate the gt targets for DRRG.

        Args:
            results (dict): The input result dictionary.

        Returns:
            results (dict): The output result dictionary.
        """

        assert isinstance(results, dict)

        polygon_masks = results['gt_masks'].masks
        polygon_masks_ignore = results['gt_masks_ignore'].masks

        h, w, _ = results['img_shape']

        gt_text_mask = self.generate_text_region_mask((h, w), polygon_masks)
        gt_mask = self.generate_effective_mask((h, w), polygon_masks_ignore)
        (center_lines, gt_center_region_mask, gt_top_height_map,
         gt_bot_height_map, gt_sin_map,
         gt_cos_map) = self.generate_center_mask_attrib_maps((h, w),
                                                             polygon_masks)

        gt_comp_attribs = self.generate_comp_attribs(center_lines,
                                                     gt_text_mask,
                                                     gt_center_region_mask,
                                                     gt_top_height_map,
                                                     gt_bot_height_map,
                                                     gt_sin_map, gt_cos_map)

        results['mask_fields'].clear()  # rm gt_masks encoded by polygons
        mapping = {
            'gt_text_mask': gt_text_mask,
            'gt_center_region_mask': gt_center_region_mask,
            'gt_mask': gt_mask,
            'gt_top_height_map': gt_top_height_map,
            'gt_bot_height_map': gt_bot_height_map,
            'gt_sin_map': gt_sin_map,
            'gt_cos_map': gt_cos_map
        }
        for key, value in mapping.items():
            value = value if isinstance(value, list) else [value]
            results[key] = BitmapMasks(value, h, w)
            results['mask_fields'].append(key)

        results['gt_comp_attribs'] = gt_comp_attribs
        return results
