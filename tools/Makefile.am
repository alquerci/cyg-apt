if CA_WANT_BASH_COMPLETION
    dist_bash_completion_SCRIPTS = cyg-apt
endif

CLEANFILES = cyg-apt
EXTRA_DIST = $(srcdir)/completion.bash
 
cyg-apt: $(srcdir)/completion.bash
	cp $^ $@
