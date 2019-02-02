from skimage import segmentation, color
from skimage.future import graph
import numpy as np
from .segmentation import Segment, Box, box_to_segment, NULL_COLOR
from .color_mod import ColorGenerator
from .image_utils import image_resize, composition_level
from math import sqrt, pi, atan, cos, sin
from .shared_variables import MAX_SEGMENT_RATIO, GRAVITY, INFINITY, image_size_relation


class BaseTransformer:
    """
    This is the image class representation
    """

    def __init__(self, image, google_vision_data=False):
        """
        This is the class constructor
        """

        if not isinstance(image, np.ndarray) or image.ndim != 3 or image.shape[2] != 3:
            raise Exception('`image` MUST be a numpy array '
                            'with 3 dimensions %s'.format(image))

        # Image to save
        self.image = image

        # Set height and width
        self.height = image.shape[0]
        self.width = image.shape[1]

        # Segments
        self.segments = None

        # image Palette
        self.palette = None

        self.n_segments = 0

        self.balance = 0

        self.segment_ratio = 0

        self.force = {}

        self.max_force = None
        self.min_force = None

        self.google_vision_data = google_vision_data

    def calculate_colors(self, n_colors):
        """
        Returns an instance of the palette class
        """
        if self.palette is None:
            colors = []
            for i in range(self.height):
                for j in range(self.width):
                    colors.append(self.image[i][j])
            self.palette = ColorGenerator(colors, n_colors)
            self.palette.generate()
        else:
            raise Exception('Palette has already been calculated '
                            'please refer to get_palette instead')

    def get_palette(self):
        if self.palette is None:
            raise Exception('Palette is not set '
                            'please refer to calculate_colors instead')

        return self.palette.get_palette()

    def get_harmonized_palette(self):
        if self.palette is None:
            raise Exception('Palette is not set '
                            'please refer to calculate_colors instead')

        return self.palette.get_harmonized_palette()

    @staticmethod
    def _eucledian_diff(arr_a, arr_b):
        if len(arr_a) != len(arr_b):
            raise Exception("Arrays have different lengths")
        diff = 0.0
        for a, b in zip(arr_a, arr_b):
            diff += (b - a) ** 2

        return sqrt(diff)

    def get_color_positions(self):
        resize_value = 2
        reduced_image = image_resize(self.image, width=int(self.width / resize_value))
        positions = []
        differences = []
        for i in range(0, self.palette.n_colors):
            positions.append([0, 0])
            differences.append(INFINITY)
        tmp_colors = self.palette.palette_colors.astype(np.float32).reshape(-1, 3).tolist()
        margin = 20
        i = margin
        while i < reduced_image.shape[0] - margin:
            j = margin
            while j < reduced_image.shape[1] - margin:
                im_color = reduced_image[i][j]
                for k in range(len(tmp_colors)):
                    diff = self._eucledian_diff(im_color, tmp_colors[k])
                    if diff < differences[k]:
                        positions[k][1] = (i * resize_value) / self.height
                        positions[k][0] = (j * resize_value) / self.width
                        differences[k] = diff
                j += 1
            i += 1

        return positions

    def segment(self, objects, faces, compactness=50, n_segments=100,
                connectivity=1, sigma=500, num_cuts=200):

        """
        Function responable of image segmentation
        """
        if self.segments is None:
            # Make segmentation slice
            labels1 = segmentation.slic(self.image,
                                        compactness=compactness,
                                        n_segments=n_segments)

            # Convert slice into rgb image based on avg
            out1 = color.label2rgb(labels1, self.image, kind='avg')

            # Complete segmentation using graph cut
            g = graph.rag_mean_color(self.image, labels1, mode='similarity', connectivity=connectivity, sigma=sigma)
            labels = graph.cut_normalized(labels1, g, num_cuts=num_cuts)

            image_segmentation = color.label2rgb(labels, self.image, kind='avg')
            self._set_boxes(labels, objects, faces)

    def _google_vision_detection(self, objects, faces):
        # save each segment into categories
        # (convert google data into usable data)
        # First convert the Faces
        for face in faces:
            if face.detection_confidence >= 0.8:
                print("Enter face")
                face_positions = face.bounding_poly.vertices
                face_size = abs((face_positions[0].x - face_positions[2].x) * (
                            face_positions[0].y - face_positions[2].y)) * image_size_relation
                # if face size is bigger than image
                print("facesize:", face_size)
                if (face_size / (self.height * self.width)) > 0.16:
                    print("Inside eyes")
                    eye_width = abs((face_positions[0].x - face_positions[2].x) / 5) * image_size_relation
                    eye_height = abs((face_positions[0].y - face_positions[2].y) / 7) * image_size_relation
                    eye_size = eye_height * eye_width

                    # left eye
                    left_eye = face.landmarks[0].position
                    left_box = Box(self.height, self.width)
                    tmp_color = NULL_COLOR
                    tmp_color[0] *= eye_size
                    tmp_color[1] *= eye_size
                    tmp_color[2] *= eye_size
                    left_box._average_color = tmp_color.copy()
                    left_box.size = eye_size
                    left_box.max = [int(left_eye.x*image_size_relation + eye_width), int(left_eye.y*image_size_relation + eye_height)]
                    left_box.min = [int(left_eye.x*image_size_relation - eye_width), int(left_eye.y*image_size_relation - eye_height)]
                    self.max_force, self.min_force, seg = box_to_segment(left_box, self.max_force, self.min_force)
                    self.segments.append(seg)
                    # right eye
                    right_eye = face.landmarks[1].position
                    right_box = Box(self.height, self.width)
                    right_box._average_color = tmp_color.copy()
                    right_box.size = eye_size
                    right_box.max = [int(right_eye.x*image_size_relation + eye_width), int(right_eye.y*image_size_relation + eye_height)]
                    right_box.min = [int(right_eye.x*image_size_relation - eye_width), int(right_eye.y*image_size_relation - eye_height)]
                    self.max_force, self.min_force, seg = box_to_segment(right_box, self.max_force, self.min_force)
                    self.segments.append(seg)
                    # mouth
                    mouth = face.landmarks[12].position
                    mouth_width = abs((face_positions[0].x - face_positions[2].x) / 5) * image_size_relation
                    mouth_height = abs((face_positions[0].y - face_positions[2].y) / 8) * image_size_relation
                    mouth_size = mouth_height * mouth_width
                    mouth_box = Box(self.height, self.width)
                    tmp_color = NULL_COLOR
                    tmp_color[0] *= mouth_size
                    tmp_color[1] *= mouth_size
                    tmp_color[2] *= mouth_size
                    mouth_box._average_color = tmp_color.copy()
                    mouth_box.size = mouth_size
                    mouth_box.max = [int(mouth.x*image_size_relation + mouth_width), int(mouth.y*image_size_relation + mouth_height)]
                    mouth_box.min = [int(mouth.x*image_size_relation - mouth_width), int(mouth.y*image_size_relation - mouth_height)]
                    self.max_force, self.min_force, seg = box_to_segment(mouth_box, self.max_force, self.min_force)
                    self.segments.append(seg)

                else:
                    # calculate avg_color
                    print("Outside")
                    avg_color = [0, 0, 0]
                    face_positions[0].y = int(face_positions[0].y * image_size_relation)
                    face_positions[2].y = int(face_positions[2].y * image_size_relation)
                    face_positions[2].x = int(face_positions[2].x * image_size_relation)
                    face_positions[0].x = int(face_positions[0].x * image_size_relation)
                    for i in range(face_positions[0].y, face_positions[2].y):
                        for j in range(face_positions[0].x, face_positions[2].x):
                            avg_color[0] += self.image[i][j][0]
                            avg_color[1] += self.image[i][j][1]
                            avg_color[2] += self.image[i][j][2]
                    print("Color: ", avg_color)
                    print("Size: ", face_size)
                    face_box = Box(self.height, self.width)
                    face_box._average_color = avg_color
                    face_box.size = face_size
                    face_box.max = [face_positions[2].x, face_positions[2].y]
                    face_box.min = [face_positions[0].x, face_positions[0].y]
                    print("MaxVertex: ", face_box.max)
                    print("MinVertex: ", face_box.min)
                    self.max_force, self.min_force, seg = box_to_segment(face_box, self.max_force, self.min_force)
                    print("Weight", seg.weight)
                    self.segments.append(seg)

        #  Convert objects and delete if there is a face in the same pos
        for obj in objects:
            if obj.score >= 0.8:
                bounding_polygon = obj.bounding_poly.normalized_vertices
                min_pos = [0, 0]
                if bounding_polygon[0]:
                    min_pos = [int(bounding_polygon[0].x * self.width), int(bounding_polygon[0].y * self.height)]
                max_pos = [int(bounding_polygon[2].x * self.width), int(bounding_polygon[2].y * self.height)]
                obj_height = max_pos[1] - min_pos[1]
                obj_width = max_pos[0] - min_pos[0]
                relative_size = (obj_height * obj_width) / (self.height * self.width)
                if relative_size < 0.2:
                    avg_color = [0, 0, 0]
                    size = 0
                    for i in range(min_pos[1], max_pos[1]):
                        for j in range(min_pos[0], max_pos[0]):
                            size += 1
                            avg_color[0] += self.image[i][j][0]
                            avg_color[1] += self.image[i][j][1]
                            avg_color[2] += self.image[i][j][2]
                    object_box = Box(self.height, self.width)
                    object_box._average_color = avg_color
                    object_box.size = size
                    object_box.max = max_pos
                    object_box.min = min_pos
                    self.max_force, self.min_force, seg = box_to_segment(object_box, self.max_force, self.min_force)
                    self.segments.append(seg)

    def _set_boxes(self, labels, objects, faces):
        """
        Calculates every bounding box
        """
        # Convert labels to bounding boxes and segments
        boxes = {}
        segments_size = 0
        for i in range(0, labels.shape[0]):
            for j in range(0, labels.shape[1]):
                c = labels[i][j]
                if boxes.get(c) is None:
                    boxes[c] = (Box(self.height, self.width))
                boxes[c].add([j, i], self.image[i, j])

        # Calculate each segment
        self.segments = []
        self.force = {'x': 0, 'y': 0, 'mod': 0}
        self.max_force = 0
        self.min_force = float('inf')
        for b in boxes:
            if boxes[b].max != [self.height, self.width] and boxes[b].min != [0, 0]:
                w = boxes[b].weight
                w['x'] *= 0.4
                w['y'] *= 0.4
                mod = sqrt(w['x']**2 + w['y']**2)
                if (mod / boxes[b].size) > self.max_force:
                    self.max_force = (mod / boxes[b].size)
                if (mod / boxes[b].size) < self.min_force:
                    self.min_force = (mod / boxes[b].size)
                self.segments.append(Segment(boxes[b], (mod / boxes[b].size)))
                segments_size += boxes[b].size
                self.force['x'] += w['x']
                self.force['y'] += w['y']
        # use google data, my slower performance but improve segmentation
        if self.google_vision_data:
            self._google_vision_detection(objects, faces)

        # Calculate weight of all the segments
        if len(self.segments) > 1:
            for seg in self.segments:
                seg.weight = (seg.weight - self.min_force) / (self.max_force - self.min_force) / 2 + 0.5
        elif len(self.segments) > 0:
            self.segments[0].weight = 1
        self.segment_ratio = (segments_size / (self.width * self.height)) * 100
        self.n_segments = len(self.segments)
        self.force['mod'] = sqrt(self.force['x'] ** 2 + self.force['y'] ** 2)
        if self.segment_ratio < MAX_SEGMENT_RATIO:
            self.force['x'] = -self.force['x']
            self.force['y'] = -self.force['y']
        self.balance = composition_level(self.force['mod'])

    def get_balance_attributes(self):
        # Generates sample image with bounding boxes
        div = 2
        f = int(sqrt((self.width / div) ** 2 + (self.height / div) ** 2)) / 2
        weight_dir = {"x": 0, "y": 0}
        angle_x = angle_y = 0
        if self.force['x'] == 0:
            angle_x = 0
            angle_y = 1
        elif not (self.force['x'] == self.force['y'] == 0):
            angle = atan(self.force['y'] / float(self.force['x']))
            angle_x = cos(angle)
            angle_y = sin(angle)
        weight_dir['x'] = f * angle_x
        weight_dir['y'] = f * angle_y
        if (self.force['x'] < 0 and weight_dir['x'] > 0) or (self.force['x'] > 0 and weight_dir['x'] < 0):
            weight_dir['x'] = -weight_dir['x']
        if (self.force['y'] < 0 and weight_dir['y'] > 0) or (self.force['y'] > 0 and weight_dir['y'] < 0):
            weight_dir['y'] = -weight_dir['y']

        mass = self.force['mod'] / (f * GRAVITY)
        size = mass
        radius = sqrt(mass / pi)
        pos_x = weight_dir['x'] + self.width / 2
        pos_y = self.height / 2 - weight_dir['y']
        return size, radius, pos_x, pos_y, weight_dir

    def get_segments(self):
        if self.segments is None:
            raise Exception('Segments are not set '
                            'please refer to segment instead')
        a = []
        for seg in self.segments:
            a.append((seg.x / self.width, seg.y / self.height,
                      seg.get_weight(), seg.get_scale()[0] / self.width,
                      seg.get_scale()[1] / self.width))
        return a

    def get_balanced_segments(self):
        if self.segments is None:
            raise Exception('Segments are not set '
                            'please refer to segment instead')
        balanced = self.get_segments()
        if self.force['mod'] > 20:
            size, radius, pos_x, pos_y, weight_dir = self.get_balance_attributes()
            weight_dir['mod'] = sqrt(weight_dir['x']**2 + weight_dir['y']**2)
            if size == 0:  # uknown erro
                raise Exception("Balanced circle is empty")
            if self.min_force == self.max_force:  # Only 1 segment
                weight = 0.5
            if self.max_force != self.min_force and size > 0:
                weight = ((weight_dir['mod'] / size) - self.min_force) / (self.max_force - self.min_force) / 2 + 0.5
            if self.segment_ratio >= MAX_SEGMENT_RATIO:
                weight = 0
            balanced.append((pos_x / self.width, pos_y / self.height,
                             weight, radius / self.width,
                             radius / self.width))
        return balanced

    def composition(self):
        return self.balance

    def harmony(self):
        return self.palette.harmony
