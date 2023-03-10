# The command line passed variable VERSION is used to set the version string
# in the metadata and in the generated zip-file. If no VERSION is passed, the
# version string in the debian control metadata is used.
#

ifndef VERSION
	VERSION = $(shell cat deb/debian/control | grep Standards-Version | cut -d' ' -f2)
endif

ifndef GIT2GO_VERSION
	GIT2GO_VERSION = $(shell cat kubescape.spec | grep "global git2go_version" | cut -d' ' -f3)
endif

ifndef LIBGIT2_VERSION
	LIBGIT2_VERSION = $(shell cat kubescape.spec | grep "global libgit2_version" | cut -d' ' -f3)
endif

export GOCACHE=$(PWD)/cache

clean:
	-rm -fR rpmbuild
	-rm -fR *.deb
	-rm -fR *.rpm
	-rm -fR *.src.tar.gz
	-rm -fR *.tar.xz
	-rm -fR *.dsc
	-rm -fR *.changes
	-rm -fR *.buildinfo
	-rm -fR deb/completion
	-rm -fR deb/kubescape
	-rm -fR deb/debian/kubescape*
	-rm -fR deb/debian/debhelper-build-stamp
	-rm -fR deb/debian/files
	-rm -fR deb/debian/.debhelper
	-rm -fR *.upload

prepare:
	rm -rf deb/kubescape
	curl --output kubescape.src.tar.gz -L https://github.com/kubescape/kubescape/archive/v$(VERSION)/kubescape-$(VERSION).tar.gz
	curl --output git2go.src.tar.gz -L https://github.com/libgit2/git2go/archive/v$(GIT2GO_VERSION)/git2go-$(GIT2GO_VERSION).tar.gz
	curl --output libgit2.src.tar.gz -L https://github.com/libgit2/libgit2/archive/v$(LIBGIT2_VERSION)/libgit2-$(LIBGIT2_VERSION).tar.gz
	cd deb; tar -xf ../kubescape.src.tar.gz
	mv deb/kubescape-$(VERSION) deb/kubescape
	cd deb/kubescape; tar -xf ../../git2go.src.tar.gz; \
		rm -rf git2go; mv git2go-$(GIT2GO_VERSION) git2go
	cd deb/kubescape/git2go; tar -xf ../../../libgit2.src.tar.gz; \
		rm -rf libgit2; mv libgit2-$(LIBGIT2_VERSION) libgit2

vendor: clean prepare
	cd deb/kubescape; go mod vendor; go generate -mod vendor ./...
	cd deb/kubescape/git2go; go mod vendor; go generate -mod vendor ./...; mv libgit2 vendor
	sed -i 's/go install /go install -mod vendor /' deb/kubescape/git2go/Makefile

deb: vendor
	cd deb; dpkg-buildpackage -F -d;

dsc: vendor
	cd deb; \
		dpkg-buildpackage -S -d;

ppa: dsc
	dput kubescape *source.changes

rpmdir:
	mkdir -p rpmbuild/BUILD
	mkdir -p rpmbuild/RPMS
	mkdir -p rpmbuild/SOURCES
	mkdir -p rpmbuild/SPECS
	mkdir -p rpmbuild/SRPMS

rpm: rpmdir
	rpmbuild --undefine=_disable_source_fetch -ba kubescape.spec -D "_topdir $(PWD)/rpmbuild" -D 'debug_package %{nil}'
