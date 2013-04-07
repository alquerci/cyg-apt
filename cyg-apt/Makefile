CONSOLE = $(SD_BUILD)/$(ID_LIBEXEC)/$(EXENAME)/$(EXENAME)/console-prod
EXEC = $(EXENAME)

GPG_CYGWIN_PUBKEY = cygwin.sig

all:: build

build: $(SD_SRC) FORCE
	$(MKDIR) $(SD_BUILD)/$(ID_SYSCONF)/postinstall
	$(MKDIR) $(SD_BUILD)/$(ID_DATA)/$(EXENAME)
	$(MKDIR) $(SD_BUILD)/$(ID_LIBEXEC)/$(EXENAME)
	$(SHELL_PATH) ./postinstall-gen.sh > $(SD_BUILD)/$(ID_SYSCONF)/postinstall/$(EXENAME).sh
	$(CP) $(GPG_CYGWIN_PUBKEY) $(SD_BUILD)/$(ID_DATA)/$(EXENAME)
	$(CP) -r $(SD_SRC) $(SD_ROOT)/$(EXENAME) $(SD_VENDOR) $(SD_BUILD)/$(ID_LIBEXEC)/$(EXENAME)

install: build
	$(INSTALL) -d -m 755 $(ID_ROOT)/$(ID_SYSCONF)/postinstall
	$(INSTALL) -d -m 755 $(ID_ROOT)/$(ID_DATA)/$(EXENAME)
	$(INSTALL) -d -m 755 $(ID_ROOT)/$(ID_LIBEXEC)/$(EXENAME)
	$(INSTALL) $(GPG_CYGWIN_PUBKEY) $(ID_ROOT)/$(ID_DATA)/$(EXENAME)
	$(CP) -r $(SD_BUILD)/$(ID_LIBEXEC)/$(EXENAME) $(ID_ROOT)/$(ID_LIBEXEC)
	ln -sf "$(ID_ROOT)/$(ID_LIBEXEC)/$(EXENAME)/$(EXENAME)/console-prod" "$(ID_ROOT)/$(ID_EXEC)/$(EXEC)"
	$(INSTALL) $(SD_BUILD)/$(ID_SYSCONF)/postinstall/$(EXENAME).sh $(ID_ROOT)/$(ID_SYSCONF)/postinstall
	$(SHELL_PATH) $(ID_ROOT)/$(ID_SYSCONF)/postinstall/$(EXENAME).sh
	$(MV) $(ID_ROOT)/$(ID_SYSCONF)/postinstall/$(EXENAME).sh $(ID_ROOT)/$(ID_SYSCONF)/postinstall/$(EXENAME).sh.done

clean: FORCE
	$(RM) -r $(SD_BUILD)/$(ID_SYSCONF)/postinstall
	$(RM) -r $(SD_BUILD)/$(ID_DATA)/$(EXENAME)
	$(RM) -r $(SD_BUILD)/$(ID_LIBEXEC)/$(EXENAME)

.PHONY: FORCE
.EXPORT_ALL_VARIABLES:
