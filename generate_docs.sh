# Document the project
export SITE_DIR="site"
pydoc-markdown --build --site-dir $SITE_DIR
mv build/docs/content docs
mv build/docs/mkdocs.yml mkdocs.yml
mkdocs build
