dist_pkgdata_DATA = cygwin.sig

if CA_WANT_BATCH
    bin_SCRIPTS = cyg-apt.bat
else
    bin_SCRIPTS = cyg-apt
endif

CLEANFILES = cyg-apt \
    cyg-apt.bat \
    cyg-apt.py

EXTRA_DIST = main.py \
    main.batin

check-local:
	cd $(srcdir) && $(PYTHON) -m cygapt.test.__main__ -v

installcheck-local:
	cd '$(DESTDIR)$(private_pythondir)' && $(PYTHON) -m cygapt.test.__main__ -v

install-data-hook:
	$(POST_INSTALL)
	if test x = x"$(DESTDIR)"; then \
	    $(GPG) --import --no-secmem-warning '$(pkgdatadir)/cygwin.sig' \
	    && if expr x"$(PYTHON_PLATFORM)" : x'cygwin.*' >/dev/null 2>&1; then \
	           '$(bindir)/cyg-apt' setup -q; \
	       else :; \
	       fi \
	else :; \
	fi

.PHONY: cyg-apt
cyg-apt: $(srcdir)/main.py
	cat $^ \
	    | $(SED) \
	        -e s,'@'ENV'@','$(ENV)',g \
	        -e s,'@'PYTHON'@','$(PYTHON)',g \
	        -e s,'@'pkglibdir'@','$(private_pythondir)',g \
	        -e s,'@'dos_pkglibdir'@','$(shell $(CYGPATH_M) '$(private_pythondir)')',g \
	    > $@

.PHONY: cyg-apt.bat
cyg-apt.bat: $(srcdir)/main.batin
	cat $^ \
	    | $(SED) \
	        -e s,'@'PYTHON'@','$(shell $(CYGPATH_M) '$(PYTHON)')',g \
	        -e s,'@'mainpath'@','$(shell $(CYGPATH_M) '$(private_pythondir)/cyg-apt.py')',g \
	    > $@

.PHONY: cyg-apt.py
cyg-apt.py: $(srcdir)/main.py
	cat $^ \
	    | $(SED) \
	        -e s,'@'pkglibdir'@','$(private_pythondir)',g \
	        -e s,'@'dos_pkglibdir'@','$(shell $(CYGPATH_M) '$(private_pythondir)')',g \
	    > $@

private_pythondir = $(pkgdatadir)/python
private_python_PYTHON = cyg-apt.py

private_python_cygaptdir = $(private_pythondir)/cygapt
private_python_cygapt_PYTHON = \
    cygapt/__init__.py \
    cygapt/argparser.py \
    cygapt/copying.py \
    cygapt/cygapt.py \
    cygapt/exception.py \
    cygapt/main.py \
    cygapt/ob.py \
    cygapt/path_mapper.py \
    cygapt/setup.py \
    cygapt/structure.py \
    cygapt/url_opener.py \
    cygapt/utils.py \
    cygapt/config.py

private_python_cygapt_testdir = $(private_python_cygaptdir)/test
private_python_cygapt_test_PYTHON = \
    cygapt/test/__init__.py \
    cygapt/test/__main__.py \
    cygapt/test/test_argparser.py \
    cygapt/test/test_cygapt.py \
    cygapt/test/test_ob.py \
    cygapt/test/test_path_mapper.py \
    cygapt/test/test_setup.py \
    cygapt/test/test_url_opener.py \
    cygapt/test/test_utils.py \
    cygapt/test/utils.py

private_python_cygapt_test_casedir = $(private_python_cygapt_testdir)/case
private_python_cygapt_test_case_PYTHON = \
    cygapt/test/case/__init__.py \
    cygapt/test/case/exception.py

private_python_cygapt_test_case_py2dir = $(private_python_cygapt_test_casedir)/py2
private_python_cygapt_test_case_py2_PYTHON = \
    cygapt/test/case/py2/__init__.py \
    cygapt/test/case/py2/exception.py

private_python_cygapt_test_case_py2_minor6dir = $(private_python_cygapt_test_case_py2dir)/minor6
private_python_cygapt_test_case_py2_minor6_PYTHON = \
    cygapt/test/case/py2/minor6/__init__.py \
    cygapt/test/case/py2/minor6/exception.py

private_python_cygapt_test_fixturesdir = $(private_python_cygapt_testdir)/fixtures

private_python_cygapt_test_fixtures_utilsdir = $(private_python_cygapt_test_fixturesdir)/utils
dist_private_python_cygapt_test_fixtures_utils_DATA = \
    cygapt/test/fixtures/utils/README \
    cygapt/test/fixtures/utils/cyglsa-bad1.dll \
    cygapt/test/fixtures/utils/cyglsa-bad2.dll \
    cygapt/test/fixtures/utils/cyglsa-bad3.dll \
    cygapt/test/fixtures/utils/cyglsa-bad4.dll \
    cygapt/test/fixtures/utils/cyglsa.dll \
    cygapt/test/fixtures/utils/cyglsa64.dll
