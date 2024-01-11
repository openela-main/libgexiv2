%if 0%{?rhel} > 7
# Disable python2 build by default
%bcond_with python2
%else
%bcond_without python2
%endif

Name:           libgexiv2
Version:        0.10.8
Release:        4%{?dist}
Summary:        Gexiv2 is a GObject-based wrapper around the Exiv2 library

License:        GPLv2+
URL:            https://wiki.gnome.org/Projects/gexiv2
Source0:        https://download.gnome.org/sources/gexiv2/0.10/gexiv2-%{version}.tar.xz

Patch0:         libgexiv2-build-against-exiv-027.patch

BuildRequires:  exiv2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  libtool
%if %{with python2}
BuildRequires:  python2-devel
BuildRequires:  python2-gobject-base
%endif # with python2
BuildRequires:  vala
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires:  python3-devel
BuildRequires:  python3-gobject-base
%endif

%description
libgexiv2 is a GObject-based wrapper around the Exiv2 library. 
It makes the basic features of Exiv2 available to GNOME applications.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%if %{with python2}
%package -n     python2-gexiv2
Summary:        Python2 bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python-gobject-base%{?_isa}
# For upgrade path from F24
Provides:       libgexiv2-python2 = %{name}-%{version}
Obsoletes:      libgexiv2-python2 < 0.10.4

%description -n python2-gexiv2
This package contains the python2 bindings for %{name}
%endif # with python2

%if 0%{?fedora} || 0%{?rhel} > 7
%package -n     python3-gexiv2
Summary:        Python3 bindings for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python3-gobject-base%{?_isa}
# For upgrade path from F24
Provides:       libgexiv2-python3 = %{name}-%{version}
Obsoletes:      libgexiv2-python3 < 0.10.4

%description -n python3-gexiv2
This package contains the python3 bindings for %{name}
%endif

%prep
%setup -q -n gexiv2-%{version}

%patch0 -p1 -b .build-against-exiv-027

%build
%configure --enable-introspection --enable-static=no --enable-shared=yes
%make_build

%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%check
make check

%ldconfig_scriptlets

%files
%license COPYING
%doc AUTHORS THANKS README
%{_libdir}/libgexiv2.so.2*
%{_libdir}/girepository-1.0/GExiv2-0.10.typelib

%files devel
%{_includedir}/gexiv2/
%{_datadir}/gir-1.0/GExiv2-0.10.gir
%{_libdir}/libgexiv2.so
%{_libdir}/pkgconfig/gexiv2.pc
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/gexiv2/
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/gexiv2.vapi

%if %{with python2}
%files -n python2-gexiv2
%{python2_sitearch}/gi/overrides/GExiv2.py*
%endif # with python2

%if 0%{?fedora} || 0%{?rhel} > 7
%files -n python3-gexiv2
%{python3_sitearch}/gi/overrides/GExiv2.py
%{python3_sitearch}/gi/overrides/__pycache__/GExiv2*
%endif

%changelog
* Tue Oct 29 2019 Tomas Pelka <tpelka@redhat.com> - 0.10.8-4
- Rebuild again to correctly trigger side-tag gating (exiv2)
  Resolves: bz#1757444

* Tue Oct 15 2019 Jan Grulich <jgrulich@redhat.com> - 0.10.8-3
- Rebuild (exiv2)
  Resolves: bz#1757444

* Thu Jun 07 2018 Charalampos Stratakis <cstratak@redhat.com> - 0.10.8-2
- Conditionalize the python2 subpackage

* Tue Feb 06 2018 Kalev Lember <klember@redhat.com> - 0.10.8-1
- Update to 0.10.8

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.10.7-2
- Switch to %%ldconfig_scriptlets

* Sat Dec 30 2017 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.10.7-1
- Update to latest upstream release

* Thu Dec 07 2017 Merlin Mathesius <mmathesi@redhat.com> - 0.10.6-4
- Cleanup spec file conditionals

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat May 13 2017 Kalev Lember <klember@redhat.com> - 0.10.6-1
- Update to 0.10.6

* Tue May 02 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.10.5-3
- Rebuild against new exiv2 soname

* Thu Apr 27 2017 Debarshi Ray <rishi@fedoraproject.org> - 0.10.5-2
- Add Provides to retain compatibility

* Tue Mar 21 2017 Kalev Lember <klember@redhat.com> - 0.10.5-1
- Update to 0.10.5
- Build API documentation
- Update source URL
- Enable the test suite

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.10.4-3
- Rebuild for Python 3.6

* Thu Sep 22 2016 Kalev Lember <klember@redhat.com> - 0.10.4-2
- BR vala instead of obsolete vala-tools subpackage

* Mon Aug 15 2016 Kalev Lember <klember@redhat.com> - 0.10.4-1
- Update to 0.10.4
- Use license macro for COPYING
- Rename python2 and python3 subpackages are per latest guidelines
- Use make_install and make_build macros
- Tighten soname glob

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.3-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.3-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Jun 24 2015 Rex Dieter <rdieter@fedoraproject.org> - 0.10.3-4
- rebuild (exiv2)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 28 2015 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.10.3-2
- Rebuild for gcc5 again.

* Tue Mar 24 2015 Kalev Lember <kalevlember@gmail.com> - 0.10.3-1
- Update to 0.10.3

* Fri Mar 20 2015 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.10.2-2
- Rebuild since exiv was rebuild for gcc5 and that seems to have broken things

* Wed Sep 17 2014 Kalev Lember <kalevlember@gmail.com> - 0.10.2-1
- Update to 0.10.2
- Tighten deps with the _isa macro
- Co-own the vala vapi directories in -devel

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.10.1-4
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue Apr 29 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.10.1-1
- Update to latest upstream release
- Contains bugfix for https://bugzilla.gnome.org/show_bug.cgi?id=728909

* Tue Mar 18 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.10.0-1
- Update to latest release

* Thu Feb 06 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.9.1-1
- Update to new release with fixes
- Do not use tests yet, cant get them to run properly

* Wed Feb 05 2014 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.9.0-1
- Update to latest unstable release

* Tue Dec 03 2013 Rex Dieter <rdieter@fedoraproject.org> 0.7.0-2
- rebuild (exiv2)

* Tue Oct 08 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.7.0-1
- Update to latest upstream release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun May 19 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.6.1-1
- Update to 0.6.1

* Tue May 14 2013 Matthias Clasen <mclasen@redhat.com> 0.5.0-8
- .gir files belong in the devel package

* Wed May 08 2013 Richard Hughes <richard@hughsie.com> 0.5.0-7
- RHEL7 does not have python3

* Wed Mar 20 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.5.0-6
- Fix requires

* Wed Mar 20 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.5.0-5
- Fix python bindings generation
- Add new subpackages for python2,3 bindings

* Tue Mar 19 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.5.0-4
- Add patch to remove overlinking rhbz#818587

* Mon Mar 11 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.5.0-3
- Enable introspection for py support
- add new files for introspection

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 06 2013 Ankur Sinha <ankursinha AT fedoraproject DOT org> 0.5.0-1
- Update to 0.5.0
- rhbz#890402

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 02 2012 Rex Dieter <rdieter@fedoraproject.org> - 0.4.1-2
- rebuild (exiv2)

* Tue Apr 03 2012 Kalev Lember <kalevlember@gmail.com> - 0.4.1-1
- Update to 0.4.1

* Thu Feb 23 2012 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.3.91-1
- Update to 0.3.91
- rhbz #796278
- remove patches

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 14 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.2.2-3
- rebuild (exiv2)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 01 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.2.2-1
- 0.2.2
- exiv2-0.21 patch

* Tue Aug 24 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.2.0-1
- update to latest upstream release

* Sun Aug 08 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.1.90-1
- update to latest upstream release

* Tue Jul 13 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.1.0-1
- update to latest upstream release

* Mon Jun 14 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.0.91-2
- changed file section so package owns the directory containing headers too

* Fri Jun 11 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.0.91-1
- updated to latest release
- removed patch - it was included in this release

* Sat Jun 05 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.0.90-5
- changed configure macro as per bug report comment

* Sat Jun 05 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.0.90-4
- changed configure portion
- added Requires:  vala for devel
- made the file section more precise
- bugzilla #599097 
- changed patch to include a default LIB setting

* Fri Jun 04 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.0.90-3
- patched makefile

* Thu Jun 03 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.0.90-2
- some fixes in spec
- moved *.vapi to devel
- removed INSTALL from doc
- added comment to yorba ticket link
- corrected typo in description

* Wed Jun 02 2010 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.0.90-1
- initial rpmbuild
