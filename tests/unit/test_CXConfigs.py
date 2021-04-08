import pytest

from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import CXString, CXType, CXRGBColor, CXInt, \
    CXFloat, CXBool, CXDict, CXList, CXRGBAColor


def test_CXConfigs_init():
    cfgs: CXConfigs = CXConfigs()
    assert len(cfgs.configs) == 0

    config1: CXType = CXString("test", "value")
    config2: CXType = CXString("test1", "value2")
    cfgs: CXConfigs = CXConfigs(
        config1,
        config2
    )
    assert len(cfgs.configs) == 2
    assert config1 in cfgs.configs
    assert config2 in cfgs.configs


def test_CXConfigs_add_junk():
    junk: int = 0
    cfgs: CXConfigs = CXConfigs()

    with pytest.raises(TypeError):
        cfgs.add(junk)

    with pytest.raises(ValueError):
        cfgs.add(None)


def test_CXConfigs_add():
    cfgs: CXConfigs = CXConfigs()
    config1: CXType = CXString("test", "value")

    cfgs.add(config1)
    assert len(cfgs.configs) == 1
    assert config1 in cfgs.configs


def test_CXConfigs_render_to_dict_empty():
    cfgs: CXConfigs = CXConfigs()

    candidate = cfgs.render_to_dict()
    assert isinstance(candidate, dict)
    assert len(candidate.keys()) == 0


def test_CXConfigs_render_to_dict():
    config1: CXType = CXString("test", "value")
    cfgs: CXConfigs = CXConfigs(
        config1
    )

    candidate = cfgs.render_to_dict()
    assert isinstance(candidate, dict)
    assert candidate[config1.label] == config1.value


def test_CXConfigs_merge_configs():
    candidate_cxtypes: list = [
        CXString("1", "1"),
        CXString("2", "2")
    ]
    merged = CXConfigs.merge_configs(candidate_cxtypes)
    assert isinstance(merged, dict)
    assert len(merged.keys()) == 2
    for k in merged.keys():
        assert merged[k] == k

    candidate_cxtypes: list = []
    merged = CXConfigs.merge_configs(candidate_cxtypes)
    assert isinstance(merged, dict)
    assert len(merged.keys()) == 0

    candidate_cxtypes = None
    merged = CXConfigs.merge_configs(candidate_cxtypes)
    assert isinstance(merged, dict)
    assert len(merged.keys()) == 0


def test_CXConfigs_set_param():
    cfgs: CXConfigs = CXConfigs()
    with pytest.raises(ValueError):
        cfgs.set_param(None, 0)

    cfgs: CXConfigs = CXConfigs()
    with pytest.raises(ValueError):
        cfgs.set_param("1", None)

    cfgs: CXConfigs = CXConfigs()
    config1: CXType = CXInt("test", 1)
    cfgs.add(config1)
    with pytest.raises(ValueError):
        cfgs.set_param(
            config1.label,
            str(config1.value)
        )

    original_value = config1.value
    cfgs.set_param(
        config1.label,
        config1.value + 1
    )
    adjusted_value_found = False
    for cfg in cfgs.configs:
        if cfg.label == config1.label:
            assert cfg.value == original_value + 1
            adjusted_value_found = True
            break
    assert adjusted_value_found

    cfgs: CXConfigs = CXConfigs()
    test_items = [
        (CXInt, "int", 0),
        (CXFloat, "float", 0.1),
        (CXBool, "bool", True),
        (CXDict, "dict", {'k': 'v'}),
        (CXList, "list", [0, 1]),
        (CXList, "set", {0, 1}),
        (CXRGBColor, "rgb_dict", {'r': 128, 'g': 128, 'b': 128}),
        (CXRGBColor, "rgb_list", [128, 128, 128]),
        (CXRGBColor, "rgb_str", "rgb(128,128,128)"),
        (CXRGBAColor, "rgba_dict", {'r': 128, 'g': 128, 'b': 128, 'a': 1}),
        (CXRGBAColor, "rgba_list", [128, 128, 128, 1]),
        (CXRGBAColor, "rgba_str", "rgba(128,128,128,1)"),
        (CXString, "str", "0"),
    ]
    for item in test_items:
        cfgs.set_param(
            item[1],
            item[2]
        )
    cfg_items = [
        (type(item), item.label, item.value)
        for item in cfgs.configs
    ]
    assert len(cfg_items) == len(test_items)
    for test_item in test_items:
        if test_item[1] == 'set':
            assert (CXList, "set", [0, 1]) in cfg_items
        elif test_item[1] in ['rgb_list', 'rgb_str', ]:
            assert (
                       CXRGBColor,
                       "rgb_dict",
                       {'r': 128, 'g': 128, 'b': 128}
                   ) in cfg_items
        elif test_item[1] in ['rgba_list', 'rgba_str', ]:
            assert (
                       CXRGBAColor,
                       "rgba_dict",
                       {'r': 128, 'g': 128, 'b': 128, 'a': 1}
                   ) in cfg_items
        else:
            assert test_item in cfg_items
