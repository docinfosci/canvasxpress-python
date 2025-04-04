import pytest

from canvasxpress.canvas import CanvasXpress, _DEFAULT_JS_URL, _DEFAULT_CSS_URL
from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXString, CXList
from canvasxpress.data.keypair import CXDictData
from canvasxpress.js.collection import CXEvents
from canvasxpress.js.function import CXEvent


def test_cdn_edition():
    CanvasXpress.set_cdn_edition("2.3")
    assert CanvasXpress.cdn_edition() == "2.3"

    CanvasXpress.set_cdn_edition(None)
    assert CanvasXpress.cdn_edition() == None


def test_js_library_url():
    CanvasXpress.set_js_library_url("https://localhost:8080/asset")
    assert CanvasXpress.js_library_url() == "https://localhost:8080/asset"

    CanvasXpress.set_js_library_url(None)
    assert CanvasXpress.js_library_url() == _DEFAULT_JS_URL


def test_css_library_url():
    CanvasXpress.set_css_library_url("https://localhost:8080/asset")
    assert CanvasXpress.css_library_url() == "https://localhost:8080/asset"

    CanvasXpress.set_css_library_url(None)
    assert CanvasXpress.css_library_url() == _DEFAULT_CSS_URL


def test_CanvasXpress_init():
    subject: CanvasXpress = CanvasXpress(render_to="this_is_a_test")
    assert subject.render_to == "this_is_a_test"

    raw_sample = {"a": [1]}
    data_sample = CXDictData(raw_sample)
    subject: CanvasXpress = CanvasXpress(data=raw_sample)
    assert subject.data == data_sample
    subject: CanvasXpress = CanvasXpress(data=data_sample)
    assert subject.data == data_sample

    raw_sample = CXEvent("test", "x = 1")
    data_sample = CXEvents(raw_sample)
    subject: CanvasXpress = CanvasXpress(events=[raw_sample])
    assert subject.events == data_sample
    subject: CanvasXpress = CanvasXpress(events=data_sample)
    assert subject.events == data_sample

    raw_sample = CXString("label", "value")
    data_sample = CXConfigs(raw_sample)
    subject: CanvasXpress = CanvasXpress(config=[raw_sample])
    assert subject.config == data_sample
    subject: CanvasXpress = CanvasXpress(config=data_sample)
    assert subject.config == data_sample


def test_CanvasXpress_init_kwargs():
    subject: CanvasXpress = CanvasXpress(
        graphType="Bar",
        graphOrientation="vertical",
        renderTo="this_is_a_test",
        afterRender=CXConfigs(CXList("label", ["Gender"])),
    )
    expected_config: CXConfigs = CXConfigs(
        {"graphType": "Bar", "graphOrientation": "vertical"}
    )
    assert subject.config == expected_config
    assert subject.render_to == "this_is_a_test"
    assert subject.after_render == CXConfigs(CXList("label", ["Gender"]))

    subject: CanvasXpress = CanvasXpress(
        config={
            "graphType": "Bar",
            "graphOrientation": "horizontal",
            "title": "Bar chart",
        },
        title="New bar chart",
        graphOrientation="vertical",
    )
    expected_config: CXConfigs = CXConfigs(
        {"graphType": "Bar", "graphOrientation": "vertical", "title": "New bar chart"}
    )
    assert subject.config == expected_config

    with pytest.warns(UserWarning):
        subject: CanvasXpress = CanvasXpress(
            render_to="test1",
            renderTo="this_is_a_test",
        )
    assert subject.render_to == "this_is_a_test"

    with pytest.warns(UserWarning):
        subject: CanvasXpress = CanvasXpress(
            after_render=CXConfigs(CXList("groupSamples", ["Country"])),
            afterRender=CXConfigs(CXList("label", ["Gender"])),
        )
    assert subject.after_render == CXConfigs(CXList("label", ["Gender"]))


def test_CanvasXpress_render_to():
    subject: CanvasXpress = CanvasXpress()
    subject.render_to = "this_is_a_test"
    assert subject.render_to == "this_is_a_test"

    subject: CanvasXpress = CanvasXpress()
    subject.render_to = None
    assert subject.anonymous

    with pytest.raises(TypeError):
        subject: CanvasXpress = CanvasXpress()
        subject.render_to = 1


def test_CanvasXpress_chart_width():
    subject: CanvasXpress = CanvasXpress()
    subject.width = 10
    assert subject.width == 10

    with pytest.raises(ValueError):
        subject: CanvasXpress = CanvasXpress()
        subject.width = None

    with pytest.raises(TypeError):
        subject: CanvasXpress = CanvasXpress()
        subject.width = "test"

    with pytest.raises(ValueError):
        subject: CanvasXpress = CanvasXpress()
        subject.width = -1


def test_CanvasXpress_chart_height():
    subject: CanvasXpress = CanvasXpress()
    subject.height = 10
    assert subject.height == 10

    with pytest.raises(ValueError):
        subject: CanvasXpress = CanvasXpress()
        subject.height = None

    with pytest.raises(TypeError):
        subject: CanvasXpress = CanvasXpress()
        subject.height = "test"

    with pytest.raises(ValueError):
        subject: CanvasXpress = CanvasXpress()
        subject.height = -1


def test_CanvasXpress_data():
    subject: CanvasXpress = CanvasXpress()
    raw_sample = {"a": [1]}
    data_sample = CXDictData(raw_sample)

    subject.data = data_sample
    assert subject.data == data_sample

    subject.data = raw_sample
    assert subject.data == data_sample

    subject.data = None
    assert subject.data == CXDictData()

    with pytest.raises(TypeError):
        subject: CanvasXpress = CanvasXpress()
        subject.data = -1


def test_CanvasXpress_events():
    subject: CanvasXpress = CanvasXpress()
    raw_sample = CXEvent("test", "x = 1")
    data_sample = CXEvents(raw_sample)

    subject.events = data_sample
    assert subject.events == data_sample

    subject.events = [raw_sample]
    assert subject.events == data_sample

    subject.events = None
    assert subject.events == CXEvents()

    with pytest.raises(TypeError):
        subject: CanvasXpress = CanvasXpress()
        subject.events = -1


def test_CanvasXpress_after_render():
    subject: CanvasXpress = CanvasXpress()
    raw_sample = CXList("label", ["Gender"])
    data_sample = CXConfigs(raw_sample)

    subject.after_render = data_sample
    assert subject.after_render == data_sample

    subject.after_render = [raw_sample]
    assert subject.after_render == data_sample

    subject.after_render = None
    assert subject.after_render == CXConfigs()

    with pytest.raises(TypeError):
        subject: CanvasXpress = CanvasXpress()
        subject.after_render = -1


def test_CanvasXpress_config():
    subject: CanvasXpress = CanvasXpress()
    raw_sample = CXString("createPie", "value")
    data_sample = CXConfigs(raw_sample)

    subject.config = data_sample
    assert subject.config == data_sample

    subject.config = [raw_sample]
    assert subject.config == data_sample

    subject.config = None
    assert subject.config == CXConfigs()

    with pytest.raises(TypeError):
        subject: CanvasXpress = CanvasXpress()
        subject.config = -1


def test_CanvasXpress_license():
    subject: CanvasXpress = CanvasXpress()

    assert not subject.license_available
    with pytest.raises(ValueError):
        subject.license_url = "junk"

    assert not subject.license_available
    subject.license_url = "CanvasXpressLicense.js"
    assert subject.license_available

    assert subject.license_available
    subject.license_url = None
    assert not subject.license_available

    assert not subject.render_to_html_parts().get("cx_license")
    subject.license_url = "CanvasXpressLicense.js"
    assert subject.render_to_html_parts().get("cx_license")
    assert "CanvasXpressLicense.js" in subject.render_to_html_parts().get("cx_license")


def test_from_json():
    candidate = CanvasXpress.from_reproducible_json(
        """
        {
          "version": 35,
          "renderTo": "scatter2d11",
          "data": {
            "z": {
              "FC": [3,3,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              "Group": ["Increased","Increased","Decreased","Decreased","Decreased","Decreased","Increased","Decreased","Increased","Increased","Decreased","Decreased","Decreased","Increased","Increased","Increased","Increased","Decreased","Decreased","Decreased","Increased","Decreased","Increased","Increased","Decreased","Increased","Increased","Decreased","Increased","Decreased","Increased","Decreased","Increased","Increased","Decreased","Decreased","Decreased","NoChange","Decreased","Increased","NoChange","Decreased","NoChange","Increased","Decreased","NoChange","Increased","Increased","Decreased","NoChange","Increased","NoChange","Decreased","Decreased","NoChange","Increased","Increased","NoChange","Increased","NoChange","Increased","Decreased","NoChange","NoChange","NoChange","Increased","Decreased","NoChange","Increased","Increased","Increased","Increased","Increased","Decreased","Decreased","Decreased","Decreased","NoChange","NoChange","NoChange","Decreased","Decreased","NoChange","NoChange","Decreased","Decreased","NoChange","Decreased","Increased","Increased","NoChange","Increased","Decreased","NoChange","NoChange","NoChange","Decreased","Decreased","NoChange","NoChange","NoChange","Decreased","NoChange","NoChange","NoChange","NoChange","NoChange","Increased","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","Decreased","NoChange","NoChange","Decreased","Increased","NoChange","Decreased","NoChange","NoChange","Increased","NoChange","Decreased","NoChange","NoChange","Increased","NoChange","NoChange","Increased","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","Decreased","Increased","Decreased","NoChange","NoChange","Increased","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","Increased","NoChange","NoChange","NoChange","Decreased","Increased","Decreased","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","Decreased","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","Decreased","NoChange","NoChange","NoChange","Decreased","NoChange","NoChange","NoChange","NoChange","Increased","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","Decreased","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","Increased","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","Decreased","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","Decreased","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","Decreased","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","Increased","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","Decreased","NoChange","NoChange","NoChange","Decreased","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","Decreased","NoChange","NoChange","NoChange","NoChange","NoChange","Decreased","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","Decreased","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","Increased","NoChange","NoChange","NoChange","NoChange","Increased","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","Increased","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange","NoChange"]
            },
            "y": {
              "smps": ["AveExpr","logFC","-log-pVal"],
              "vars": ["Gene1","Gene2","Gene3","Gene4","Gene5","Gene6","Gene7","Gene8","Gene9","Gene10","Gene11","Gene12","Gene13","Gene14","Gene15","Gene16","Gene17","Gene18","Gene19","Gene20","Gene21","Gene22","Gene23","Gene24","Gene25","Gene26","Gene27","Gene28","Gene29","Gene30","Gene31","Gene32","Gene33","Gene34","Gene35","Gene36","Gene37","Gene38","Gene39","Gene40","Gene41","Gene42","Gene43","Gene44","Gene45","Gene46","Gene47","Gene48","Gene49","Gene50","Gene51","Gene52","Gene53","Gene54","Gene55","Gene56","Gene57","Gene58","Gene59","Gene60","Gene61","Gene62","Gene63","Gene64","Gene65","Gene66","Gene67","Gene68","Gene69","Gene70","Gene71","Gene72","Gene73","Gene74","Gene75","Gene76","Gene77","Gene78","Gene79","Gene80","Gene81","Gene82","Gene83","Gene84","Gene85","Gene86","Gene87","Gene88","Gene89","Gene90","Gene91","Gene92","Gene93","Gene94","Gene95","Gene96","Gene97","Gene98","Gene99","Gene100","Gene101","Gene102","Gene103","Gene104","Gene105","Gene106","Gene107","Gene108","Gene109","Gene110","Gene111","Gene112","Gene113","Gene114","Gene115","Gene116","Gene117","Gene118","Gene119","Gene120","Gene121","Gene122","Gene123","Gene124","Gene125","Gene126","Gene127","Gene128","Gene129","Gene130","Gene131","Gene132","Gene133","Gene134","Gene135","Gene136","Gene137","Gene138","Gene139","Gene140","Gene141","Gene142","Gene143","Gene144","Gene145","Gene146","Gene147","Gene148","Gene149","Gene150","Gene151","Gene152","Gene153","Gene154","Gene155","Gene156","Gene157","Gene158","Gene159","Gene160","Gene161","Gene162","Gene163","Gene164","Gene165","Gene166","Gene167","Gene168","Gene169","Gene170","Gene171","Gene172","Gene173","Gene174","Gene175","Gene176","Gene177","Gene178","Gene179","Gene180","Gene181","Gene182","Gene183","Gene184","Gene185","Gene186","Gene187","Gene188","Gene189","Gene190","Gene191","Gene192","Gene193","Gene194","Gene195","Gene196","Gene197","Gene198","Gene199","Gene200","Gene201","Gene202","Gene203","Gene204","Gene205","Gene206","Gene207","Gene208","Gene209","Gene210","Gene211","Gene212","Gene213","Gene214","Gene215","Gene216","Gene217","Gene218","Gene219","Gene220","Gene221","Gene222","Gene223","Gene224","Gene225","Gene226","Gene227","Gene228","Gene229","Gene230","Gene231","Gene232","Gene233","Gene234","Gene235","Gene236","Gene237","Gene238","Gene239","Gene240","Gene241","Gene242","Gene243","Gene244","Gene245","Gene246","Gene247","Gene248","Gene249","Gene250","Gene251","Gene252","Gene253","Gene254","Gene255","Gene256","Gene257","Gene258","Gene259","Gene260","Gene261","Gene262","Gene263","Gene264","Gene265","Gene266","Gene267","Gene268","Gene269","Gene270","Gene271","Gene272","Gene273","Gene274","Gene275","Gene276","Gene277","Gene278","Gene279","Gene280","Gene281","Gene282","Gene283","Gene284","Gene285","Gene286","Gene287","Gene288","Gene289","Gene290","Gene291","Gene292","Gene293","Gene294","Gene295","Gene296","Gene297","Gene298","Gene299","Gene300","Gene301","Gene302","Gene303","Gene304","Gene305","Gene306","Gene307","Gene308","Gene309","Gene310","Gene311","Gene312","Gene313","Gene314","Gene315","Gene316","Gene317","Gene318","Gene319","Gene320","Gene321","Gene322","Gene323","Gene324","Gene325","Gene326","Gene327","Gene328","Gene329","Gene330","Gene331","Gene332","Gene333","Gene334","Gene335","Gene336","Gene337","Gene338","Gene339","Gene340","Gene341","Gene342","Gene343","Gene344","Gene345","Gene346","Gene347","Gene348","Gene349","Gene350","Gene351","Gene352","Gene353","Gene354","Gene355","Gene356","Gene357","Gene358","Gene359","Gene360","Gene361","Gene362","Gene363","Gene364","Gene365","Gene366","Gene367","Gene368","Gene369","Gene370","Gene371","Gene372","Gene373","Gene374","Gene375","Gene376","Gene377","Gene378","Gene379","Gene380","Gene381","Gene382","Gene383","Gene384","Gene385","Gene386","Gene387","Gene388","Gene389","Gene390","Gene391","Gene392","Gene393","Gene394","Gene395","Gene396","Gene397","Gene398","Gene399","Gene400","Gene401","Gene402","Gene403","Gene404","Gene405","Gene406","Gene407","Gene408","Gene409","Gene410","Gene411","Gene412","Gene413","Gene414","Gene415","Gene416","Gene417","Gene418","Gene419","Gene420","Gene421","Gene422","Gene423","Gene424","Gene425","Gene426","Gene427","Gene428","Gene429","Gene430","Gene431","Gene432","Gene433","Gene434","Gene435","Gene436","Gene437","Gene438","Gene439","Gene440","Gene441","Gene442","Gene443","Gene444","Gene445","Gene446","Gene447","Gene448","Gene449","Gene450","Gene451","Gene452","Gene453","Gene454","Gene455","Gene456","Gene457","Gene458","Gene459","Gene460","Gene461","Gene462","Gene463","Gene464","Gene465","Gene466","Gene467","Gene468","Gene469","Gene470","Gene471","Gene472","Gene473","Gene474","Gene475","Gene476","Gene477","Gene478","Gene479","Gene480","Gene481","Gene482","Gene483","Gene484","Gene485","Gene486","Gene487","Gene488","Gene489","Gene490","Gene491","Gene492","Gene493","Gene494","Gene495","Gene496","Gene497","Gene498","Gene499","Gene500","Gene501","Gene502","Gene503","Gene504","Gene505","Gene506","Gene507","Gene508","Gene509","Gene510","Gene511","Gene512","Gene513","Gene514","Gene515","Gene516","Gene517","Gene518","Gene519","Gene520","Gene521","Gene522","Gene523","Gene524","Gene525","Gene526","Gene527","Gene528","Gene529","Gene530","Gene531","Gene532","Gene533","Gene534","Gene535","Gene536","Gene537","Gene538","Gene539","Gene540","Gene541","Gene542","Gene543","Gene544","Gene545","Gene546","Gene547","Gene548","Gene549","Gene550","Gene551","Gene552","Gene553","Gene554","Gene555","Gene556","Gene557","Gene558","Gene559","Gene560","Gene561","Gene562","Gene563","Gene564","Gene565","Gene566","Gene567","Gene568","Gene569","Gene570","Gene571","Gene572","Gene573","Gene574","Gene575","Gene576","Gene577","Gene578","Gene579","Gene580","Gene581","Gene582","Gene583","Gene584","Gene585","Gene586","Gene587","Gene588","Gene589","Gene590","Gene591","Gene592","Gene593","Gene594","Gene595","Gene596","Gene597","Gene598","Gene599","Gene600","Gene601","Gene602","Gene603","Gene604","Gene605","Gene606","Gene607","Gene608","Gene609","Gene610","Gene611","Gene612","Gene613","Gene614","Gene615","Gene616","Gene617","Gene618","Gene619","Gene620","Gene621","Gene622","Gene623","Gene624","Gene625","Gene626","Gene627","Gene628","Gene629","Gene630","Gene631","Gene632","Gene633","Gene634","Gene635","Gene636","Gene637","Gene638","Gene639","Gene640","Gene641","Gene642","Gene643","Gene644","Gene645","Gene646","Gene647","Gene648","Gene649","Gene650","Gene651","Gene652","Gene653","Gene654","Gene655","Gene656","Gene657","Gene658","Gene659","Gene660","Gene661","Gene662","Gene663","Gene664","Gene665","Gene666","Gene667","Gene668","Gene669","Gene670","Gene671","Gene672","Gene673","Gene674","Gene675","Gene676","Gene677","Gene678","Gene679","Gene680","Gene681","Gene682","Gene683","Gene684","Gene685","Gene686","Gene687","Gene688","Gene689","Gene690","Gene691","Gene692","Gene693","Gene694","Gene695","Gene696","Gene697","Gene698","Gene699","Gene700","Gene701","Gene702","Gene703","Gene704","Gene705","Gene706","Gene707","Gene708","Gene709","Gene710","Gene711","Gene712","Gene713","Gene714","Gene715","Gene716","Gene717","Gene718","Gene719","Gene720","Gene721","Gene722","Gene723","Gene724","Gene725","Gene726","Gene727","Gene728","Gene729","Gene730","Gene731","Gene732","Gene733","Gene734","Gene735","Gene736","Gene737","Gene738","Gene739","Gene740","Gene741","Gene742","Gene743","Gene744","Gene745","Gene746","Gene747","Gene748","Gene749","Gene750","Gene751","Gene752","Gene753","Gene754","Gene755","Gene756","Gene757","Gene758","Gene759","Gene760","Gene761","Gene762","Gene763","Gene764","Gene765","Gene766","Gene767","Gene768","Gene769","Gene770","Gene771","Gene772","Gene773","Gene774","Gene775","Gene776","Gene777","Gene778","Gene779","Gene780","Gene781","Gene782","Gene783","Gene784","Gene785","Gene786","Gene787","Gene788","Gene789","Gene790","Gene791","Gene792","Gene793","Gene794","Gene795","Gene796","Gene797","Gene798","Gene799","Gene800","Gene801","Gene802","Gene803","Gene804","Gene805","Gene806","Gene807","Gene808","Gene809","Gene810","Gene811","Gene812","Gene813","Gene814","Gene815","Gene816","Gene817","Gene818","Gene819","Gene820","Gene821","Gene822","Gene823","Gene824","Gene825","Gene826","Gene827","Gene828","Gene829","Gene830","Gene831","Gene832","Gene833","Gene834","Gene835","Gene836","Gene837","Gene838","Gene839","Gene840","Gene841","Gene842","Gene843","Gene844","Gene845","Gene846","Gene847","Gene848","Gene849","Gene850","Gene851","Gene852","Gene853","Gene854","Gene855","Gene856","Gene857","Gene858","Gene859","Gene860","Gene861","Gene862","Gene863","Gene864","Gene865","Gene866","Gene867","Gene868","Gene869","Gene870","Gene871","Gene872","Gene873","Gene874","Gene875","Gene876","Gene877","Gene878","Gene879","Gene880","Gene881","Gene882","Gene883","Gene884","Gene885","Gene886","Gene887","Gene888","Gene889","Gene890","Gene891","Gene892","Gene893","Gene894","Gene895","Gene896","Gene897","Gene898","Gene899","Gene900","Gene901","Gene902","Gene903","Gene904","Gene905","Gene906","Gene907","Gene908","Gene909","Gene910","Gene911","Gene912","Gene913","Gene914","Gene915","Gene916","Gene917","Gene918","Gene919","Gene920","Gene921","Gene922","Gene923","Gene924","Gene925","Gene926","Gene927","Gene928","Gene929","Gene930","Gene931","Gene932","Gene933","Gene934","Gene935","Gene936","Gene937","Gene938","Gene939","Gene940","Gene941","Gene942","Gene943","Gene944","Gene945","Gene946","Gene947","Gene948","Gene949","Gene950","Gene951","Gene952","Gene953","Gene954","Gene955","Gene956","Gene957","Gene958","Gene959","Gene960","Gene961","Gene962","Gene963","Gene964","Gene965","Gene966","Gene967","Gene968","Gene969","Gene970","Gene971","Gene972","Gene973","Gene974","Gene975","Gene976","Gene977","Gene978","Gene979","Gene980","Gene981","Gene982","Gene983","Gene984","Gene985","Gene986","Gene987","Gene988","Gene989","Gene990","Gene991","Gene992","Gene993","Gene994","Gene995","Gene996","Gene997","Gene998","Gene999","Gene1000"],
              "data": [
                [0.94,1.399,3.5508],
                [0.923,1.917,3.3186],
                [-0.234,-1.15,2.8226],
                [0.326,-1.329,2.7428],
                [0.159,-1.05,2.5841],
                [0.062,-0.896,2.4041],
                [-0.057,1.006,2.1794],
                [0.004,-1.016,2.0992],
                [-0.23,0.816,2.0522],
                [-0.134,1.174,2.0317],
                [0.024,-0.648,2.003],
                [0.298,-0.621,1.999],
                [-0.246,-0.576,1.8406],
                [-0.416,1.327,1.8405],
                [-0.149,0.74,1.8137],
                [0.144,0.624,1.7512],
                [-0.134,0.626,1.7371],
                [-0.25,-0.873,1.716],
                [0.109,-0.944,1.655],
                [0.155,-0.671,1.6509],
                [0.022,0.616,1.633],
                [-0.154,-0.519,1.5754],
                [0.133,0.912,1.5739],
                [0.032,0.692,1.5642],
                [0.215,-0.601,1.5373],
                [-0.052,0.576,1.5266],
                [0.233,0.534,1.5025],
                [0.103,-0.531,1.4939],
                [0.277,0.545,1.4886],
                [0.654,-2.438,1.485],
                [-0.114,0.772,1.4845],
                [-0.179,-0.741,1.4601],
                [-0.002,0.535,1.4464],
                [-0.222,0.809,1.4417],
                [0.113,-0.544,1.4238],
                [0.15,-0.506,1.3955],
                [-0.144,-0.562,1.3811],
                [0.033,-0.458,1.3751],
                [0.165,-0.659,1.35],
                [0.096,0.591,1.3475],
                [-0.022,0.481,1.345],
                [0.025,-0.937,1.3431],
                [-0.337,0.475,1.3338],
                [-0.036,0.687,1.3194],
                [0.07,-0.505,1.3086],
                [0.142,0.491,1.3038],
                [0.209,0.803,1.2919],
                [-0.085,0.647,1.2828],
                [-0.325,-0.721,1.2789],
                [0.158,-0.477,1.2772],
                [0.026,0.56,1.2702],
                [0.182,-0.441,1.266],
                [0.039,-0.654,1.2501],
                [0.146,-0.607,1.2441],
                [-0.101,0.411,1.2361],
                [0.407,0.811,1.2338],
                [-0.117,0.76,1.2275],
                [0.231,0.477,1.2126],
                [0.284,0.648,1.1959],
                [-0.011,0.446,1.1935],
                [-0.063,0.52,1.1886],
                [-0.415,-0.616,1.1866],
                [-0.16,0.49,1.1846],
                [-0.37,0.453,1.1759],
                [0.162,0.436,1.1721],
                [-0.215,0.599,1.168],
                [0.243,-0.502,1.1633],
                [0.021,0.423,1.1593],
                [-0.276,1.169,1.1517],
                [0.004,0.588,1.1509],
                [0.271,1.917,1.1379],
                [0.082,0.578,1.136],
                [0.283,0.556,1.135],
                [-0.187,-0.562,1.1033],
                [-0.171,-0.747,1.0994],
                [-0.012,-0.587,1.0809],
                [0.275,-0.714,1.077],
                [0.004,0.493,1.0752],
                [0.116,0.5,1.0723],
                [-0.025,0.497,1.0669],
                [-0.313,-0.887,1.0642],
                [0.092,-0.546,1.0612],
                [-0.115,0.389,1.0542],
                [0.07,-0.434,1.0519],
                [0.263,-0.513,1.0492],
                [0.432,-0.743,1.0481],
                [0.2,-0.394,1.0424],
                [0.198,-0.617,1.039],
                [-0.13,0.6,1.0334],
                [0.116,0.588,1.0331],
                [0.035,-0.444,1.0305],
                [0.163,0.735,1.0177],
                [0.159,-0.573,1.0128],
                [-0.029,0.37,1.0126],
                [0.01,-0.359,1.0086],
                [0.036,0.401,1.0069],
                [0.44,-0.566,1.0055],
                [0.551,-0.513,1.0011],
                [0.043,-0.327,1.0009],
                [0.054,0.383,0.9932],
                [0.217,-0.459,0.9931],
                [-0.37,-0.569,0.9842],
                [-0.003,0.405,0.9833],
                [-0.258,0.361,0.9802],
                [-0.103,0.379,0.977],
                [0.36,0.36,0.975],
                [-0.095,-0.365,0.9748],
                [-0.339,0.508,0.9725],
                [-0.237,-0.454,0.9693],
                [-0.021,0.398,0.968],
                [0.136,-0.49,0.9668],
                [-0.172,-0.342,0.9589],
                [0.099,-0.353,0.9576],
                [0.084,-0.452,0.9575],
                [0.064,-0.388,0.9564],
                [0.049,0.436,0.9539],
                [0.124,-0.845,0.9511],
                [0.215,-0.39,0.946],
                [-0.218,0.375,0.9429],
                [-0.101,-0.516,0.9397],
                [0.583,1.182,0.9385],
                [0.168,-0.485,0.9366],
                [-0.075,-0.532,0.9346],
                [0.045,0.342,0.9312],
                [0.142,0.375,0.9292],
                [0.275,0.524,0.9255],
                [-0.068,-0.407,0.9246],
                [-0.248,-0.657,0.9214],
                [0.061,0.397,0.921],
                [-0.061,0.486,0.9205],
                [0.276,1.082,0.9184],
                [-0.199,0.323,0.9183],
                [0.06,-0.477,0.9142],
                [0.061,0.514,0.9129],
                [0.007,-0.488,0.9121],
                [0.225,-0.376,0.9091],
                [-0.18,0.496,0.9067],
                [-0.255,-0.461,0.9063],
                [-0.25,0.477,0.9014],
                [0.037,-0.344,0.9011],
                [-0.114,-0.435,0.8959],
                [-0.159,-0.545,0.8911],
                [-0.288,0.84,0.8902],
                [-0.148,-0.506,0.888],
                [0.186,0.44,0.8877],
                [-0.031,0.394,0.8846],
                [0.025,1.034,0.8845],
                [-0.086,-0.362,0.8839],
                [-0.203,0.344,0.8814],
                [0.044,-0.329,0.8775],
                [0.232,0.389,0.8762],
                [0.197,-0.442,0.8746],
                [-0.033,-0.448,0.8719],
                [-0.043,0.407,0.8689],
                [0.376,0.812,0.8661],
                [-0.061,0.378,0.8659],
                [0.349,0.443,0.8622],
                [-0.223,-0.386,0.8605],
                [0.372,-0.535,0.8595],
                [-0.041,0.82,0.8588],
                [0.215,-0.554,0.8561],
                [-0.022,0.456,0.8552],
                [-0.084,0.401,0.8488],
                [-0.044,0.46,0.8475],
                [0.163,-0.312,0.8467],
                [0.034,0.425,0.8448],
                [0.092,-0.391,0.8447],
                [0.173,-0.416,0.844],
                [-0.179,0.293,0.8384],
                [0.094,-0.494,0.8326],
                [0.086,0.327,0.832],
                [0.106,0.344,0.8317],
                [0.081,-0.314,0.8309],
                [0.018,-0.546,0.8268],
                [0.123,-0.327,0.8237],
                [-0.037,-0.489,0.8168],
                [0.045,-0.348,0.8035],
                [0.074,0.329,0.8008],
                [0.281,0.467,0.8001],
                [0.075,-0.454,0.7951],
                [-0.002,-0.398,0.7935],
                [-0.126,-0.3,0.7891],
                [0.044,0.337,0.789],
                [0.209,0.365,0.7881],
                [0.108,0.387,0.7862],
                [-0.088,-0.392,0.7821],
                [-0.05,-0.357,0.7819],
                [-0.05,-0.294,0.778],
                [0.359,-0.411,0.7726],
                [0.115,0.33,0.7707],
                [-0.378,0.444,0.77],
                [0.196,0.428,0.7642],
                [0.077,0.325,0.7593],
                [0.275,-0.39,0.759],
                [0.236,-0.391,0.7552],
                [-0.034,-0.621,0.7476],
                [-0.14,-0.327,0.7472],
                [-0.13,-0.331,0.7434],
                [-0.166,0.469,0.737],
                [0.088,-0.564,0.7297],
                [-0.01,0.407,0.7263],
                [0.164,-0.405,0.7225],
                [-0.123,0.256,0.7184],
                [-0.039,0.426,0.7158],
                [0.32,0.584,0.7149],
                [0.001,0.291,0.7126],
                [0.194,0.414,0.7113],
                [-0.153,-0.284,0.703],
                [0.006,0.293,0.7003],
                [-0.061,0.304,0.6992],
                [-0.129,-0.424,0.6987],
                [0.026,-0.275,0.6971],
                [-0.125,-0.281,0.6936],
                [0.041,-0.364,0.6926],
                [0.047,0.261,0.691],
                [0.039,0.307,0.6849],
                [0.155,-0.422,0.6755],
                [0.135,0.402,0.673],
                [-0.022,0.302,0.6722],
                [-0.294,0.329,0.6702],
                [0.01,-0.392,0.6695],
                [-0.099,-0.32,0.6681],
                [-0.089,-0.345,0.6679],
                [0.027,-0.292,0.6655],
                [0.005,0.291,0.6651],
                [0.007,-0.429,0.6645],
                [-0.006,0.366,0.6608],
                [0.085,0.257,0.6583],
                [-0.142,0.397,0.6574],
                [0.159,-0.28,0.6562],
                [0.232,0.336,0.656],
                [-0.16,-0.684,0.6555],
                [-0.014,0.26,0.6544],
                [-0.155,-0.238,0.6533],
                [-0.047,0.289,0.647],
                [0.226,0.264,0.6464],
                [0.054,-0.275,0.6463],
                [-0.117,-0.265,0.6454],
                [-0.068,0.513,0.645],
                [-0.115,0.322,0.6418],
                [0.1,0.286,0.6417],
                [-0.021,-0.245,0.6406],
                [-0.026,-0.383,0.6401],
                [-0.182,-0.424,0.6394],
                [-0.165,0.251,0.6386],
                [0.186,-0.284,0.6334],
                [-0.009,0.33,0.6322],
                [-0.085,0.344,0.6296],
                [-0.093,0.478,0.6246],
                [0.311,-0.271,0.6215],
                [-0.031,-0.623,0.6211],
                [-0.149,0.362,0.62],
                [-0.029,0.232,0.62],
                [-0.024,-0.24,0.6195],
                [-0.109,-0.342,0.6186],
                [0.318,0.284,0.6179],
                [-0.006,-0.335,0.617],
                [-0.138,0.253,0.6165],
                [0.048,0.238,0.6153],
                [0.113,-0.473,0.6146],
                [-0.067,-0.225,0.6144],
                [-0.263,-0.273,0.6109],
                [0.07,0.231,0.6083],
                [-0.002,-0.323,0.6066],
                [0.2,0.4,0.6041],
                [0.182,-0.232,0.603],
                [-0.948,-1.12,0.5997],
                [0.056,-0.4,0.5933],
                [-0.512,-0.379,0.5924],
                [0.111,0.366,0.5922],
                [-0.18,-0.235,0.592],
                [0.009,0.293,0.5904],
                [-0.204,0.253,0.59],
                [-0.028,0.296,0.5868],
                [0.056,-0.282,0.5848],
                [-0.014,-0.295,0.5815],
                [-0.145,0.234,0.5797],
                [0.004,0.264,0.5794],
                [-0.129,0.273,0.5749],
                [0.226,-0.335,0.5745],
                [0.108,-0.302,0.5723],
                [-0.008,0.388,0.5718],
                [-0.025,-0.254,0.5718],
                [0.033,-0.273,0.5707],
                [0.166,-0.231,0.5687],
                [0.125,0.288,0.5684],
                [0.241,0.35,0.5634],
                [-0.078,0.243,0.5623],
                [0.147,-0.315,0.5573],
                [-0.05,0.345,0.5572],
                [0.015,0.355,0.5565],
                [0.248,-0.262,0.5553],
                [0.013,-0.225,0.5547],
                [-0.008,0.218,0.5534],
                [0.242,0.336,0.5516],
                [0.018,-0.248,0.5507],
                [0.128,0.246,0.5505],
                [-0.18,-0.523,0.5492],
                [0.075,-0.232,0.5488],
                [0.036,0.274,0.5475],
                [0.059,-0.225,0.542],
                [0.075,0.235,0.5402],
                [-0.183,0.279,0.5381],
                [0.009,-0.458,0.5376],
                [-0.055,-0.248,0.5359],
                [0.035,0.371,0.5355],
                [-0.075,0.206,0.534],
                [0.088,0.271,0.533],
                [-0.17,-0.259,0.5327],
                [0.018,-0.232,0.5318],
                [0.063,0.561,0.5302],
                [-0.145,-0.394,0.5289],
                [-0.203,0.261,0.5277],
                [-0.087,0.356,0.5223],
                [-0.255,0.262,0.5217],
                [-0.007,-0.418,0.5203],
                [-0.282,-0.214,0.5198],
                [0,0.217,0.5197],
                [0.133,0.229,0.5174],
                [0.155,-0.223,0.5171],
                [0.069,-0.208,0.5138],
                [-0.006,0.202,0.5118],
                [0.091,-0.559,0.5118],
                [-0.133,0.194,0.51],
                [-0.01,-0.358,0.5076],
                [0.03,-0.224,0.5058],
                [-0.028,-0.715,0.4994],
                [0.017,-0.272,0.4955],
                [0.093,-0.276,0.4928],
                [-0.099,0.198,0.4928],
                [-0.094,-0.269,0.4925],
                [0.071,-0.216,0.4907],
                [0.053,-0.283,0.4902],
                [-0.084,0.267,0.4898],
                [-0.096,0.289,0.4889],
                [0.124,-0.279,0.4866],
                [-0.157,-0.255,0.486],
                [0.088,-0.203,0.4858],
                [0.056,0.202,0.4837],
                [0.29,0.228,0.4832],
                [-0.144,-0.271,0.4784],
                [-0.05,0.217,0.4761],
                [-0.277,-0.232,0.476],
                [0.182,0.235,0.4754],
                [-0.24,-0.251,0.4745],
                [-0.072,0.244,0.4738],
                [0.005,-0.254,0.4726],
                [0.032,-0.292,0.4702],
                [0.212,-0.199,0.4691],
                [-0.139,0.186,0.4679],
                [0.264,0.232,0.4662],
                [-0.085,-0.241,0.466],
                [-0.328,-0.192,0.4637],
                [-0.226,0.411,0.4633],
                [0.032,0.227,0.4621],
                [0.035,0.36,0.4596],
                [-0.109,-0.272,0.459],
                [-0.238,-0.338,0.4561],
                [-0.064,0.242,0.4548],
                [-0.006,-0.22,0.4545],
                [0.448,0.28,0.4526],
                [0.077,0.211,0.4501],
                [0.066,0.238,0.45],
                [0.161,0.183,0.4498],
                [-0.157,0.293,0.4463],
                [0.27,-0.622,0.4458],
                [-0.043,-0.186,0.4457],
                [0.158,-0.196,0.4411],
                [0.126,-0.297,0.4399],
                [0.084,-0.209,0.4381],
                [0.061,-0.207,0.4375],
                [0.042,-0.581,0.4371],
                [-0.101,0.235,0.4353],
                [-0.097,-0.35,0.4312],
                [-0.035,-0.21,0.4311],
                [0.005,-0.181,0.431],
                [0.074,-0.2,0.4305],
                [-0.11,0.35,0.4296],
                [-0.157,-0.499,0.4287],
                [-0.056,-0.276,0.4263],
                [0.014,-0.29,0.4263],
                [-0.125,0.21,0.4252],
                [-0.376,-0.381,0.4244],
                [0.037,0.245,0.4237],
                [-0.05,0.267,0.4229],
                [0.056,-0.215,0.4206],
                [0.218,-0.332,0.4206],
                [-0.127,0.224,0.4204],
                [-0.026,0.398,0.4179],
                [0.137,-0.371,0.417],
                [-0.162,-0.534,0.4161],
                [0.147,-0.205,0.4153],
                [-0.046,0.249,0.4123],
                [0.147,-0.204,0.4113],
                [-0.054,0.186,0.4104],
                [0.063,0.194,0.4102],
                [0.012,-0.257,0.4102],
                [-0.098,-0.244,0.4088],
                [1.222,0.554,0.4079],
                [0.025,0.186,0.4057],
                [-0.021,-0.196,0.4035],
                [-0.064,0.253,0.4016],
                [-0.095,0.211,0.4008],
                [-0.159,0.901,0.3978],
                [0.201,0.455,0.3969],
                [0.037,0.21,0.3962],
                [0.018,-0.177,0.396],
                [0.047,0.177,0.3957],
                [-0.014,-0.228,0.3954],
                [0.093,-0.168,0.3938],
                [0.2,0.163,0.3933],
                [-0.003,0.291,0.393],
                [0.081,0.358,0.3927],
                [0.105,-0.267,0.3925],
                [-0.126,0.214,0.3923],
                [0.092,-0.163,0.392],
                [0.324,0.257,0.3914],
                [0.274,0.213,0.3909],
                [-0.007,0.267,0.3899],
                [-0.1,-0.211,0.3888],
                [-0.051,0.316,0.3864],
                [-0.182,0.25,0.3863],
                [0.052,0.21,0.3817],
                [-0.162,0.153,0.3807],
                [-0.084,-0.164,0.3762],
                [0.028,0.241,0.3738],
                [0.024,-0.212,0.3716],
                [-0.14,-0.277,0.3704],
                [-0.06,-0.157,0.3703],
                [0.103,-0.247,0.3671],
                [0.283,0.482,0.3655],
                [0.047,0.157,0.3648],
                [-0.109,0.19,0.3585],
                [0.054,-0.219,0.3585],
                [0.191,-0.184,0.3585],
                [0.199,0.257,0.3581],
                [-0.163,-0.276,0.3549],
                [0.076,-0.204,0.3545],
                [-0.171,-0.232,0.3538],
                [0.013,0.197,0.3526],
                [-0.102,0.177,0.3522],
                [0.093,0.239,0.3519],
                [0.246,-0.392,0.3518],
                [-0.073,0.152,0.3494],
                [-0.047,0.191,0.3476],
                [0.42,0.228,0.3471],
                [-0.031,0.202,0.3465],
                [0.139,0.204,0.3449],
                [0.055,0.22,0.3443],
                [0,0.153,0.3429],
                [0.116,-0.232,0.3412],
                [0.357,-0.416,0.3408],
                [-0.033,-0.166,0.3406],
                [1.014,1.453,0.3403],
                [0.182,0.162,0.3392],
                [0.097,-0.227,0.339],
                [-0.243,-0.237,0.3384],
                [0.076,-0.146,0.338],
                [0.307,0.247,0.3374],
                [-0.045,-0.158,0.3364],
                [0.114,-0.21,0.336],
                [0.191,0.156,0.3358],
                [0.151,-0.205,0.3329],
                [0.133,0.222,0.3323],
                [-0.387,0.359,0.3321],
                [0.165,0.18,0.3319],
                [0.078,0.169,0.3305],
                [0.016,0.142,0.3303],
                [0.109,-0.149,0.3299],
                [0.073,-0.199,0.3294],
                [-0.141,0.216,0.3292],
                [0.007,-0.219,0.3274],
                [-0.042,0.232,0.3274],
                [-0.022,0.205,0.3247],
                [-0.097,-0.146,0.3225],
                [-0.064,-0.136,0.3225],
                [-0.1,0.159,0.3222],
                [0.02,-0.151,0.3207],
                [-0.04,0.162,0.3197],
                [-0.244,0.332,0.3193],
                [0.048,-0.178,0.3173],
                [0.047,-0.186,0.3173],
                [0.372,0.24,0.317],
                [0.258,0.204,0.3157],
                [-0.174,-0.16,0.3149],
                [-0.163,-0.172,0.313],
                [0.009,0.174,0.3128],
                [-0.122,0.214,0.3126],
                [0.021,0.221,0.3111],
                [-0.238,0.176,0.3101],
                [-0.062,0.15,0.3089],
                [0.093,-0.313,0.3076],
                [0.13,0.178,0.3073],
                [-0.026,0.159,0.3067],
                [0.021,-0.231,0.306],
                [-0.022,-0.153,0.3055],
                [0.267,-0.134,0.3023],
                [-0.091,0.208,0.3021],
                [-0.217,0.338,0.3009],
                [-0.127,0.15,0.3008],
                [-0.073,0.16,0.3003],
                [0.095,0.131,0.3],
                [-0.014,0.176,0.2996],
                [0.116,-0.142,0.299],
                [-0.064,0.158,0.2985],
                [-0.066,-0.232,0.2955],
                [-0.195,-0.144,0.2949],
                [-0.067,-0.176,0.2936],
                [-0.029,0.255,0.2932],
                [-0.051,0.162,0.2926],
                [-0.043,0.126,0.2926],
                [0.031,-0.189,0.2925],
                [-0.06,-0.14,0.2922],
                [-0.204,-0.209,0.2919],
                [0.178,0.139,0.2905],
                [0.017,0.199,0.2897],
                [0.174,-0.173,0.2855],
                [0.272,0.147,0.2849],
                [-0.055,-0.157,0.2846],
                [-0.182,-0.271,0.2826],
                [0.067,-0.132,0.2819],
                [0.093,-0.126,0.2807],
                [-0.062,-0.161,0.2806],
                [0.049,0.181,0.2805],
                [0.039,0.142,0.28],
                [-0.127,-0.167,0.2793],
                [-0.064,-0.221,0.2791],
                [-0.004,-0.332,0.278],
                [-0.153,0.133,0.2778],
                [0.198,-0.175,0.2777],
                [-0.118,0.139,0.2765],
                [-0.071,-0.155,0.2743],
                [-0.04,-0.125,0.274],
                [-0.069,0.161,0.272],
                [0.128,0.131,0.2713],
                [-0.056,0.135,0.2692],
                [0.155,-0.126,0.2688],
                [-0.107,0.14,0.2659],
                [-0.203,0.142,0.2641],
                [-0.119,-0.123,0.2627],
                [-0.039,0.148,0.262],
                [-0.209,0.382,0.2613],
                [0.152,-0.111,0.2603],
                [-0.125,0.112,0.2567],
                [-0.042,0.112,0.2562],
                [-0.068,-0.146,0.2559],
                [0.051,0.124,0.255],
                [-0.191,-0.155,0.2533],
                [0.001,-0.206,0.253],
                [0.059,0.135,0.2519],
                [0.144,0.201,0.2517],
                [0.426,-0.258,0.2509],
                [0.133,0.121,0.2509],
                [-0.006,-0.197,0.2509],
                [-0.106,0.126,0.2495],
                [0.02,-0.264,0.249],
                [0.036,0.108,0.247],
                [-0.556,-0.478,0.2468],
                [0.136,0.155,0.2437],
                [-0.223,-0.123,0.2435],
                [-0.038,-0.111,0.2431],
                [0.092,-0.131,0.2426],
                [-0.123,0.108,0.2422],
                [0.055,0.16,0.2415],
                [-0.053,0.134,0.2413],
                [0.289,-0.119,0.2404],
                [0.12,0.122,0.2383],
                [-0.12,0.124,0.2383],
                [0.045,0.172,0.2371],
                [-0.029,-0.142,0.2368],
                [0.026,-0.167,0.2355],
                [-0.017,-0.167,0.2353],
                [-0.279,-0.278,0.2322],
                [-0.051,0.171,0.2299],
                [0.08,-0.119,0.2298],
                [0.306,0.288,0.2289],
                [-0.035,0.129,0.2284],
                [-0.153,-0.138,0.2274],
                [-0.102,-0.195,0.2261],
                [0.061,0.145,0.2257],
                [-0.269,0.339,0.2254],
                [0.056,-0.128,0.2253],
                [-0.368,0.226,0.2239],
                [0.017,0.107,0.2238],
                [0.004,-0.108,0.2237],
                [-0.057,-0.207,0.2221],
                [0.025,-0.115,0.2218],
                [-0.05,-0.124,0.221],
                [0.34,0.121,0.2208],
                [0.03,0.155,0.2207],
                [0.095,-0.113,0.2201],
                [-0.032,-0.131,0.2196],
                [-0.213,-0.18,0.2188],
                [0.187,0.132,0.2175],
                [-0.016,0.123,0.2166],
                [0.174,-0.15,0.2164],
                [0.05,0.13,0.2153],
                [0.027,0.209,0.2137],
                [0.018,-0.106,0.2125],
                [-0.039,0.117,0.2117],
                [0.063,-0.118,0.2099],
                [0.039,0.147,0.2092],
                [0.049,-0.139,0.2092],
                [-0.081,0.149,0.2091],
                [-0.267,-0.234,0.2088],
                [0.008,0.119,0.2078],
                [0.32,0.205,0.2073],
                [-0.171,0.1,0.2049],
                [0.019,-0.11,0.2038],
                [0.044,-0.129,0.2038],
                [-0.113,-0.124,0.2036],
                [-0.036,0.121,0.203],
                [-0.464,0.127,0.2013],
                [-0.104,0.148,0.2002],
                [-0.111,-0.114,0.1999],
                [0.133,-0.103,0.1987],
                [0.12,0.218,0.1985],
                [-0.07,0.221,0.1973],
                [0.073,-0.161,0.1972],
                [-0.061,-0.095,0.1968],
                [-0.076,-0.112,0.196],
                [-0.007,-0.203,0.1952],
                [0.057,-0.105,0.1946],
                [0.167,-0.272,0.1935],
                [-0.059,0.16,0.1931],
                [0,0.094,0.193],
                [-0.049,0.194,0.1929],
                [0.053,-0.111,0.1927],
                [0.051,0.097,0.1927],
                [-0.163,-0.099,0.1926],
                [0.045,0.165,0.1921],
                [-0.09,0.087,0.1912],
                [-0.004,0.1,0.1902],
                [-0.116,-0.157,0.1896],
                [-0.046,0.108,0.1893],
                [-0.05,0.133,0.1886],
                [-0.052,-0.107,0.1879],
                [0.025,-0.088,0.187],
                [0.072,0.091,0.1867],
                [0.107,0.114,0.1865],
                [-0.148,-0.091,0.1858],
                [0.007,-0.115,0.1851],
                [0.171,0.105,0.1846],
                [0.35,0.109,0.1846],
                [0.03,-0.125,0.1837],
                [-0.048,-0.145,0.1835],
                [0.037,0.154,0.1824],
                [-0.173,0.115,0.1814],
                [0.084,0.09,0.18],
                [0,-0.126,0.18],
                [-0.046,0.099,0.1799],
                [-0.013,0.105,0.1794],
                [0.07,-0.139,0.1789],
                [0.135,-0.117,0.1789],
                [-0.043,0.091,0.1787],
                [-0.027,-0.081,0.1787],
                [0.049,0.103,0.1783],
                [0.142,-0.09,0.178],
                [0.002,-0.093,0.1778],
                [-0.047,0.097,0.1776],
                [0.007,0.165,0.1764],
                [0.095,0.089,0.1764],
                [0.111,-0.157,0.175],
                [0.066,0.126,0.1748],
                [-0.007,0.099,0.1738],
                [-0.106,0.122,0.1736],
                [0.051,-0.116,0.1731],
                [-0.07,0.079,0.173],
                [0.078,0.088,0.1713],
                [-0.176,0.142,0.1713],
                [0.056,-0.083,0.1699],
                [-0.198,-0.22,0.1695],
                [0.045,-0.08,0.1683],
                [-0.025,-0.081,0.168],
                [0.124,-0.149,0.1667],
                [0.107,-0.089,0.1662],
                [0.154,-0.086,0.1657],
                [0.021,-0.097,0.1648],
                [0.126,-0.117,0.1647],
                [-0.284,0.217,0.1644],
                [0.062,-0.114,0.1642],
                [0.126,-0.097,0.1639],
                [-0.059,0.099,0.1627],
                [-0.02,-0.126,0.1624],
                [0.207,0.078,0.1621],
                [0.081,-0.176,0.1617],
                [0.015,-0.105,0.1616],
                [0.406,-0.088,0.161],
                [0.157,0.104,0.1607],
                [-0.075,-0.088,0.1607],
                [-0.003,-0.158,0.1595],
                [-0.005,0.105,0.1582],
                [0.076,-0.102,0.1581],
                [0.266,-0.238,0.1578],
                [-0.207,0.094,0.157],
                [-0.053,-0.097,0.1569],
                [-0.119,0.089,0.1555],
                [-0.169,-0.074,0.1553],
                [-0.202,0.102,0.1542],
                [-0.034,-0.106,0.153],
                [0.026,0.08,0.1512],
                [0.065,-0.084,0.1509],
                [-0.001,-0.141,0.1499],
                [0.004,-0.086,0.1495],
                [0.06,0.125,0.1493],
                [0.159,-0.203,0.1492],
                [-0.193,-0.128,0.1492],
                [-0.032,0.082,0.1491],
                [0.261,-0.109,0.1489],
                [-0.095,0.109,0.1482],
                [0.165,-0.104,0.1479],
                [0.131,0.089,0.1477],
                [-0.076,-0.085,0.1477],
                [-0.044,0.078,0.1468],
                [-0.255,0.096,0.1465],
                [-0.155,0.083,0.1457],
                [0.077,-0.083,0.1453],
                [-0.21,-0.087,0.145],
                [0.087,-0.081,0.1447],
                [-0.189,-0.09,0.1444],
                [0.066,0.128,0.1409],
                [-0.045,0.081,0.1403],
                [-0.091,0.101,0.1399],
                [-0.009,-0.07,0.1398],
                [-0.162,0.092,0.1386],
                [-0.049,-0.067,0.1376],
                [0.313,-0.114,0.1375],
                [0.065,-0.109,0.1371],
                [0.654,0.228,0.1365],
                [-0.081,-0.131,0.1364],
                [-0.192,-0.076,0.1345],
                [0.036,0.125,0.1343],
                [-0.067,-0.083,0.1341],
                [-0.108,-0.104,0.1339],
                [0.056,0.075,0.1335],
                [-0.034,0.077,0.1333],
                [-0.134,0.07,0.133],
                [-0.157,-0.067,0.1319],
                [0.011,-0.099,0.1313],
                [0.039,-0.07,0.1305],
                [0.086,0.081,0.1305],
                [-0.213,0.084,0.1304],
                [-0.06,0.104,0.1294],
                [-0.079,0.072,0.1293],
                [-0.04,-0.133,0.1292],
                [-0.064,0.062,0.1291],
                [-0.021,-0.066,0.1286],
                [0.094,-0.086,0.1274],
                [0.047,-0.108,0.1266],
                [-0.015,-0.072,0.1265],
                [-0.108,-0.063,0.1262],
                [-0.122,0.148,0.1261],
                [-0.263,-0.085,0.1251],
                [-0.104,-0.073,0.1237],
                [-0.129,0.114,0.122],
                [-0.195,-0.069,0.1217],
                [0.045,0.061,0.1208],
                [-0.039,-0.077,0.1179],
                [0.028,0.108,0.1177],
                [-0.007,0.118,0.1173],
                [-0.006,-0.091,0.1173],
                [-0.069,-0.076,0.1169],
                [0.227,-0.076,0.1166],
                [-0.071,-0.076,0.116],
                [-0.155,0.068,0.115],
                [-0.084,-0.067,0.1146],
                [-0.093,0.063,0.1136],
                [-0.042,-0.054,0.1127],
                [0.284,0.099,0.1118],
                [0.039,-0.08,0.1085],
                [0.078,0.067,0.1083],
                [0.158,0.061,0.1078],
                [-0.056,-0.089,0.1071],
                [-0.103,-0.142,0.1067],
                [0.035,-0.082,0.106],
                [0.006,-0.076,0.1041],
                [0.104,0.101,0.1033],
                [-0.143,-0.107,0.1032],
                [0.062,-0.079,0.1031],
                [0.037,0.118,0.1017],
                [-0.176,0.066,0.1013],
                [-0.114,-0.062,0.1007],
                [0.115,0.197,0.1005],
                [0.183,0.115,0.1003],
                [-0.089,0.06,0.0994],
                [0.032,0.06,0.0993],
                [0.015,0.064,0.0986],
                [-0.072,-0.053,0.0978],
                [0.017,-0.067,0.0975],
                [-0.079,0.049,0.0969],
                [-0.061,0.121,0.0951],
                [-0.106,0.054,0.0948],
                [-0.091,-0.072,0.0941],
                [-0.037,0.06,0.0936],
                [-0.081,-0.053,0.0933],
                [-0.057,-0.047,0.093],
                [-0.164,-0.079,0.0907],
                [-0.077,-0.083,0.0905],
                [-0.121,-0.099,0.0896],
                [-0.173,-0.057,0.0887],
                [0.393,0.138,0.0881],
                [0.141,-0.046,0.0879],
                [0.192,-0.068,0.0873],
                [0.233,-0.049,0.0863],
                [-0.321,-0.057,0.0841],
                [-0.052,0.074,0.0841],
                [0.221,0.047,0.0834],
                [-0.148,0.052,0.0832],
                [-0.107,-0.061,0.0831],
                [0.116,0.057,0.0823],
                [-0.066,-0.043,0.0803],
                [-0.167,-0.044,0.0799],
                [0.033,-0.053,0.0797],
                [0.052,0.04,0.0795],
                [-0.098,-0.055,0.0792],
                [0.031,-0.046,0.0791],
                [0.011,-0.044,0.079],
                [-0.144,0.096,0.0788],
                [0.004,0.066,0.0787],
                [0.012,0.042,0.0787],
                [-0.112,0.056,0.0783],
                [0.01,0.064,0.0782],
                [-0.038,-0.044,0.0772],
                [0.092,0.04,0.0767],
                [-0.127,-0.113,0.0766],
                [0.043,0.048,0.0764],
                [0.174,-0.048,0.076],
                [-0.15,0.055,0.0755],
                [-0.064,0.048,0.0755],
                [-0.008,-0.048,0.0754],
                [-0.238,0.072,0.0721],
                [0.01,0.09,0.0717],
                [0.089,-0.038,0.0715],
                [-0.171,-0.041,0.0714],
                [-0.013,0.041,0.0714],
                [-0.076,0.059,0.0709],
                [-0.257,0.039,0.0707],
                [-0.077,0.045,0.0701],
                [0.144,0.044,0.0694],
                [-0.17,0.055,0.0686],
                [0.162,0.044,0.0683],
                [0.461,-0.074,0.0681],
                [0.152,0.062,0.0681],
                [0.065,0.035,0.0678],
                [-0.058,0.04,0.0674],
                [-0.035,-0.034,0.0659],
                [-0.14,0.039,0.0647],
                [-0.156,0.04,0.0639],
                [0.186,-0.047,0.063],
                [-0.017,-0.039,0.0621],
                [0.273,0.046,0.062],
                [-0.051,-0.041,0.0618],
                [0.143,-0.102,0.0614],
                [0.027,-0.042,0.0613],
                [0.13,-0.033,0.0606],
                [0.064,-0.036,0.0606],
                [0.019,-0.042,0.0599],
                [0.055,-0.036,0.0597],
                [0.004,0.037,0.0596],
                [-0.075,-0.081,0.0595],
                [0.006,-0.051,0.059],
                [0.341,-0.04,0.0582],
                [0.084,-0.035,0.058],
                [-0.037,-0.035,0.0574],
                [0.216,-0.038,0.0571],
                [0.144,0.034,0.057],
                [-0.145,-0.042,0.0567],
                [0.183,-0.066,0.0564],
                [0.069,-0.035,0.0563],
                [0.006,0.04,0.0557],
                [-0.016,0.034,0.0554],
                [0.025,-0.036,0.0547],
                [0.189,0.048,0.0544],
                [0.01,-0.039,0.0544],
                [-0.006,-0.032,0.0542],
                [-0.167,-0.038,0.0541],
                [0.255,0.075,0.0531],
                [-0.062,-0.033,0.0528],
                [-0.064,0.037,0.0527],
                [0.167,-0.029,0.0521],
                [-0.091,-0.042,0.0514],
                [-0.02,-0.03,0.0512],
                [-0.111,0.041,0.0503],
                [-0.142,0.031,0.0501],
                [-0.184,-0.038,0.0501],
                [0.074,0.039,0.0498],
                [0.061,0.03,0.0495],
                [-0.188,0.07,0.0494],
                [-0.068,0.027,0.0492],
                [0.089,0.034,0.0491],
                [-0.02,0.027,0.0481],
                [0.047,0.032,0.0467],
                [-0.12,-0.029,0.0467],
                [-0.038,-0.055,0.0464],
                [0.268,-0.033,0.0463],
                [-0.021,-0.026,0.0455],
                [0.166,0.043,0.0454],
                [-0.083,0.03,0.0452],
                [0.099,-0.026,0.0437],
                [-0.104,-0.027,0.0435],
                [-0.259,0.047,0.0417],
                [-0.005,-0.031,0.0415],
                [-0.004,0.023,0.041],
                [0.096,0.04,0.0408],
                [0.079,-0.028,0.0405],
                [-0.061,0.039,0.0401],
                [-0.091,0.023,0.0401],
                [0.03,-0.029,0.0398],
                [0.123,0.029,0.0388],
                [0.088,-0.024,0.0386],
                [-0.039,-0.027,0.0384],
                [0.113,0.044,0.0375],
                [-0.079,-0.021,0.0374],
                [-0.009,0.019,0.0371],
                [0.079,0.038,0.0362],
                [-0.122,-0.023,0.0357],
                [-0.177,0.023,0.0354],
                [0.173,0.026,0.0348],
                [-0.094,0.017,0.0337],
                [-0.035,-0.032,0.0329],
                [-0.125,0.025,0.0329],
                [0.188,-0.018,0.0327],
                [-0.101,0.03,0.0318],
                [0.109,-0.02,0.0302],
                [0.151,-0.034,0.03],
                [0.411,0.024,0.0296],
                [0.173,0.018,0.0295],
                [-0.22,-0.017,0.0293],
                [0.062,-0.02,0.0292],
                [0.023,0.017,0.0288],
                [0.002,0.025,0.0287],
                [0,-0.029,0.0283],
                [0.3,-0.02,0.0275],
                [-0.011,0.015,0.0273],
                [0.159,-0.022,0.0272],
                [-0.02,-0.023,0.0271],
                [-0.336,0.022,0.0269],
                [0.053,-0.018,0.0261],
                [0.434,-0.024,0.0253],
                [0.046,-0.025,0.0249],
                [0.081,0.018,0.0245],
                [-0.325,0.024,0.0244],
                [0.278,-0.022,0.0241],
                [-0.083,0.017,0.023],
                [0.104,0.012,0.023],
                [-0.011,-0.017,0.0229],
                [-0.249,0.017,0.0221],
                [0.224,-0.02,0.0203],
                [0.041,0.025,0.0202],
                [-0.023,0.018,0.02],
                [0.009,0.028,0.0195],
                [0.065,0.013,0.0195],
                [0.047,-0.024,0.019],
                [0.089,0.017,0.0186],
                [-0.21,0.011,0.018],
                [-0.04,0.012,0.0179],
                [0.087,0.02,0.0174],
                [-0.081,-0.012,0.0172],
                [0.204,-0.011,0.0165],
                [-0.15,-0.013,0.0163],
                [-0.049,0.01,0.0162],
                [0.089,0.018,0.0156],
                [-0.125,-0.012,0.0156],
                [-0.328,-0.011,0.0153],
                [0.017,0.008,0.0142],
                [-0.009,0.009,0.0129],
                [0.098,0.01,0.0128],
                [-0.006,-0.007,0.0125],
                [0.058,0.013,0.0114],
                [0.09,-0.007,0.0104],
                [-0.004,0.008,0.0098],
                [-0.138,-0.007,0.0095],
                [-0.001,-0.005,0.0089],
                [-0.055,0.007,0.0088],
                [0.054,-0.005,0.0086],
                [-0.073,0.006,0.0084],
                [-0.163,-0.007,0.0084],
                [0.038,-0.007,0.0076],
                [-0.162,0.005,0.0069],
                [-0.025,-0.005,0.0068],
                [0.01,0.004,0.0065],
                [-0.064,-0.003,0.0059],
                [0.053,-0.005,0.0058],
                [-0.026,-0.004,0.0045],
                [0.139,-0.004,0.0043],
                [0.128,-0.002,0.0042],
                [0.095,0.003,0.0038],
                [-0.462,-0.007,0.0037],
                [0.089,-0.002,0.0035],
                [-0.076,0.002,0.003],
                [0.03,-0.002,0.0029],
                [0.153,-0.002,0.0026],
                [-0.202,0.001,0.0024],
                [0.125,-0.002,0.0024],
                [-0.145,0.002,0.0022],
                [0.017,0.001,0.0015],
                [0.226,-0.001,0.0005],
                [0.039,0,0.0005],
                [0.074,0,0.0004],
                [-0.039,0,0]
              ]
            }
          },
          "config": {
            "axisAlgorithm": "rPretty",
            "backgroundType": "window",
            "backgroundWindow": "rgb(238,238,238)",
            "colorBy": "Group",
            "colors": ["rgba(0,104,139,0.5)","rgba(205,0,0,0.5)","rgba(64,64,64,0.5)"],
            "decorations": {
              "line": [
                {
                  "color": "rgba(205,0,0,0.5)",
                  "y": 0.5,
                  "width": 2
                },
                {
                  "width": 2,
                  "color": "rgba(0,104,139,0.5)",
                  "y": -0.5
                }
              ]
            },
            "graphType": "Scatter2D",
            "legendBackgroundColor": "rgb(238,238,238)",
            "legendBox": true,
            "legendBoxColor": "rgb(0,0,0)",
            "legendInside": true,
            "legendPosition": "bottomRight",
            "plotBox": false,
            "showConfidenceIntervals": false,
            "showDecorations": true,
            "showLoessFit": true,
            "showTransition": false,
            "sizeBy": "FC",
            "sizes": [4,14,16,18],
            "theme": "CanvasXpress",
            "title": "Profile plot",
            "xAxis": ["AveExpr"],
            "xAxisTickColor": "rgb(255,255,255)",
            "yAxis": ["logFC"],
            "yAxisTickColor": "rgb(255,255,255)"
          },
          "events": false,
          "info": false,
          "afterRenderInit": false,
          "afterRender": [
            [
              "setDimensions",
              [613,613,true]
            ]
          ],
          "noValidate": true,
          "factory": {
            "version": 35,
            "buildDate": "06-20-2021",
            "client": "MTYyNDMwMDM0NTY0MDo6MTo6MzU6Og==",
            "siteSrc": true,
            "valid": 0,
            "href": "https://www.canvasxpress.org/examples/scatter2d.html",
            "services": "https://www.canvasxpress.org/cgi-bin/services.pl"
          },
          "system": {
            "browser": "Chrome",
            "browserVersion": "91",
            "os": "Mac OS",
            "alt": "&#8997;",
            "command": "&#8984;",
            "control": "&#8963;",
            "shift": "&#8679;",
            "isjQuery": true,
            "isReveal": false,
            "isZoom": false,
            "isIE": false,
            "isInIframe": false,
            "isTouchScreen": 0,
            "isR": false,
            "isHTMLWidgets": false,
            "isShiny": false,
            "isRViewer": false,
            "isRConsole": false,
            "isNode": false
          }
        }
        """
    )

    result = repr(candidate)
    alt_candidate = eval(result)

    assert candidate.render_to == alt_candidate.render_to
    assert candidate.data == alt_candidate.data
    assert candidate.config == alt_candidate.config
    assert candidate.events == alt_candidate.events
    assert candidate.after_render == alt_candidate.after_render
    assert candidate.other_init_params == alt_candidate.other_init_params

    assert repr(candidate) == repr(alt_candidate)
