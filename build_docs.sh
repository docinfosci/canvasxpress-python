# Document the project

# Clear any existing build artifacts
rm -rf build docs site mkdocs.yml

# Produce API documentation and mkdocs templates
export SITE_DIR="site"
pydoc-markdown --build --site-dir $SITE_DIR

# Move mkdocs templates to expected build locations for readthedocs.io build
cp -R build/docs/content docs
cp -R readme/examples docs/examples
cp -R readme/images docs/images
cp build/docs/mkdocs.yml mkdocs.yml
sed -i 's/docs_dir: content/docs_dir: docs/' mkdocs.yml

# For local inspection, also run mkdocs
mkdocs build
