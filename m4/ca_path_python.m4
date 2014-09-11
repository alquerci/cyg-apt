# CA_PATH_PYTHON([MINIMUM-VERSION], [ACTION-IF-FOUND], [ACTION-IF-NOT-FOUND])
# ---------------------------------------------------------------------------
#
# extends AM_PATH_PYTHON
#
AC_DEFUN([CA_PATH_PYTHON], [
    AM_PATH_PYTHON($1, $2, $3)
    CA_NORMALIZE_PATH(pyexecdir)
    CA_NORMALIZE_PATH(pythondir)
])
