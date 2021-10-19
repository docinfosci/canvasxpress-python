import json
from copy import copy, deepcopy

import pytest

from canvasxpress.config.collection import CXConfigs
from canvasxpress.config.type import (
    CXString,
    CXConfig,
    CXRGBColor,
    CXInt,
    CXFloat,
    CXBool,
    CXDict,
    CXList,
    CXRGBAColor,
    CXGraphType,
    CXGraphTypeOptions,
)


def test_CXConfigs_init():
    cfgs: CXConfigs = CXConfigs()
    assert len(cfgs.configs) == 0

    config1: CXConfig = CXString("test", "value")
    config2: CXConfig = CXString("test1", "value2")
    cfgs: CXConfigs = CXConfigs(config1, config2)
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
    candidate: CXConfigs = CXConfigs()
    config1: CXConfig = CXString("test", "value")

    candidate.add(config1)
    assert len(candidate.configs) == 1
    assert config1 in candidate.configs

    candidate: CXConfigs = CXConfigs(["test", 1])
    assert len(candidate.configs) == 1
    for config in candidate.configs:
        assert config.label == "test"
        assert config.value == 1

    candidate: CXConfigs = CXConfigs(CXInt("test", 1))
    assert len(candidate.configs) == 1
    for config in candidate.configs:
        assert config.label == "test"
        assert config.value == 1

    candidate: CXConfigs = CXConfigs([["test", 1], ("test2", 2)])
    assert len(candidate.configs) == 2
    for config in candidate.configs:
        if config.label == "test":
            assert config.value == 1
        if config.label == "test2":
            assert config.value == 2


def test_CXConfigs_render_to_dict_empty():
    cfgs: CXConfigs = CXConfigs()

    candidate = cfgs.render_to_dict()
    assert isinstance(candidate, dict)
    assert len(candidate.keys()) == 0


def test_CXConfigs_render_to_dict():
    config1: CXConfig = CXString("test", "value")
    cfgs: CXConfigs = CXConfigs(config1)

    candidate = cfgs.render_to_dict()
    assert isinstance(candidate, dict)
    assert candidate[config1.label] == config1.value


def test_CXConfigs_merge_configs():
    candidate_cxtypes: list = [CXString("1", "1"), CXString("2", "2")]
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
    config1: CXConfig = CXInt("test", 1)
    cfgs.add(config1)
    with pytest.raises(ValueError):
        cfgs.set_param(config1.label, str(config1.value))

    original_value = config1.value
    cfgs.set_param(config1.label, config1.value + 1)
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
        (CXDict, "dict", {"k": "v"}),
        (CXList, "list", [0, 1]),
        (CXList, "set", {0, 1}),
        (CXRGBColor, "rgb_dict", {"r": 128, "g": 128, "b": 128}),
        (CXRGBColor, "rgb_list", [128, 128, 128]),
        (CXRGBColor, "rgb_str", "rgb(128,128,128)"),
        (CXRGBAColor, "rgba_dict", {"r": 128, "g": 128, "b": 128, "a": 1}),
        (CXRGBAColor, "rgba_list", [128, 128, 128, 1]),
        (CXRGBAColor, "rgba_str", "rgba(128,128,128,1)"),
        (CXString, "str", "0"),
    ]
    for item in test_items:
        cfgs.set_param(item[1], item[2])
    cfg_items = [(type(item), item.label, item.value) for item in cfgs.configs]
    assert len(cfg_items) == len(test_items)
    for test_item in test_items:
        if test_item[1] == "set":
            assert (CXList, "set", [0, 1]) in cfg_items
        elif test_item[1] in [
            "rgb_list",
            "rgb_str",
        ]:
            assert (CXRGBColor, "rgb_dict", {"r": 128, "g": 128, "b": 128}) in cfg_items
        elif test_item[1] in [
            "rgba_list",
            "rgba_str",
        ]:
            assert (
                CXRGBAColor,
                "rgba_dict",
                {"r": 128, "g": 128, "b": 128, "a": 1},
            ) in cfg_items
        else:
            assert test_item in cfg_items


def test_CXConfigs_copy():
    configs1 = CXConfigs(CXString(label="1", value="hi"))
    configs2 = copy(configs1)
    assert configs1 == configs2


def test_CXConfigs_deepcopy():
    configs1 = CXConfigs(CXString(label="1", value="hi"))
    configs2 = deepcopy(configs1)
    assert configs1 == configs2


def test_CXConfigs_str_perspective():
    config = CXString(label="1", value="hi")
    configs = CXConfigs(config)

    configs_str = str(configs)
    assert configs_str == json.dumps(configs.render_to_dict())


def test_CXConfigs_repr_perspective():
    config = CXString(label="1", value="hi")
    configs = CXConfigs(config)

    configs_repr = repr(configs)
    configs_rep = eval(r"{}".format(configs_repr))
    assert configs_rep == configs


def test_CXConfigs_equality():
    configs_a: CXConfigs = CXConfigs()
    configs_b: CXConfigs = CXConfigs()

    assert configs_a == configs_b
    assert not configs_a < configs_b
    assert not configs_a > configs_b

    configs_c: CXConfigs = CXConfigs(CXString("a", "a()"))

    assert configs_a != configs_c
    assert configs_a < configs_c
    assert configs_c > configs_a

    configs_d: CXConfigs = CXConfigs(CXString("a", "a()"))

    assert configs_c == configs_d
    assert not configs_c < configs_d
    assert not configs_c > configs_d

    configs_e: CXConfigs = CXConfigs(CXString("b", "b()"))

    assert configs_a != configs_e
    assert configs_a < configs_e
    assert configs_e > configs_a
    assert not configs_a > configs_e

    assert configs_d != configs_e
    assert configs_d < configs_e
    assert configs_e > configs_d
    assert not configs_d > configs_e

    configs: CXConfigs = CXConfigs()
    assert configs != None
    assert not configs < None
    assert configs > None
    assert None < configs

    configs: CXConfig = CXConfigs()
    junk_candidates: list = [0, "0", {"a": 0}, [0]]
    for junk in junk_candidates:
        assert configs != junk
        assert not configs < junk
        assert configs > junk
