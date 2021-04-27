# Document the project
rm -rf build docs site mkdocs.yml
export SITE_DIR="site"
pydoc-markdown --build --site-dir $SITE_DIR
cp -R build/docs/content docs
cp -R readme/examples docs/examples
cp -R readme/images docs/images
cp build/docs/mkdocs.yml mkdocs.yml
sed -i 's/docs_dir: content/docs_dir: docs/' mkdocs.yml
mkdocs build
