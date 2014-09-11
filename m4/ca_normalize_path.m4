# CA_NORMALIZE_PATH(PATH)
# -----------------------
#
# replace backslashes with slash
#
AC_DEFUN([CA_NORMALIZE_PATH], [
    AS_CASE(
        ${$1},
        *[AS_ESCAPE(\)]*,
        [AC_MSG_CHECKING(for $1 without backslash)]
        [AS_VAR_SET(
            $1,
            `[AS_ECHO(${$1})] | tr [AS_ESCAPE([AS_ESCAPE(\\)])] /`,
        )]
        [AC_MSG_RESULT(${$1})],
    )
])
