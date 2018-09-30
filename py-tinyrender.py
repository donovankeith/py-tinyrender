# Imports
from PIL import Image
import os.path

class Model:
    def __init__(self, filename):
        self.filename = filename

        self.points = []
        self.vertex_normals = []
        self.uv_points = []

        self.polygons = []
        self.uv_polygons = []
        self.polygon_normals = []

        script_dir = os.path.dirname(__file__)
        self.file_path = os.path.join(script_dir, 'obj', filename)

        with open(self.file_path) as f:
            for line in f:
                # Find lines of pattern `v 1.0 1.0 1.0`
                # TODO: Add support for x,y,z,[w]
                chunks = line.split()
                if len(chunks) == 4:
                    typeToken = chunks[0]

                    # Vertices
                    if typeToken == 'v':
                        point = [
                            float(chunks[1]),
                            float(chunks[2]),
                            float(chunks[3])
                        ]
                        self.points.append(point)
                    # Vertex Normals
                    elif typeToken == 'vt':
                        vertex_normal = [
                            float(chunks[1]),
                            float(chunks[2]),
                            float(chunks[3])
                        ]
                        self.vertex_normals.append(vertex_normal)
                    # UVW Point Coordinates
                    elif typeToken == 'vp':
                        uv_point = [
                            float(chunks[1]),
                            float(chunks[2]),
                            float(chunks[3])
                        ]
                        self.uv_points.append(uv_point)
                    # Faces
                    elif typeToken == 'f':
                        #TODO: Add support for NGons
                        # Matching: f 1148/908/1295 1149/907/1294 1150/906/1293
                        # [Vertex Indices] [UV Point Indices] [Vertex Normal Indices]

                        polygon_chunks = chunks[1].split('/')

                        polygon = [int(polygon_chunks[0]), int(polygon_chunks[1]), int(polygon_chunks[2])]
                        self.polygons.append(polygon)

                        uv_chunks = chunks[2].split('/')
                        uv_polygon = [uv_chunks[0], uv_chunks[1], uv_chunks[2]]
                        self.uv_polygons.append(uv_polygon)

                        normal_chunks = chunks[3].split('/')
                        polygon_normal = [normal_chunks[0], normal_chunks[1], normal_chunks[2]]
                        self.polygon_normals.append(polygon_normal)

        print ("POINTS")
        for point in self.points:
            print(point)

        print("POLYGONS")
        for polygon in self.polygons:
            print(polygon)

def draw_point(x, y, pixels, color):
    pixels[int(x), int(y)] = color

def draw_line(x0, y0, x1, y1, pixels, color):
    """Draws a line on `pixels` from (x0, y0) to (x1, y1) in `color`.

    Starts at (x0, y0) and then walks in small steps towards (x1, y1)
    """

    x_steps = abs(x1 - x0)
    y_steps = abs(y1 - y0)

    # Might result in drawing too many or too few pixels, but it seems like a reasonable compromise.
    steps = int(x_steps + y_steps)

    for step in range(steps):
        t = step/steps

        x = x0 + (x1-x0) * t
        y = y0 + (y1-y0) * t

        pixels[int(x), int(y)] = color

def main():
    # Image Size
    image_width = 1024
    image_height = 1024

    image = Image.new('RGB', (image_width, image_height), "black")
    pixels = image.load()

    # Preset colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

    model = Model("businessWoman.obj")

    to_pixel_scalar = 1.0 / 37.5 * 1024.0

    # Draw line connecting all points in sequence
    for a, b in zip(model.points[:-1], model.points[1:]):
        draw_line(a[0] * to_pixel_scalar, a[1] * to_pixel_scalar, b[0] * to_pixel_scalar, b[1] * to_pixel_scalar, pixels, blue)
    #
    # for polygon in model.polygons:
    #     a, b, c = polygon

    # Overlay points on top
    for point in model.points:
        draw_point(point[0]*to_pixel_scalar, point[1]*to_pixel_scalar, pixels, green)

    # Flip Top/Bottom so that drawing is done in more intuitive directions.
    image.transpose(Image.FLIP_LEFT_RIGHT)

    image.show()

if __name__ == "__main__":
    main()
