# Default target
all:: build tools doc manifest

# vars utils
UTIL_SPACE := $() #

# Programs
SHELL_PATH = /bin/sh
CP = /bin/cp -f
RM = /bin/rm -f --preserve-root
MV = /bin/mv
MKDIR = /bin/mkdir -p
INSTALL = /bin/install
GZ = /bin/gzip --best
TAR = /bin/tar
PYTHON = /usr/bin/python
MAKE ?= /usr/bin/make
TOUCH = /bin/touch
FIND = /bin/find
SED = /bin/sed

# Source directories
SD_ROOT = $(subst $(UTIL_SPACE),\$(UTIL_SPACE),$(shell pwd))
SD_BUILD = $(SD_ROOT)/build
SD_SRC = $(SD_ROOT)/src
SD_TEST = $(SD_ROOT)/test
SD_DIST = $(SD_ROOT)/dist
SD_DOC = $(SD_ROOT)/doc
SD_TOOLS = $(SD_ROOT)/tools

# source environement
VERSION = 1.1.0rc1
VERSION_FILE = VERSION-FILE~
$(VERSION_FILE): FORCE
	@$(SHELL_PATH) ./VERSION-GEN
-include $(VERSION_FILE)

# install environement
EXENAME = cyg-apt

# Install directories
ID_ROOT = 
ID_PREFIX = usr
ID_LOCALSTATE = var
ID_SYSCONF = etc
ID_LIBEXEC = $(ID_PREFIX)/lib
ID_EXEC = $(ID_PREFIX)/bin
ID_DATA = $(ID_PREFIX)/share
ID_MAN = $(ID_DATA)/man
ID_INFO = $(ID_DATA)/info

build: FORCE
	@cd $(SD_SRC); $(MAKE)

doc: FORCE
	@cd $(SD_DOC); $(MAKE)

tools: FORCE
	@cd $(SD_TOOLS); $(MAKE)

manifest: build doc tools
	$(TOUCH) $(SD_BUILD)/$(ID_DATA)/doc/$(EXENAME)/MANIFEST;
	cd $(SD_BUILD); $(FIND) -P . -type f -or -type l | $(SED) -r "s/^\\./$$(echo $(ID_ROOT) | $(SED) s/\\//\\\\\\//g)/" > $(SD_BUILD)/$(ID_DATA)/doc/$(EXENAME)/MANIFEST;

test: build FORCE
	@cd $(SD_TEST); $(MAKE)

installtest: install FORCE
	@cd $(SD_TEST); $(MAKE) $@

install: install-manifest FORCE
	@cd $(SD_SRC); $(MAKE) $@
	@cd $(SD_DOC); $(MAKE) $@
	@cd $(SD_TOOLS); $(MAKE) $@

install-manifest: manifest
	$(CP) $(SD_BUILD)/$(ID_DATA)/doc/$(EXENAME)/MANIFEST $(ID_ROOT)/$(ID_DATA)/doc/$(EXENAME)/MANIFEST;

uninstall: FORCE
	while read path; do\
        $(RM) "$$path";\
    done < $(ID_ROOT)/$(ID_DATA)/doc/$(EXENAME)/MANIFEST;

$(SD_DIST)/$(EXENAME)-$(VERSION): build doc tools
	$(MKDIR) $(SD_DIST)/$(EXENAME)-$(VERSION)
	cd $(SD_BUILD); pwd; $(TAR) -jcf $(SD_DIST)/$(EXENAME)-$(VERSION)/$(EXENAME)-$(VERSION).tar.bz2 *
	git archive --prefix="$(EXENAME)-$(VERSION)/" --format=tar HEAD | bzip2 -c > $(SD_DIST)/$(EXENAME)-$(VERSION)/$(EXENAME)-$(VERSION)-src.tar.bz2
	$(CP) setup.hint $(SD_DIST)/$(EXENAME)-$(VERSION)

package: $(SD_DIST)/$(EXENAME)-$(VERSION)

packageclean:
	$(RM) -r $(SD_DIST)

clean: FORCE
	@cd $(SD_TEST); $(MAKE) $@
	@cd $(SD_SRC); $(MAKE) $@
	@cd $(SD_DOC); $(MAKE) $@
	@cd $(SD_TOOLS); $(MAKE) $@
	$(RM) $(VERSION_FILE)

mrproper: FORCE clean packageclean
	$(RM) -r $(SD_BUILD)

.PHONY: FORCE
.EXPORT_ALL_VARIABLES:
