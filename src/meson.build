pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'sittytalky'
assets_path = moduledir / '.assets'
gnome = import('gnome')

gnome.compile_resources('sittytalky',
  'sittytalky.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')
py_installation = python.find_installation('python3')

conf = configuration_data()
conf.set('PYTHON', py_installation.path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)
conf.set('assests_path', assets_path)

configure_file(
  input: 'sittytalky.in',
  output: 'sittytalky',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

install_subdir(
    'lib',
    install_dir: py_installation.get_install_dir()
)

# asset installation
subdir('assets')

sittytalky_sources = [
  '__init__.py',
  'main.py',
  'window.py',
]

install_data(sittytalky_sources, install_dir: moduledir)
