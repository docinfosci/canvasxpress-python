import os

from canvasxpress.util.example.generator import \
    generate_canvasxpress_code_from_json_file


def test_code_generator():
    example_json_path = os.path.join(
        os.path.dirname(__file__),
        "test.json"
    )
    candidate = generate_canvasxpress_code_from_json_file(
        example_json_path
    )

    valid_result_path = os.path.join(
        os.path.dirname(__file__),
        "valid_result.txt"
    )

    # # Used to maintain the test, with manual review after the write.
    # with open(valid_result_path, 'w') as valid_result_file:
    #     valid_result_file.write(candidate)

    with open(valid_result_path, 'r') as valid_result_file:
        valid_result = valid_result_file.read()
        assert valid_result == candidate
