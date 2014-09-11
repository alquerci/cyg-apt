# CA_PROG_CYGPATH_M
# -----------------
#
# define CYGPATH_M
# requires AC_PATH_PYTHON
#
AC_DEFUN([CA_PROG_CYGPATH_M], [
    {
        AC_PATH_PROG(CYGPATH, cygpath)
    } AS_MESSAGE_FD>/dev/null AS_MESSAGE_LOG_FD>/dev/null
    AC_CACHE_CHECK(
        for cygpath -m,
        ca_cv_path_cygpath_m,
        [AS_VAR_IF(
            CYGPATH,
            [],
            [AS_VAR_SET(ca_cv_path_cygpath_m, echo)],
            [AS_VAR_SET(
                ca_cv_path_cygpath_m,
                [AS_ESCAPE(${CYGPATH} -m, [ ])],
            )],
        )]
        [AS_CASE(
            ${PYTHON_PLATFORM},
            win*,
            [],
            [AS_VAR_SET(ca_cv_path_cygpath_m, false)]
        )]
        [AS_IF(
            ${ca_cv_path_cygpath_m} --version >/dev/null 2>/dev/null,
            [],
            [AS_VAR_SET(ca_cv_path_cygpath_m, echo)]dnl
        )],
    )
    AC_SUBST(CYGPATH_M, ${ca_cv_path_cygpath_m})
])
