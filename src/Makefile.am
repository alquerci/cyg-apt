dist_pkgdata_DATA = $(srcdir)/cygwin.sig

if CA_WANT_BATCH
    bin_SCRIPTS = cyg-apt.bat
else
    bin_SCRIPTS = cyg-apt
endif

CLEANFILES = cyg-apt \
    cyg-apt.bat \
    cyg-apt.py

EXTRA_DIST = $(srcdir)/main.py \
    $(srcdir)/main.batin

check-local:
	cd $(srcdir) && $(PYTHON) -m cygapt.test.__main__ -v

installcheck-local:
	cd '$(DESTDIR)$(pkglibdir)' && $(PYTHON) -m cygapt.test.__main__ -v

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
	        -e s,'@'pkglibdir'@','$(pkglibdir)',g \
	        -e s,'@'dos_pkglibdir'@','$(shell $(CYGPATH_M) '$(pkglibdir)')',g \
	    > $@

.PHONY: cyg-apt.bat
cyg-apt.bat: $(srcdir)/main.batin
	cat $^ \
	    | $(SED) \
	        -e s,'@'PYTHON'@','$(shell $(CYGPATH_M) '$(PYTHON)')',g \
	        -e s,'@'mainpath'@','$(shell $(CYGPATH_M) '$(pkgpythondir)/cyg-apt.py')',g \
	    > $@

.PHONY: cyg-apt.py
cyg-apt.py: $(srcdir)/main.py
	cat $^ \
	    | $(SED) \
	        -e s,'@'pkglibdir'@','$(pkglibdir)',g \
	        -e s,'@'dos_pkglibdir'@','$(shell $(CYGPATH_M) '$(pkglibdir)')',g \
	    > $@

pkgpythondir = $(pkglibdir)/cygapt
pkgpython_PYTHON = \
    $(srcdir)/cygapt/__init__.py \
    $(srcdir)/cygapt/argparser.py \
    $(srcdir)/cygapt/copying.py \
    $(srcdir)/cygapt/cygapt.py \
    $(srcdir)/cygapt/exception.py \
    $(srcdir)/cygapt/main.py \
    $(srcdir)/cygapt/ob.py \
    $(srcdir)/cygapt/path_mapper.py \
    $(srcdir)/cygapt/setup.py \
    $(srcdir)/cygapt/structure.py \
    $(srcdir)/cygapt/url_opener.py \
    $(srcdir)/cygapt/utils.py \
    cyg-apt.py \
    cygapt/config.py

pkgpython_testdir = $(pkgpythondir)/test
pkgpython_test_PYTHON = \
    $(srcdir)/cygapt/test/__init__.py \
    $(srcdir)/cygapt/test/__main__.py \
    $(srcdir)/cygapt/test/test_argparser.py \
    $(srcdir)/cygapt/test/test_cygapt.py \
    $(srcdir)/cygapt/test/test_ob.py \
    $(srcdir)/cygapt/test/test_path_mapper.py \
    $(srcdir)/cygapt/test/test_setup.py \
    $(srcdir)/cygapt/test/test_url_opener.py \
    $(srcdir)/cygapt/test/test_utils.py \
    $(srcdir)/cygapt/test/utils.py

pkgpython_test_casedir = $(pkgpython_testdir)/case
pkgpython_test_case_PYTHON = \
    $(srcdir)/cygapt/test/case/__init__.py \
    $(srcdir)/cygapt/test/case/exception.py

pkgpython_test_case_py2dir = $(pkgpython_test_casedir)/py2
pkgpython_test_case_py2_PYTHON = \
    $(srcdir)/cygapt/test/case/py2/__init__.py \
    $(srcdir)/cygapt/test/case/py2/exception.py

pkgpython_test_case_py2_minor6dir = $(pkgpython_test_case_py2dir)/minor6
pkgpython_test_case_py2_minor6_PYTHON = \
    $(srcdir)/cygapt/test/case/py2/minor6/__init__.py \
    $(srcdir)/cygapt/test/case/py2/minor6/exception.py

pkgpython_test_fixturesdir = $(pkgpython_testdir)/fixtures

pkgpython_test_fixtures_utilsdir = $(pkgpython_test_fixturesdir)/utils
dist_pkgpython_test_fixtures_utils_DATA = \
    $(srcdir)/cygapt/test/fixtures/utils/README \
    $(srcdir)/cygapt/test/fixtures/utils/cyglsa-bad1.dll \
    $(srcdir)/cygapt/test/fixtures/utils/cyglsa-bad2.dll \
    $(srcdir)/cygapt/test/fixtures/utils/cyglsa-bad3.dll \
    $(srcdir)/cygapt/test/fixtures/utils/cyglsa-bad4.dll \
    $(srcdir)/cygapt/test/fixtures/utils/cyglsa.dll \
    $(srcdir)/cygapt/test/fixtures/utils/cyglsa64.dll
