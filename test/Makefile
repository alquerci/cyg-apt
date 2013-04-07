all:: sourcetest

TEST_SCRIPT = -m cygapt.test.__main__
ARGUMENTS =

sourcetest: FORCE
	@export PYTHONPATH="$(subst \,,$(SD_SRC)):$(PYTHONPATH)";\
$(PYTHON) $(TEST_SCRIPT) $(ARGUMENTS)

installtest: sourcetest FORCE

clean: FORCE


.PHONY: FORCE
.EXPORT_ALL_VARIABLES:
