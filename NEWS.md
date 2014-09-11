News
====

* 2.0.0 ()

  * Removed the `setup_ini` configuration field

    Before:

    The `setup.ini` database is located at the following paths:

      - `<cachedir>/<mirror>/<arch>/setup.ini`

      - according to the value of the `setup_ini` configuration field,
          with the default one `/etc/setup/setup.ini`

    After:

    The `setup.ini` database is only located at the following path:

      - `<cachedir>/<mirror>/<arch>/setup.ini`

* 1.1.0 ()

  * the python library of this package is private so it does not install under
    the standard python `site-package` directory but on `pkglibdir`
    (default: `/usr/local/lib/cyg-apt`)

  * to build from source it requires the `automake` package

  * the build command line: `autoreconf -i && ./configure && make`
