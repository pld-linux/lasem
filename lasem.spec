#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries

Summary:	Lasem - MathML and SVG rendering library
Summary(pl.UTF-8):	Lasem - biblioteka do renderowania MathML i SVG
Name:		lasem
Version:	0.4.3
Release:	2
License:	LGPL v2+
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/lasem/0.4/%{name}-%{version}.tar.xz
# Source0-md5:	a9637877bfce3f9bceecc742a52a7ee5
URL:		http://live.gnome.org/Lasem
BuildRequires:	bison
BuildRequires:	cairo-devel >= 1.2
BuildRequires:	flex
BuildRequires:	gdk-pixbuf2-devel >= 2.16
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gobject-introspection-devel >= 0.6.7
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	intltool >= 0.45.0
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	pango-devel >= 1:1.16.0
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	cairo >= 1.2
Requires:	gdk-pixbuf2 >= 2.16
Requires:	pango >= 1:1.16.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lasem aims to be a C/GObject based SVG/MathML renderer and editor,
supporting CSS style sheets (only rendering is implemented for now).
It uses cairo and pango as its rendering abstraction layer, and then
support numerous output formats: xlib, PNG, SVG, PDF, PS, EPS...

%description -l pl.UTF-8
Lasem ma być opartą na C/GObject biblioteką do renderowania i edycji
SVG/MathML z obsługą arkuszy stylów CSS (na razie zaimplementowane
jest tylko renderowanie). Wykorzystuje cairo i pango jako warstwę
abstrakcji przy renderowaniu, a następnie obsługuje wiele formatów
wyjściowych: xlib, PNG, SVG, PDF, PS, EPS...

%package devel
Summary:	Header files for lasem library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki lasem
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cairo-devel >= 1.2
Requires:	gdk-pixbuf2-devel >= 2.16
Requires:	glib2-devel >= 2.0
Requires:	libxml2-devel >= 2.0
Requires:	pango-devel >= 1:1.16.0

%description devel
Header files for lasem library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki lasem.

%package static
Summary:	Static lasem library
Summary(pl.UTF-8):	Statyczna biblioteka lasem
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static lasem library.

%description static -l pl.UTF-8
Statyczna biblioteka lasem.

%package apidocs
Summary:	lasem API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki lasem
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for lasem library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki lasem.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc/lasem-0.4

%find_lang %{name}-0.4

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}-0.4.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO
%attr(755,root,root) %{_bindir}/lasem-render-0.4
%attr(755,root,root) %{_libdir}/liblasem-0.4.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblasem-0.4.so.4
%{_libdir}/girepository-1.0/Lasem-0.4.typelib
%{_mandir}/man1/lasem-render-0.4.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblasem-0.4.so
%{_includedir}/lasem-0.4
%{_datadir}/gir-1.0/Lasem-0.4.gir
%{_pkgconfigdir}/lasem-0.4.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/liblasem-0.4.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/lasem-0.4
%endif
