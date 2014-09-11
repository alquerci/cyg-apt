# CA_PATH_PROG(VARIABLE, PROG-TO-CHECK-FOR, [VALUE-IF-NOT-FOUND], [PATH = $PATH])
# -------------------------------------------------------------------------------
#
# extends AC_PATH_PROG
# requires CA_PROG_CYGPATH_M
# mark the $1 as precious with AC_ARG_VAR
#
AC_DEFUN([CA_PATH_PROG], [
    AC_CACHE_CHECK(
        for $2,
        [AS_TR_SH(ca_cv_path_$1)],
        {
            [AC_PATH_PROG($1, $2, $3, $4)]
        } [AS_MESSAGE_FD]>/dev/null [AS_MESSAGE_LOG_FD]>/dev/null
        [AS_VAR_IF(
            $1,
            [],
            [AC_MSG_FAILURE(the $2 program was not found on PATH)],
        )]
        [AS_VAR_SET([AS_TR_SH(ca_cv_path_$1)], `${CYGPATH_M} ${$1}`)]
        [AS_VAR_SET([AS_TR_SH($1)], ${[AS_TR_SH(ca_cv_path_$1)]})],
    )
    AC_ARG_VAR($1, the $2 program)
])
