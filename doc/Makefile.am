dist_man1_MANS = cyg-apt.1

CLEANFILES = cyg-apt.1
EXTRA_DIST = $(srcdir)/man.1

cyg-apt.1: $(srcdir)/man.1
	gzip -c $^ > $@
	gzip -t $@
