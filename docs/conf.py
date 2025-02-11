# SunPy documentation build configuration file.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this file.
#
# All configuration values have a default. Some values are defined in
# the global Astropy configuration which is loaded here before anything else.
# See astropy.sphinx.conf for which values are set there.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.insert(0, os.path.abspath('..'))
# IMPORTANT: the above commented section was generated by sphinx-quickstart, but
# is *NOT* appropriate for sunpy or sunpy affiliated packages. It is left
# commented out with this explanation to make it clear why this should not be
# done. If the sys.path entry above is added, when the astropy.sphinx.conf
# import occurs, it will import the *source* version of astropy instead of the
# version installed (if invoked as "make html" or directly with sphinx), or the
# version in the build directory (if "python setup.py build_docs" is used).
# Thus, any C-extensions that are needed to build the documentation will *not*
# be accessible, and the documentation will not build correctly.

# ITS THE WILD WEST IN HERE
# flake8: noqa

import os
import sys
import pathlib
import datetime

# -- Import Base config from sphinx-astropy ------------------------------------
try:
    from sphinx_astropy.conf.v1 import *
except ImportError:
    print('ERROR: the documentation requires the "sphinx-astropy" package to be installed')
    sys.exit(1)

try:
    import sphinx_gallery
    from sphinx_gallery.sorting import ExplicitOrder
    if on_rtd and os.environ.get('READTHEDOCS_PROJECT').lower() != 'sunpy':
        # Gallery takes too long on RTD to build unless you have extra build time.
        has_sphinx_gallery = False
    else:
        has_sphinx_gallery = True
except ImportError:
    has_sphinx_gallery = False

if on_rtd:
    os.environ['SUNPY_CONFIGDIR'] = '/home/docs/'
    os.environ['HOME'] = '/home/docs/'
    os.environ['LANG'] = 'C'
    os.environ['LC_ALL'] = 'C'

try:
    import zeep
except ImportError:
    raise Exception(e, 'ERROR: zeep could not be imported. Building the documentation requires '
                    'the "zeep" package to be installed')

try:
    import skimage
except ImportError as e:
    raise Exception(e, 'ERROR: skimage could not be imported. Building the documentation requires '
                    'the "scikit-image" package to be installed')

try:
    import drms
except ImportError as e:
    raise Exception(e, 'ERROR: drms could not be imported. Building the documentation requires '
                    'the "drms" package to be installed')

try:
    import glymur
except ImportError as e:
    raise Exception(e, 'ERROR: glymur could not be imported. Building the documentation requires '
                    'the "glymur" package to be installed')

try:
    import sqlalchemy
except ImportError as e:
    raise Exception(e, 'ERROR: sqlalchemy could not be imported. Building the documentation requires '
                    'the "sqlalchemy" package to be installed')

try:
    import astroquery
except ImportError as e:
    raise Exception(e, 'ERROR: astroquery could not be imported. Building the documentation requires '
                    'the "astroquery" package to be installed')

try:
    import jplephem
except ImportError as e:
    raise Exception(e, 'ERROR: jplephem could not be imported. Building the documentation requires '
                    'the "jplephem" package to be installed')

from pkg_resources import get_distribution  # noqa  isort:skip
versionmod = get_distribution('sunpy')

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
# The short X.Y version.
version = '.'.join(versionmod.version.split('.')[:3])
# The full version, including alpha/beta/rc tags.
release = versionmod.version.split('+')[0]
# Is this version a development release
is_development = '.dev' in release

# -- Shut up numpy warnings from WCSAxes --------------------------------------
import numpy as np  # noqa  isort:skip

np.seterr(invalid='ignore')

# -- Download Sample Data -----------------------------------------------------
import sunpy.data.sample  # noqa  isort:skip

# -- General configuration ----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '2.0'

# To perform a Sphinx version check that needs to be more specific than
# major.minor, call `check_sphinx_version("x.y.z")` here.
check_sphinx_version(needs_sphinx)

# Add any custom intersphinx for SunPy
intersphinx_mapping.pop('h5py', None)
intersphinx_mapping['sqlalchemy'] = ('https://docs.sqlalchemy.org/en/latest/', None)
intersphinx_mapping['pandas'] = ('https://pandas.pydata.org/pandas-docs/stable/', None)
intersphinx_mapping['skimage'] = ('https://scikit-image.org/docs/stable/', None)
intersphinx_mapping['drms'] = ('https://docs.sunpy.org/projects/drms/en/stable/', None)
intersphinx_mapping['parfive'] = ('https://parfive.readthedocs.io/en/latest/', None)

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns.append('_templates')

# Add any paths that contain templates here, relative to this directory.
if 'templates_path' not in locals():  # in case parent conf.py defines it
    templates_path = []
templates_path.append('_templates')

# For the linkcheck
linkcheck_ignore = [r"https://doi.org/\d+",
                    r"https://riot.im/\d+",
                    r"https://github.com/\d+",
                    r"https://docs.sunpy.org/\d+"]
linkcheck_anchors = False

# This is added to the end of RST files - a good place to put substitutions to
# be used globally.
rst_epilog = """
.. SunPy
.. _SunPy: https://sunpy.org
.. _`SunPy mailing list`: https://groups.google.com/group/sunpy
.. _`SunPy dev mailing list`: https://groups.google.com/group/sunpy-dev
"""

# -- Project information ------------------------------------------------------
project = 'SunPy'
author = 'The SunPy Community'
copyright = '{}, {}'.format(datetime.datetime.now().year, author)

try:
    from sunpy_sphinx_theme.conf import *
except ImportError:
    html_theme = 'default'

try:
    import ruamel.yaml as yaml
    has_yaml = True
    # Load data about stability
    with open('./dev_guide/sunpy_stability.yaml', 'r') as estability:
        sunpy_modules = yaml.load(estability.read(), Loader=yaml.Loader)

    html_context = {
        'sunpy_modules': sunpy_modules
    }

    def rstjinja(app, docname, source):
        """
        Render our pages as a jinja template for fancy templating goodness.
        """
        # Make sure we're outputting HTML
        if app.builder.format != 'html':
            return
        src = source[0]
        if "Current status" in src[:20]:
            rendered = app.builder.templates.render_string(
                src, app.config.html_context
            )
            source[0] = rendered
except ImportError:
    has_yaml = False
    html_context = {}
    print('Warning: Stability of SunPy API page of the documentation requires the ruamel.yaml package to be installed')

# The name of an image file (within the static path) to use as favicon of the
# docs. This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "./logo/favicon.ico"

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = f'{project} v{release}'

# Output file base name for HTML help builder.
htmlhelp_basename = project + 'doc'

# A dictionary of values to pass into the template engine’s context for all pages.
html_context['to_be_indexed'] = ['stable', 'latest']

# -- Options for LaTeX output --------------------------------------------------
# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [('index', project + '.tex', project + ' Documentation', author, 'manual')]

# -- Options for manual page output --------------------------------------------
# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [('index', project.lower(), project + ' Documentation', [author], 1)]

# -- Swap to Napoleon ---------------------------------------------------------
# Remove numpydoc
extensions.remove('numpydoc')
extensions.append('sphinx.ext.napoleon')

# Disable having a separate return type row
napoleon_use_rtype = False
# Disable google style docstrings
napoleon_google_docstring = False

extensions += ['sphinx_astropy.ext.edit_on_github', 'sphinx.ext.doctest', 'sphinx.ext.githubpages']

# -- Options for the edit_on_github extension ---------------------------------
# Don't import the module as "version" or it will override the
# "version" configuration parameter
edit_on_github_project = "sunpy/sunpy"
if 'dev' not in release:
    edit_on_github_branch = f"{version}"
else:
    edit_on_github_branch = "master"
edit_on_github_source_root = ""
edit_on_github_doc_root = "docs"
edit_on_github_skip_regex = '_.*|generated/.*'
github_issues_url = 'https://github.com/sunpy/sunpy/issues/'

# -- Options for the Sphinx gallery -------------------------------------------
if has_sphinx_gallery:
    extensions += ["sphinx_gallery.gen_gallery"]
    path = pathlib.Path.cwd()
    example_dir = path.parent.joinpath('examples')
    sphinx_gallery_conf = {
        'backreferences_dir':
        path.joinpath('generated', 'modules'),  # path to store the module using example template
        # execute all examples except those that start with "skip_"
        'filename_pattern': '^((?!skip_).)*$',
        'examples_dirs': example_dir,  # path to the examples scripts
        'subsection_order': ExplicitOrder([(os.path.join('..', 'examples/acquiring_data')),
                                           (os.path.join('..', 'examples/map')),
                                           (os.path.join('..', 'examples/time_series')),
                                           (os.path.join('..', 'examples/units_and_coordinates')),
                                           (os.path.join('..', 'examples/plotting')),
                                           (os.path.join('..', 'examples/saving_and_loading_data')),
                                           (os.path.join('..', 'examples/computer_vision_techniques'))]),
        # path to save gallery generated examples
        'gallery_dirs': path.joinpath('generated', 'gallery'),
        'default_thumb_file': path.joinpath('logo', 'sunpy_icon_128x128.png'),
        'abort_on_example_error': False,
        'plot_gallery': True
    }


"""
Write the latest changelog into the documentation.
"""
target_file = os.path.abspath("./whatsnew/latest_changelog.txt")
try:
    from sunpy.util.towncrier import generate_changelog_for_docs
    if is_development:
        generate_changelog_for_docs("../", target_file)
except Exception as e:
    print(f"Failed to add changelog to docs with error {e}.")
# Make sure the file exists or else sphinx will complain.
open(target_file, 'a').close()


def setup(app):
    if not has_sphinx_gallery:
        import warnings
        warnings.warn('The sphinx_gallery extension is not installed, so the '
                      'gallery will not be built. You will probably see '
                      'additional warnings about undefined references due '
                      'to this.')
    if has_yaml:
        app.connect("source-read", rstjinja)
