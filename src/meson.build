pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'sittytalky'
gnome = import('gnome')

gnome.compile_resources('sittytalky',
  'sittytalky.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'sittytalky.in',
  output: 'sittytalky',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

py_installation = python.find_installation('python3')
install_subdir(
    'lib',
    install_dir: py_installation.get_install_dir()
)

sittytalky_sources = [
  '__init__.py',
  'main.py',
  'window.py',
]

install_data(sittytalky_sources, install_dir: moduledir)
