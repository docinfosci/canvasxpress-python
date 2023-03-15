import os
from pathlib import Path

from selenium.webdriver.webkitgtk.webdriver import WebDriver
from skimage import img_as_float
from skimage.io import imread
from skimage.metrics import structural_similarity as ssim
from skimage.transform import resize

# https://scikit-image.org/docs/dev/auto_examples/transform/plot_ssim.html
IMAGE_SSIM_MIN_THRESHOLD = 0.75


def image_files_match(image1_path: Path, image2_path: Path) -> float:
    """
    Compares image files to determine the degree by which they match.
    :param image1_path: The path to one image
    :param image2_path: The path to another image
    :param ssim_min: The degree by which they must match
    :return: The match confidence from 0.0 to 1.0
    """
    image1 = imread(str(image1_path))
    image2 = imread(str(image2_path))

    image1_w, image1_h, image1_c = image1.shape

    image1r = resize(image1, (image1_w, image1_h))
    image2r = resize(image2, (image1_w, image1_h))

    return ssim(img_as_float(image1r), img_as_float(image2r), win_size = 7, channel_axis=1, multichannel=True)


def assert_chart_visuals_match(
    session: WebDriver,
    work_dir: str,
    chart_id: str,
    known_image: str = "known_chart.png",
) -> None:
    """
    Checks the default canvas image against a known image profile to ensure that
    the default graph is generally drawn as expected.  Requires that the calling
    function's package contains "known_chart.png" to compare against.
    :param session: A browser session to use for the test
    :param work_dir: The location for image manipulation
    :param chart_id: The HTML ID of the chart to test
    :param known_image: The name of the known image to compare against.
    :return: Fails if the browser image does not match
    """
    chart = session.find_element_by_id(chart_id)

    chart.screenshot(os.path.sep.join([work_dir, "browser_chart.png"]))

    known_chart_image = imread(os.path.sep.join([work_dir, known_image]))

    browser_chart_image = imread(os.path.sep.join([work_dir, "browser_chart.png"]))

    known_w, known_h, known_c = known_chart_image.shape
    browser_chart_image = resize(browser_chart_image, (known_w, known_h))

    ssim_result = ssim(
        img_as_float(known_chart_image),
        img_as_float(browser_chart_image),
        multichannel=True,
    )

    assert ssim_result >= IMAGE_SSIM_MIN_THRESHOLD, (
        f"Known and Browser images do not match: "
        f"SSIM is {ssim_result} but {IMAGE_SSIM_MIN_THRESHOLD} minimum required"
    )
