# CA_PATH_PROG(VARIABLE, PROG-TO-CHECK-FOR, [VALUE-IF-NOT-FOUND], [PATH = $PATH])
# -------------------------------------------------------------------------------
#
# extends AC_PATH_PROG
# requires CA_PROG_CYGPATH_M
# mark the $1 as precious with AC_ARG_VAR
#
AC_DEFUN([CA_PATH_PROG], [
    AC_PATH_PROG($1, $2, $3, $4)
    AS_VAR_IF(
        $1,
        [],
        [AC_MSG_FAILURE(the $2 program was not found on PATH)],
    )
    AC_ARG_VAR($1, the $2 program)
    # checking for $2 program with dos path
    AC_CACHE_CHECK(
        for $2 with dos path,
        ca_cv_dospath_$1,
        [AS_VAR_IF(
            DOS_$1,
            [],
            [AS_VAR_SET(ca_cv_dospath_$1, `${CYGPATH_M} ${$1}`)],
            [AS_VAR_SET(ca_cv_dospath_$1, ${DOS_$1})]
        )],
    )
    AC_SUBST(DOS_$1, ${ca_cv_dospath_$1})
    AC_ARG_VAR(DOS_$1, the $2 program with dos path)
])
