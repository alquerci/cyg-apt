SUBDIRS = src doc tools

DIST_SUBDIRS = $(SUBDIRS) \
    build-aux

dist_doc_DATA = \
    AUTHORS \
    CONTRIBUTING.md \
    CONVENTIONS.md \
    COPYING \
    ChangeLog \
    INSTALL.md \
    LICENSE \
    NEWS.md \
    TODO \
    README.md

ACLOCAL_AMFLAGS = -I m4

dist-hook:
	echo '$(VERSION)' > $(distdir)/version
