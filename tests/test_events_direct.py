"""
Direct testing of events_skill.md with plain English prompts.

This script creates test cases with plain English prompts and generates
CXEvent code to validate the skill's effectiveness.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

# Test chart examples and plain English prompts
TEST_CASES = [
    {
        "id": "bar_click_tooltip",
        "chart_type": "bar",
        "description": "Single Variable Bar Chart",
        "data": {
            "y": {
                "data": [[4, 5, 4, 4, 7]],
                "smps": ["Cat 1", "Cat 2", "Cat 3", "Cat 4", "Cat 5"],
                "vars": ["Var 1"],
            }
        },
        "config": {
            "graphType": "Bar",
            "title": "Bar graph with a single series",
        },
        "prompt": "When I click on a bar in the chart, show a tooltip popup that displays the category name and the value.",
        "expected_event": {
            "id": "click",
            "script": "var s = 'Category: ' + o.y.smps[0] + ', Value: ' + o.y.data[0][o.y.smps.indexOf(o.y.smps[0])]; t.showInfoSpan(e, s);",
        },
    },
    {
        "id": "bar_hover_effect",
        "chart_type": "bar",
        "description": "Single Variable Bar Chart",
        "data": {
            "y": {
                "data": [[4, 5, 4, 4, 7]],
                "smps": ["Cat 1", "Cat 2", "Cat 3", "Cat 4", "Cat 5"],
                "vars": ["Var 1"],
            }
        },
        "config": {
            "graphType": "Bar",
            "title": "Bar graph with a single series",
        },
        "prompt": "Add a hover effect so when the mouse moves over a bar, a tooltip shows the data value for that category.",
        "expected_event": {
            "id": "mousemove",
            "script": "t.showInfoSpan(e, 'Value: ' + o.y.data[0][o.y.smps.indexOf(o.y.smps[0])]);",
        },
    },
    {
        "id": "heatmap_cell_interaction",
        "chart_type": "heatmap",
        "description": "Simple Heatmap",
        "data": {
            "y": {
                "data": [[1.2, 2.3, 3.4], [4.5, 5.6, 6.7], [7.8, 8.9, 9.0]],
                "smps": ["S1", "S2", "S3"],
                "vars": ["V1", "V2", "V3"],
            }
        },
        "config": {
            "graphType": "Heatmap",
            "title": "Simple Heatmap",
        },
        "prompt": "When I hover over a heatmap cell, display a tooltip showing the variable name, sample name, and the cell value.",
        "expected_event": {
            "id": "mousemove",
            "script": "var gene = o.y.vars[0]; var sample = o.y.smps[0]; var value = o.y.data[o.y.vars.indexOf(gene)][o.y.smps.indexOf(sample)]; t.showInfoSpan(e, gene + ' | ' + sample + ': ' + value);",
        },
    },
    {
        "id": "scatter_click_select",
        "chart_type": "scatter",
        "description": "Scatter Plot",
        "data": {
            "y": {
                "data": [[10, 20, 30, 40, 50], [15, 25, 35, 45, 55]],
                "smps": ["S1", "S2", "S3", "S4", "S5"],
                "vars": ["X", "Y"],
            }
        },
        "config": {
            "graphType": "Scatter2D",
            "title": "Scatter Plot Example",
        },
        "prompt": "When I click on a data point, show a popup with the sample name and both X and Y values.",
        "expected_event": {
            "id": "click",
            "script": "var smp = o.y.smps[0]; var x = o.y.data[0][o.y.smps.indexOf(smp)]; var y = o.y.data[1][o.y.smps.indexOf(smp)]; t.showInfoSpan(e, smp + ' (X=' + x + ', Y=' + y + ')');",
        },
    },
    {
        "id": "line_doubleclick_zoom",
        "chart_type": "line",
        "description": "Line Chart",
        "data": {
            "y": {
                "data": [[10, 20, 30], [15, 25, 35]],
                "smps": ["S1", "S2", "S3"],
                "vars": ["Var 1", "Var 2"],
            }
        },
        "config": {
            "graphType": "Line",
            "title": "Line Chart",
        },
        "prompt": "When I double-click on the chart, zoom in to show only the selected data series.",
        "expected_event": {
            "id": "dblclick",
            "script": "t.zoom();",
        },
    },
    {
        "id": "network_node_click",
        "chart_type": "network",
        "description": "Network Graph",
        "data": {
            "edges": [
                {"id1": "A", "id2": "B", "value": 1},
                {"id1": "B", "id2": "C", "value": 2},
                {"id1": "C", "id2": "A", "value": 3},
            ],
            "y": {
                "vars": ["A", "B", "C"],
            },
        },
        "config": {
            "graphType": "Network",
            "title": "Network Graph",
        },
        "prompt": "When I click on a network node, display a tooltip showing the node ID.",
        "expected_event": {
            "id": "click",
            "script": "if (o && o.nodes) { t.showInfoSpan(e, 'Node: ' + o.nodes[0].id); }",
        },
    },
    {
        "id": "pie_legend_click",
        "chart_type": "pie",
        "description": "Pie Chart",
        "data": {
            "y": {
                "data": [[30, 40, 30]],
                "smps": ["Category A", "Category B", "Category C"],
                "vars": ["Total"],
            }
        },
        "config": {
            "graphType": "Pie",
            "title": "Pie Chart Example",
        },
        "prompt": "When I click on a legend item, show what category was selected.",
        "expected_event": {
            "id": "clicklegend",
            "script": "if (o) { t.showInfoSpan(e, 'Selected: ' + o.legend); }",
        },
    },
    {
        "id": "boxplot_mouseout_cleanup",
        "chart_type": "boxplot",
        "description": "Box Plot",
        "data": {
            "y": {
                "data": [
                    [10, 12, 14, 16, 18],
                    [11, 13, 15, 17, 19],
                    [9, 11, 13, 15, 17],
                ],
                "smps": ["S1", "S2", "S3", "S4", "S5"],
                "vars": ["Group A", "Group B", "Group C"],
            }
        },
        "config": {
            "graphType": "Boxplot",
            "title": "Box Plot Example",
        },
        "prompt": "When the mouse moves over a box, show a tooltip with the group name. When the mouse leaves, hide the tooltip.",
        "expected_events": [
            {
                "id": "mouseover",
                "script": "t.showInfoSpan(e, o.y.vars[0]);",
            },
            {
                "id": "mouseout",
                "script": "t.hideInfoSpan();",
            },
        ],
    },
]


def generate_python_code(test_case: dict) -> str:
    """Generate Python code for a test case."""
    code = "from canvasxpress.canvas import CanvasXpress\n"
    code += "from canvasxpress.js.function import CXEvent\n"
    code += "from canvasxpress.js.collection import CXEvents\n"
    code += "from canvasxpress.plot import convert_to_reproducible_json\n\n"
    
    # Add data
    code += f"data = {json.dumps(test_case['data'])}\n"
    
    # Add config
    code += f"config = {json.dumps(test_case['config'])}\n"
    
    # Add events
    if "expected_events" in test_case:
        # Multiple events
        code += "\nevents = CXEvents(\n"
        for evt in test_case["expected_events"]:
            code += f'    CXEvent(id="{evt["id"]}", script="{evt["script"]}"),\n'
        code += ")\n"
    elif "expected_event" in test_case:
        # Single event
        evt = test_case["expected_event"]
        code += f'\nevents = CXEvent(id="{evt["id"]}", script="{evt["script"]}")\n'
    
    # Add CanvasXpress object
    code += "\ncx = CanvasXpress(data=data, config=config, events=events)\n"
    
    # Validation
    code += """
try:
    json_output = convert_to_reproducible_json(cx)
    print("VALIDATION PASSED")
except Exception as e:
    print(f"VALIDATION FAILED: {e}")
    raise
"""
    
    return code


def run_ruff_check(code: str, test_id: str) -> tuple[bool, str]:
    """Run ruff check on the code."""
    temp_file = Path(f"/tmp/ruff_test_{test_id}.py")
    temp_file.write_text(code)
    
    try:
        result = subprocess.run(
            ["ruff", "check", str(temp_file)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        temp_file.unlink(missing_ok=True)
        if result.returncode == 0:
            return True, ""
        return False, result.stdout
    except Exception as e:
        temp_file.unlink(missing_ok=True)
        return False, str(e)


def run_canvasxpress_validation(code: str, test_id: str) -> tuple[bool, str]:
    """Validate CanvasXpress code executes without exceptions."""
    temp_file = Path(f"/tmp/cx_test_{test_id}.py")
    temp_file.write_text(code)
    
    try:
        result = subprocess.run(
            [sys.executable, str(temp_file)],
            capture_output=True,
            text=True,
            timeout=60,
        )
        temp_file.unlink(missing_ok=True)
        if result.returncode == 0 and "VALIDATION PASSED" in result.stdout:
            return True, result.stdout
        return False, result.stdout + result.stderr
    except Exception as e:
        temp_file.unlink(missing_ok=True)
        return False, str(e)


def main():
    """Run all test cases."""
    print("=" * 80)
    print("CanvasXpress Events Skill Testing - Direct Code Validation")
    print("=" * 80)
    
    results = []
    
    for test_case in TEST_CASES:
        print(f"\n{'='*80}")
        print(f"Test: {test_case['id']}")
        print(f"Chart: {test_case['chart_type']} - {test_case['description']}")
        print(f"Prompt: {test_case['prompt']}")
        print(f"{'='*80}")
        
        # Generate code
        code = generate_python_code(test_case)
        
        print("\nGenerated Code:")
        print("-" * 80)
        print(code)
        print("-" * 80)
        
        # Run validations
        ruff_ok, ruff_output = run_ruff_check(code, test_case['id'])
        cx_ok, cx_output = run_canvasxpress_validation(code, test_case['id'])
        
        result = {
            "id": test_case["id"],
            "chart": test_case["chart_type"],
            "description": test_case["description"],
            "prompt": test_case["prompt"],
            "ruff_valid": ruff_ok,
            "ruff_output": ruff_output,
            "cx_valid": cx_ok,
            "cx_output": cx_output,
            "code": code,
        }
        results.append(result)
        
        # Print results
        print(f"\nRuff Check: {'PASS' if ruff_ok else 'FAIL'}")
        if ruff_output:
            print(f"  {ruff_output[:300]}")
        
        print(f"CanvasXpress Validation: {'PASS' if cx_ok else 'FAIL'}")
        if cx_output:
            print(f"  {cx_output[:300]}")
    
    # Summary
    print(f"\n\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    
    passed = sum(1 for r in results if r['ruff_valid'] and r['cx_valid'])
    total = len(results)
    
    print(f"\nPassed: {passed}/{total}")
    
    for r in results:
        status = "PASS" if (r['ruff_valid'] and r['cx_valid']) else "FAIL"
        print(f"  [{status}] {r['id']} ({r['chart']})")
    
    # Save results
    results_file = Path("/tmp/events_direct_test_results.json")
    results_to_save = []
    for r in results:
        results_to_save.append({
            "id": r["id"],
            "chart": r["chart"],
            "prompt": r["prompt"],
            "ruff_valid": r["ruff_valid"],
            "cx_valid": r["cx_valid"],
        })
    results_file.write_text(json.dumps(results_to_save, indent=2))
    print(f"\nResults saved to: {results_file}")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
