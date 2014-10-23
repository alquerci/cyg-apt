# CA_PATH_PYTHON([MINIMUM-VERSION], [ACTION-IF-FOUND], [ACTION-IF-NOT-FOUND], [MAXIMUM-VERSION])
# ---------------------------------------------------------------------------
#
# extends AM_PATH_PYTHON
#
AC_DEFUN([CA_PATH_PYTHON], [
    AM_PATH_PYTHON(
        $1,
        [CA_NORMALIZE_PATH(pyexecdir)]
        [CA_NORMALIZE_PATH(pythondir)]
        [AS_IF(
            test x != x"$4",
            [AC_MSG_CHECKING(whether ${am_display_PYTHON} version is < $4)]
            [AM_PYTHON_CHECK_VERSION(
                ${PYTHON},
                $4,
                [AC_MSG_RESULT(no)]
                [AC_MSG_ERROR(Python interpreter is too new)],
                [AC_MSG_RESULT(yes)],
            )],
        )]
        $2,
        $3,
    )
])
