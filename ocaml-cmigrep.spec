%define ocaml_major 3.11
%define ocaml_minor 0

Name:           ocaml-cmigrep
Version:        1.5
Release:        %mkrel 1
Summary:        Search OCaml compiled interface (cmi) files

Group:          Development/Libraries
License:        GPLv2+
URL:            http://homepage.mac.com/letaris/
Source0:        http://homepage.mac.com/letaris/cmigrep-%{version}.tar.bz2
Source1:        http://caml.inria.fr/distrib/ocaml-%{ocaml_major}/ocaml-%{ocaml_major}.%{ocaml_minor}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

Patch0:         cmigrep-make-without-godi-debian.patch
Patch1:         ocaml-3.11.0-rpath.patch
Patch2:         ocaml-user-cflags.patch
Patch3:         ocaml-3.11.0-ppc64.patch

# Sent upstream on 2008-11-20.
Patch10:        ocaml-cmigrep-3.11.0-updated-types.patch

BuildRequires:  ocaml = %{ocaml_major}.%{ocaml_minor}
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-pcre-devel


%description
A utility to mine the data in Caml compiled interface (cmi) files, and
elisp that allows emacs to use cmigrep for completion.


%prep
%setup -q -n cmigrep-%{version}
%patch0 -p1

# Unpack OCaml sources into compiler/ subdirectory.
# XXX On Debian the compiled compiler libs are shipped in a
# +compiler-libs directory.  It would be good to copy this,
# however in Debian the only packages which actually use
# compiler-libs are camlp5 & cmigrep.
bzcat %{SOURCE1} | tar xf -
pushd ocaml-%{ocaml_major}.%{ocaml_minor}
%patch1 -p1
%patch2 -p1
%patch3 -p1
popd
mv ocaml-%{ocaml_major}.%{ocaml_minor} compiler

%patch10 -p1


%build
# Build the compiler libs.
pushd compiler
CFLAGS="$RPM_OPT_FLAGS" ./configure \
    -bindir %{_bindir} \
    -libdir %{_libdir}/ocaml \
    -x11lib %{_libdir} \
    -x11include %{_includedir} \
    -mandir %{_mandir}/man1
make world
make opt.opt
popd

# Build cmigrep itself.
make byte
make all

strip cmigrep


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 0755 cmigrep $RPM_BUILD_ROOT%{_bindir}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc GPL README cmigrep.el
%{_bindir}/cmigrep


