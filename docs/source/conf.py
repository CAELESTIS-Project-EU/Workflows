# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import inspect
import os
import subprocess as subp
import sys

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('../../'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.linkcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    'sphinx_gallery.gen_gallery',
    'matplotlib.sphinxext.plot_directive',
]

napoleon_google_docstring = False
napoleon_use_param = False
napoleon_use_ivar = True

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Caelestis-Eu Simulations Service'
copyright = '2025, Caelestis'
author = 'Barcelona Supercomputing Center (BSC)'

autodoc_mock_imports = ['pycompss']
language = "en"

sphinx_gallery_conf = {
    'examples_dirs': ['../scipy-sphinx-theme/examples'],
}

templates_path = ['_templates']


source_suffix = {'.rst': 'restructuredtext'}

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'scipy'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    "edit_link": False,
    "sidebar": "right",
    "scipy_org_logo": False,
    "rootlinks": []
}

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = [os.path.join(os.pardir, 'scipy-sphinx-theme', '_theme')]



def linkcode_resolve(domain, info):
    """
    Determine the URL corresponding to Python object
    """
    if domain != 'py':
        return None

    modname = info['module']
    fullname = info['fullname']

    submod = sys.modules.get(modname)
    if submod is None:
        return None

    try:
        obj = submod
        for part in fullname.split('.'):
            obj = getattr(obj, part)
    except (AttributeError, IndexError):
        return None

    # strip decorators, which would resolve to the source of the decorator
    # possibly an upstream bug in getsourcefile, bpo-1764286
    try:
        unwrap = inspect.unwrap
    except AttributeError:
        pass
    else:
        obj = unwrap(obj)

    fn = None
    try:
        fn = inspect.getsourcefile(obj)
    except Exception:
        pass
    if not fn:
        return None

    try:
        source, lineno = inspect.getsourcelines(obj)
    except Exception:
        lineno = None

    if lineno:
        linespec = "#L%d-L%d" % (lineno, lineno + len(source) - 1)
    else:
        linespec = ""

    modname = inspect.getmodule(obj).__name__

    try:
        branch = subp.getoutput(["git", "rev-parse", "--abbrev-ref", "HEAD"]).strip()
        if not branch:
            branch = "master"
    except subp.CalledProcessError as e:
        print("Error getting branch name. I will use 'master'.")
        branch = "master"

    return "http://github.com/bsc-wdc/dislib/blob/%s/%s.py%s" \
           % (branch, modname.replace(".", "/"), linespec)