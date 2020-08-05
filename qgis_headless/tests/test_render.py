from io import BytesIO
import ctypes
import pytest
from PIL import Image

import qgis_headless
from qgis_headless.util import image_stat


def render_vector(data, style, extent, size):
    image = qgis_headless.renderVector(str(data), style, *(extent + size + (3857, -1)))
    return Image.open(BytesIO(image.to_string()))


def test_contour(fetch, shared_datadir):
    data = shared_datadir / 'contour.geojson'  
    style = (shared_datadir / 'contour-rgb.qml').read_text()

    extent = (9757454.0, 6450871.0, 9775498.0, 6465163.0)

    base = 1024
    size = (base, int(base * (extent[3] - extent[1]) / (extent[2] - extent[0])))

    img = render_vector(data, style, extent, size)
    stat = image_stat(img)

    assert stat.alpha.min == 0, "There are no transparent pixels found"
    assert stat.red.max == 255, "Labels aren't visible"
    assert stat.green.max == 255, "Primary lines aren't visible"
    assert stat.blue.max == 255, "Primary lines aren't visible"

    assert 3 < stat.red.mean < 4
    assert 12 < stat.green.mean < 13
    assert 29 < stat.blue.mean < 30

    # img.save('output.png')