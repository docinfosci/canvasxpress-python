---
name: code_validator
description: Validates generated CanvasXpress Python code for syntax correctness before presenting solutions to users. Creates temporary validation scripts, runs syntax checks using convert_to_reproducible_json, iteratively fixes errors until code is correct, and cleans up temporary files. ALWAYS iterate on the code until validation passes - never present broken code to the user.
category: code-quality
tools:
  - python
  - canvasxpress
---

## Purpose

Before presenting any CanvasXpress chart code to the user, validate that it is syntactically correct and can be executed without errors. This prevents users from receiving broken code that won't run.

## Validation Workflow

### 1. Generate Temporary Validation Script

Create a temporary Python file (e.g., `/tmp/cx_validate_XXXXXX.py`) containing:

```python
# Essential imports only
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import convert_to_reproducible_json
import pandas as pd

# Data definition
df = pd.DataFrame({
    'Category': ['A', 'B', 'C'],
    'Value': [10, 20, 30]
})

# Chart configuration
cx = CanvasXpress(
    data=df,
    config={
        "graphType": "Bar",
        "title": "Test Chart",
        "xAxisTitle": "Category",
        "yAxisTitle": "Value"
    }
)

# Validation: Try to convert to reproducible JSON
# This catches syntax errors without needing a browser
try:
    json_output = convert_to_reproducible_json(cx)
    print("VALIDATION PASSED")
except Exception as e:
    print(f"VALIDATION FAILED: {e}")
    raise
```

**Key requirements:**
- Include only necessary imports: `CanvasXpress`, `convert_to_reproducible_json`, and any data libraries (pandas, numpy, etc.)
- Include the user's data definition
- Include the complete CanvasXpress configuration
- Include the validation block using `convert_to_reproducible_json`
- Do NOT include rendering code (`graph()`, `show_in_browser()`, etc.) as these require a display environment

### 2. Execute Validation Script

Run the temporary script using subprocess or exec:

```python
import subprocess
import sys

result = subprocess.run(
    [sys.executable, temp_script_path],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("Code is syntactically correct")
else:
    print(f"Validation errors:\n{result.stderr}")
```

### 3. Iterate Until Code is Correct

**This is mandatory - never present broken code to the user.**

If validation fails:
1. **Parse error message** - Identify the exact line and nature of the error
2. **Fix the code** - Correct the syntax or logic error
3. **Update validation script** - Regenerate the temp file with fixed code
4. **Re-validate** - Run the validation script again
5. **Repeat** - Continue this loop until validation passes

**You MUST keep iterating until the code runs without errors. Do not present code to the user until `convert_to_reproducible_json()` succeeds without exceptions.**

**Common errors to check:**
- Missing imports
- Incorrect parameter names
- Wrong data structure (e.g., DataFrame format)
- Invalid config keys
- Typo in method names
- Incorrect indentation
- Wrong quotation marks or brackets

**Iteration process:**
```
1. Generate code → 2. Create validation script → 3. Run validation
     ↑                                                      ↓
     └────────── ERROR? Fix code and go to step 1 ←─────────┘
                          ↓
                     NO ERROR
                          ↓
     Present working code to user
```

**Critical rule:** Never skip validation or show untested code. If the code fails validation three times, debug more carefully before trying again.

### 4. Clean Up Temporary Files

Once validation passes, delete the temporary script:

```python
import os
os.remove(temp_script_path)
```

**Never leave validation scripts on disk** - always clean up immediately after validation.

## Template for Validation Script

```python
"""
CanvasXpress code validation script.
Auto-generated for syntax verification.
"""

from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import convert_to_reproducible_json
import pandas as pd  # Add other imports as needed


def validate_chart():
    """Validate that the chart code executes without errors."""

    # Data definition
    # ... insert user's data code here ...

    # Chart configuration
    cx = CanvasXpress(
        # ... insert user's config here ...
    )

    # Validation check
    json_output = convert_to_reproducible_json(cx)
    return True


if __name__ == "__main__":
    try:
        validate_chart()
        print("VALIDATION PASSED")
    except Exception as e:
        print(f"VALIDATION FAILED: {e}")
        raise
```

## Validation Checklist

Before presenting code to the user, verify:
- [ ] All imports are correct and available
- [ ] DataFrame/data structure matches CanvasXpress expectations
- [ ] Config dictionary uses valid keys and values
- [ ] Method names are spelled correctly
- [ ] Indentation and syntax are correct
- [ ] Temporary validation file has been deleted

## Best Practices

1. **Be thorough** - Always validate before showing code to users
2. **Be efficient** - Don't show the validation process to users, only the final working code
3. **Be clear** - If code needs multiple iterations to fix, document what was learned
4. **Be clean** - Always delete temporary validation files
5. **Be safe** - Use `convert_to_reproducible_json` instead of rendering functions for validation

## When to Skip Validation

Validation can be skipped when:
- Using well-known patterns from the canvasxpress_charts or notebook_builder skills
- The user is providing their own data/code and just needs CanvasXpress integration tips
- The code is already known to work from previous successful generations

However, **always validate when generating new or modified code** for the first time.

## Example: Full Validation Cycle

**Step 1: Generate code**
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd

df = pd.DataFrame({'Month': ['Jan', 'Feb', 'Mar'], 'Sales': [100, 200, 300]})
cx = CanvasXpress(data=df, config={"graphType": "Bar", "title": "Sales"})
graph(cx)
```

**Step 2: Create validation script**
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import convert_to_reproducible_json
import pandas as pd

df = pd.DataFrame({'Month': ['Jan', 'Feb', 'Mar'], 'Sales': [100, 200, 300]})
cx = CanvasXpress(data=df, config={"graphType": "Bar", "title": "Sales"})
json_output = convert_to_reproducible_json(cx)
```

**Step 3: Run validation**
```bash
python /tmp/cx_validate_123456.py
```

**Step 4: Clean up**
```bash
rm /tmp/cx_validate_123456.py
```

**Step 5: Present working code to user**
```python
from canvasxpress.canvas import CanvasXpress
from canvasxpress.plot import graph
import pandas as pd

df = pd.DataFrame({'Month': ['Jan', 'Feb', 'Mar'], 'Sales': [100, 200, 300]})
cx = CanvasXpress(data=df, config={"graphType": "Bar", "title": "Sales"})
graph(cx)
```

<small>This skill should be used in conjunction with canvasxpress_charts and notebook_builder skills to ensure all generated CanvasXpress code is syntactically correct.</small>
