#
# spec file for building package kubescape in openSUSE Build Service (OBS)
#
# Copyright (c) 2023 Hollow Man
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://github.com/kubescape/kubescape/issues
#


%global git2go_version 33.0.9
%global libgit2_version 1.3.0
Name:           kubescape
Version:        2.2.5
Release:        0
Summary:        CLI interface of a Kubernetes security platform
License:        Apache-2.0
Group:          Development/Tools/Other
URL:            https://github.com/kubescape/%{name}
Source0:        %{name}_%{version}.tar.xz
BuildRequires:  golang >= 1.19
BuildRequires:  pkg-config
BuildRequires:  cmake

%description
An open-source Kubernetes security platform for your IDE, CI/CD pipelines, and clusters.
It includes risk analysis, security, compliance, and misconfiguration scanning, saving
Kubernetes users and administrators precious time, effort, and resources.

%package bash-completion
Summary:        Bash Completion for %{name}
Group:          System/Shells
Requires:       bash-completion
Supplements:    packageand(%{name}:bash)
BuildArch:      noarch

%description bash-completion
The official bash completion script for %{name}, generated during the build.


%package zsh-completion
Summary:        Zsh Completion for %{name}
Group:          System/Shells
Requires:       zsh-completion
Supplements:    packageand(%{name}:zsh)
BuildArch:      noarch

%description zsh-completion
The official zsh completion script for %{name}, generated during the build.


%package fish-completion
Summary:        Fish Completion for %{name}
Group:          System/Shells
Requires:       fish-completion
Supplements:    packageand(%{name}:fish)
BuildArch:      noarch

%description fish-completion
The official fish completion script for %{name}, generated during the build.

%prep
%setup -q -n deb/%{name}

%build
export CGO_ENABLED=1
cd git2go && make install-static && cd ..
cp -r git2go/static-build vendor/github.com/libgit2/git2go/v*/
go build -mod=vendor -buildmode=pie -ldflags="-s -w -X github.com/kubescape/%{name}/v2/core/cautils.BuildNumber=v%{version}" -tags=static,gitenabled -o %{name}

%install
install -Dpm 0755 %{name} %{buildroot}%{_bindir}/%{name}

# Bash autocomplete file
%{buildroot}/%{_bindir}/%{name} completion bash > %{name}-autocomplete.sh
install -Dm 644 %{name}-autocomplete.sh %{buildroot}%{_datadir}/bash-completion/completions/%{name}

# Zsh autocomplete file
%{buildroot}/%{_bindir}/%{name} completion zsh > %{name}-autocomplete.sh
install -Dm 644 %{name}-autocomplete.sh %{buildroot}%{_datadir}/zsh/vendor-completions/_%{name}

# Fish autocomplete file
%{buildroot}/%{_bindir}/%{name} completion fish > %{name}-autocomplete.sh
install -Dm 644 %{name}-autocomplete.sh %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish

%check
if [ "$(%{buildroot}%{_bindir}/%{name} version)" != "Your current version is: v%{version} [git enabled in build: true]" ]; then exit 1; fi

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}

%files bash-completion
%{_datadir}/bash-completion

%files zsh-completion
%{_datadir}/zsh

%files fish-completion
%{_datadir}/fish

%changelog
* Mon Mar 13 2023 github-actions[bot] <github-actions[bot]@users.noreply.github.com> - 2.2.5
- Update to 2.2.5

* Sat Mar 11 2023 github-actions[bot] <github-actions[bot]@users.noreply.github.com> - 2.2.4
- Update to 2.2.4

* Sun Feb 26 2023 Hollow Man <hollowman@opensuse.org> - 2.2.2
- Upgrade with patches

* Thu Feb 23 2023 Hollow Man <hollowman@opensuse.org> - 2.2.1
- Upgrade

* Wed Feb 15 2023 Hollow Man <hollowman@opensuse.org> - 2.2.0
- New control statuses (https://github.com/kubescape/kubescape/pull/1016)

* Fri Feb 10 2023 Hollow Man <hollowman@opensuse.org> - 2.1.3
- Init kubescape package
