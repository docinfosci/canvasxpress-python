from canvasxpress.data.text import CXTextData

raw_data = """
"Name",     "Sex", "Age", "Height (in)", "Weight (lbs)"
"Alex",       "M",   41,       74,      170
"Bert",       "M",   42,       68,      166
"Carl",       "M",   32,       70,      155
"Dave",       "M",   39,       72,      167
"Elly",       "F",   30,       66,      124
"Fran",       "F",   33,       66,      115
"Gwen",       "F",   26,       64,      121
"Hank",       "M",   30,       71,      158
"Ivan",       "M",   53,       72,      175
"Jake",       "M",   32,       69,      143
"Kate",       "F",   47,       69,      139
"Luke",       "M",   34,       72,      163
"Myra",       "F",   23,       62,       98
"Neil",       "M",   36,       75,      160
"Omar",       "M",   38,       70,      145
"Page",       "F",   31,       67,      135
"Quin",       "M",   29,       71,      176
"Ruth",       "F",   28,       65,      131
"""


def test_init_CXTextData():
    candidate = CXTextData(raw_data)
    assert candidate.text == raw_data

    candidate = CXTextData()
    assert candidate.text == ""

    candidate = CXTextData(1)
    assert candidate.text == "1"


def test_text():
    candidate = CXTextData()
    candidate.text = raw_data
    assert candidate.text == raw_data

    candidate = CXTextData()
    candidate.text = None
    assert candidate.text == ""

    candidate = CXTextData()
    candidate.text = 1
    assert candidate.text == "1"


def test_data():
    candidate = CXTextData()
    candidate.text = raw_data
    assert candidate.data == {"raw": raw_data}

    candidate = CXTextData()
    candidate.text = None
    assert candidate.data == {"raw": ""}
    candidate = CXTextData()
    candidate.text = 1
    assert candidate.data == {"raw": "1"}
    candidate = CXTextData()
    candidate.text = "https://www.canvasxpress.org/data/cX-heatmapR-dat.txt"
    assert candidate.data == {
        "raw": "https://www.canvasxpress.org/data/cX-heatmapR-dat.txt"
    }
