SUBDIRS = src doc tools

DIST_SUBDIRS = $(SUBDIRS) \
    build-aux

dist_doc_DATA = \
    $(srcdir)/AUTHORS \
    $(srcdir)/CONTRIBUTING.md \
    $(srcdir)/CONVENTIONS.md \
    $(srcdir)/COPYING \
    $(srcdir)/ChangeLog \
    $(srcdir)/INSTALL.md \
    $(srcdir)/LICENSE \
    $(srcdir)/NEWS.md \
    $(srcdir)/TODO \
    $(srcdir)/README.md

ACLOCAL_AMFLAGS = -I m4

dist-hook:
	echo '$(VERSION)' > $(distdir)/version
