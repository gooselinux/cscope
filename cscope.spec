Summary: C source code tree search and browse tool 
Name: cscope
Version: 15.6
Release: 6%{?dist}
Source0: http://downloads.sourceforge.net/project/cscope/cscope/15.6/cscope-15.6.tar.gz
URL: http://cscope.sourceforge.net
License: BSD 
Group: Development/Tools 
BuildRoot: %{_tmppath}/%{name}-%{version}
BuildRequires: pkgconfig ncurses-devel flex bison m4

%define cscope_share_path %{_datadir}/cscope
%define xemacs_lisp_path %{_datadir}/xemacs/site-packages/lisp
%define emacs_lisp_path %{_datadir}/emacs/site-lisp

Patch0:cscope-15.6-findassign.patch
Patch1:cscope-15.6-ocs.patch
Patch2:cscope-15.6-xcscope-man.patch
Patch3:cscope-15.6-sigwinch-linemode.patch
Patch4:cscope-15.6-qrebuild.patch
Patch5:cscope-15.6-incdir-overflow.patch

%description
cscope is a mature, ncurses based, C source code tree browsing tool.  It 
allows users to search large source code bases for variables, functions,
macros, etc, as well as perform general regex and plain text searches.  
Results are returned in lists, from which the user can select individual 
matches for use in file editing.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT %{name}-%{version}.files
make DESTDIR=$RPM_BUILD_ROOT install 
mkdir -p $RPM_BUILD_ROOT/var/lib/cs
mkdir -p $RPM_BUILD_ROOT%{cscope_share_path}
cp -a contrib/xcscope/xcscope.el $RPM_BUILD_ROOT%{cscope_share_path}
cp -a contrib/xcscope/cscope-indexer $RPM_BUILD_ROOT%{_bindir}
for dir in %{xemacs_lisp_path} %{emacs_lisp_path} ; do
  mkdir -p $RPM_BUILD_ROOT$dir
  ln -s %{cscope_share_path}/xcscope.el $RPM_BUILD_ROOT$dir
  touch $RPM_BUILD_ROOT$dir/xcscope.elc
  echo "%ghost $dir/xcscope.el*" >> %{name}-%{version}.files
done


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}-%{version}.files
%defattr(-,root,root,-)
%{_bindir}/*
%dir %{cscope_share_path}
%{cscope_share_path}/xcscope.el
%{_mandir}/man1/*
%dir /var/lib/cs
%doc AUTHORS COPYING ChangeLog README TODO

%triggerin -- xemacs
ln -sf %{cscope_share_path}/xcscope.el %{xemacs_lisp_path}/xcscope.el

%triggerin -- emacs
ln -sf %{cscope_share_path}/xcscope.el %{emacs_lisp_path}/xcscope.el

%triggerun -- xemacs
[ $2 -gt 0 ] && exit 0
rm -f %{xemacs_lisp_path}/xcscope.el

%triggerun -- emacs
[ $2 -gt 0 ] && exit 0
rm -f %{emacs_lisp_path}/xcscope.el

%changelog
* Mon Nov 30 2009 Neil Horman <nhorman@redhat.com> - 15.6-6
- Update Source0 url for package wrangler

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Neil Horman <nhorman@redhat.com>
- Fix some buffer overflows (bz 505605)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 08 2008 Neil Horman <nhorman@redhat.com> -15.6-2.dist
- Grab upstream patch for -q rebuld (bz 436648)

* Fri Mar 25 2007 Neil Horman <nhorman@redhat.com> -15.6-1.dist
- Rebase to version 15.6

* Mon Mar 05 2007 Neil Horman <nhorman@redhat.com> -15.5-15.4.dist
- Make sigwinch handler only register for curses mode (bz 230862)

* Mon Feb 05 2007 Neil Horman <nhorman@redhat.com> -15.5-15.3.dist
- Fixing dist label in release tag.

* Thu Feb 01 2007 Neil Horman <nhorman@redhat.com> -15.5-15.2.dist
- Fixing changelog to not have macro in release

* Wed Aug 23 2006 Neil Horman <nhorman@redhat.com> -15.5-15.1
- fixed overflows per bz 203651
- start using {dist} tag to make release numbering easier

* Mon Jul 17 2006 Jesse Keating <jkeating@redhat.com> - 15.5-14
- rebuild

* Fri Jun 23 2006 Neil Horman <nhorman@redhat.com>
- Fix putstring overflow (bz 189666)

* Fri Jun 23 2006 Neil Horman <nhorman@redhat.com>
- Fix putstring overflow (bz 189666)

* Fri May 5  2006 Neil Horman <nhorman@redhat.com>
- Adding fix to put SYSDIR in right location (bz190580)

* Fri Apr 21 2006 Neil Horman <nhorman@redhat.com> - 15.5-13.4
- adding inverted index overflow patch

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 15.5-13.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 15.5-13.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuild on new gcc

* Tue Nov 30 2004 Neil Horman <nhorman@redhat.com>
- added tempsec patch to fix bz140764/140765

* Mon Nov 29 2004 Neil Horman <nhorman@redhat.com>
- updated cscope resize patch to do less work in
  signal handler and synced version nr. on dist.

* Mon Nov 22 2004 Neil Horman <nhorman@redhat.com>
- added cscope-1.5.-resize patch to allow terminal
  resizing while cscope is running

* Tue Oct 5  2004 Neil Horman <nhorman@redhat.com>
- modified cscope-15.5.-inverted patch to be upstream
  friendly

* Tue Sep 28 2004 Neil Horman <nhorman@redhat.com>
- fixed inverted index bug (bz 133942)
 
* Mon Sep 13 2004 Frank Ch. Eigler <fche@redhat.com>
- bumped release number to a plain "1"

* Fri Jul 16 2004 Neil Horman <nhorman@redhat.com>
- Added cscope-indexer helper and xcscope lisp addon
- Added man page for xcscope
- Added triggers to add xcscope.el pkg to (x)emacs
- Thanks to Ville, Michael and Jens for thier help :)

* Fri Jul 2 2004 Neil Horman <nhorman@redhat.com>
- Added upstream ocs fix
- Added feature to find symbol assignments
- Changed default SYSDIR directory to /var/lib/cs
- Incoproated M. Schwendt's fix for ocs -s 

* Fri Jun 18 2004 Neil Horman <nhorman@redhat.com>
- built the package
