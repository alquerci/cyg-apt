# Process this file with autoconf to produce a configure script.

AC_PREREQ(2.64)
AC_INIT(
    cyg-apt,
    m4_esyscmd_s(build-aux/git-version-gen --fallback='1.1.0-DEV'),
    https://github.com/nylen/cyg-apt/issues,
)
AC_CONFIG_SRCDIR(src/cygapt/config.pyin)
AC_CONFIG_MACRO_DIR(m4)
AC_CONFIG_AUX_DIR(build-aux)
AM_INIT_AUTOMAKE(foreign -Wall -Werror subdir-objects)


# checks for configure options
AC_ARG_ENABLE(
    bash-completion,
    [AS_HELP_STRING(
        --enable-bash-completion=DIR,
        include bash-completion,
    )],
    [AS_VAR_IF(
        enable_bash_completion,
        no,
        [],
        [AC_MSG_CHECKING(for bash-completion directory)],
    )]
    [AS_VAR_IF(
        enable_bash_completion,
        yes,
        [AS_VAR_SET(enable_bash_completion)],
    )]
    [AS_VAR_IF(
        enable_bash_completion,
        no,
        [],
        [AC_MSG_RESULT(${enable_bash_completion})],
    )]
    [AS_VAR_IF(
        enable_bash_completion,
        [],
        [AC_MSG_ERROR(
            [AS_ESCAPE(
required value for --enable-bash-completion option
it can be set with one of the following directories:

    - pkg-config --variable=completionsdir bash-completion
    - ${BASH_COMPLETION_DIR}
    - /etc/bash_completion.d,
            )],
        )],
    )]
    [AC_SUBST(bash_completiondir, ${enable_bash_completion})],
    [AS_VAR_SET(enable_bash_completion, no)],
)
AM_CONDITIONAL(
    CA_WANT_BASH_COMPLETION,
    test x"no" != "x${enable_bash_completion}",
)


# checks for programs
AC_PROG_SED
CA_PATH_PYTHON(2.6, , , 3)
CA_PROG_CYGPATH_M
CA_PATH_PROG(GPG, gpg)
CA_PATH_PROG(LN, ln)
CA_PATH_PROG(BASH, bash)
CA_PATH_PROG(PS, ps)
CA_PATH_PROG(XZ, xz)
CA_PATH_PROG(MOUNT, mount)
CA_PATH_PROG(CYGCHECK, cygcheck, false)
CA_PATH_PROG(CYGPATH, cygpath, echo)
CA_PATH_PROG(ENV, env)


# checks for libraries
AS_VAR_IF(
    PYTHON_VERSION,
    2.6,
    [AC_MSG_CHECKING(for ${am_display_PYTHON} argparse module)]
    [AS_IF(
        ${PYTHON} -c [AS_ESCAPE(import argparse, [ ])] >/dev/null 2>&1,
        [AC_MSG_RESULT(yes)],
        [AC_MSG_FAILURE(
            failed to find required ${am_display_PYTHON} argparse module
        )]dnl
    )],
)


# checks for header files


# checks for types


# checks for structures


# checks for compiler characteristics


# checks for library functions


# checks for system services


AC_CONFIG_FILES(
    Makefile
    build-aux/Makefile
    src/Makefile
    src/cygapt/config.py:src/cygapt/config.pyin
    doc/Makefile
    tools/Makefile
)
AC_OUTPUT
