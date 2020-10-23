import pytest

from qgis_headless import Style


@pytest.mark.parametrize('file, expected', (
    pytest.param('contour-simple.qml', (), id='contour-simple'),
    pytest.param('contour-rgb.qml', ('level', ), id='contour-rgb'),
    pytest.param('attributes/osm-highway.qml', ('HIGHWAY', 'NAME_EN', 'NAME'), id='osm-highway'),
    pytest.param('attributes/data-defined.qml', ('size', ), id='osm-highway'),
))
def test_sample(file, expected, shared_datadir):
    style = Style.from_file(str(shared_datadir / file))
    assert style.used_attributes() == set(expected)