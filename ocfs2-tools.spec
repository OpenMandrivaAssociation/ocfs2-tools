%if %{_use_internal_dependency_generator}
%define __noautoreq 'pkgconfig(com_err)'
%else
%define _requires_exceptions pkgconfig(com_err) 
%endif

Summary:	Tools for managing the Oracle Cluster Filesystem 2
Name:		ocfs2-tools
Version:	1.6.4
Release:	2
License:	GPL
Group:		System/Base
URL:		http://oss.oracle.com/projects/ocfs2-tools/
Source0:	http://oss.oracle.com/projects/ocfs2-tools/dist/files/source/v1.2/%{name}-%{version}.tar.gz
Patch1:     ocfs2-tools-1.6.4-fix-format-errors.patch
Patch2:     ocfs2-tools-1.4.4-fix-linking.patch
Patch3:     ocfs2-tools-gcc45.patch
BuildRequires:	libblkid-devel
BuildRequires:	glib2-devel >= 2.2.3
BuildRequires:	glibc-static-devel
BuildRequires:	pygtk2.0 >= 1.99.16
BuildRequires:	python-devel
BuildRequires:	pkgconfig
BuildRequires:	libreadline-devel
BuildRequires:	ncurses-devel
BuildRequires:	ext2fs-devel
BuildRequires:	dlm-devel
BuildRequires:	openais-devel
Requires:	kernel >= 2.6.16.1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Tools to manage Oracle Cluster Filesystem 2 volumes.

%package -n	ocfs2console
Summary:	GUI frontend for OCFS2 management
Group:		System/Base
Requires:	e2fsprogs
Requires:	glib2 >= 2.2.3
Requires:	vte >= 0.11.10
Requires:	pygtk2.0 >= 1.99.16
Requires:	%{name} = %{version}

%description -n	ocfs2console
GUI frontend for management and debugging of Oracle Cluster Filesystem 2
volumes.

%package	devel
Summary:	Development for ocfs2-tools
Group:		Development/C
Requires:	%{name} = %{version}

%description devel
This package contains development files for ocfs2-tools.

%package	static-devel
Summary:	Static libraries for ocfs2-tools
Group:		Development/C
Requires:	%{name}-devel = %{version}

%description static-devel
This package contains static libraries used for ocfs2-tools development.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p 1
%patch2 -p 1
#patch3 -p 1

%build

%configure2_5x

# lib64 fix
perl -pi -e "s|^pyexecdir.*|pyexecdir = %{py_libdir}/site-packages|g" Config.make

make

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%makeinstall_std

# install sample config
install -d %{buildroot}%{_sysconfdir}/ocfs2
install -m0644 documentation/samples/cluster.conf %{buildroot}%{_sysconfdir}/ocfs2/cluster.conf

# install extras
install -d %{buildroot}%{_sbindir}
install -m0755 extras/compute_groups %{buildroot}%{_sbindir}/
install -m0755 extras/decode_lockres %{buildroot}%{_sbindir}/
install -m0755 extras/encode_lockres %{buildroot}%{_sbindir}/
install -m0755 extras/find_allocation_fragments %{buildroot}%{_sbindir}/
install -m0755 extras/find_dup_extents %{buildroot}%{_sbindir}/
install -m0755 extras/find_hardlinks %{buildroot}%{_sbindir}/
install -m0755 extras/find_inode_paths %{buildroot}%{_sbindir}/
install -m0755 extras/mark_journal_dirty %{buildroot}%{_sbindir}/
install -m0755 extras/set_random_bits %{buildroot}%{_sbindir}/

# install python stuff
%{__python} -c "import compileall; compileall.compile_dir('%{buildroot}%{py_libdir}/site-packages/ocfs2interface', ddir='%{py_libdir}/site-packages/ocfs2interface')"

# install init system
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 0755 vendor/common/o2cb.init %{buildroot}%{_initrddir}/o2cb
install -m 0755 vendor/common/ocfs2.init %{buildroot}%{_initrddir}/ocfs2
install -m 0644 vendor/common/o2cb.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/o2cb

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README* COPYING CREDITS MAINTAINERS
%doc documentation/samples/cluster.conf documentation/*.txt
%config(noreplace) %{_sysconfdir}/sysconfig/o2cb
%{_initrddir}/o2cb
%{_initrddir}/ocfs2
%config(noreplace) %{_sysconfdir}/ocfs2/cluster.conf
/sbin/debugfs.ocfs2
/sbin/fsck.ocfs2
/sbin/mkfs.ocfs2
/sbin/mount.ocfs2
/sbin/mounted.ocfs2
/sbin/o2cb_ctl
/sbin/ocfs2_hb_ctl
/sbin/tunefs.ocfs2
/sbin/o2image
%{_sbindir}/compute_groups
%{_sbindir}/decode_lockres
%{_sbindir}/encode_lockres
%{_sbindir}/find_allocation_fragments
%{_sbindir}/find_dup_extents
%{_sbindir}/find_hardlinks
%{_sbindir}/find_inode_paths
%{_sbindir}/mark_journal_dirty
%{_sbindir}/set_random_bits
%{_sbindir}/o2hbmonitor
%{_bindir}/o2info
%{_mandir}/man1/o2info.1.*
%{_mandir}/man7/o2cb.7.*
%{_mandir}/man8/o2image.8.*
%{_mandir}/man8/debugfs.ocfs2.8*
%{_mandir}/man8/fsck.ocfs2.8*
%{_mandir}/man8/fsck.ocfs2.checks.8*
%{_mandir}/man8/mkfs.ocfs2.8*
%{_mandir}/man8/mounted.ocfs2.8*
%{_mandir}/man8/o2cb_ctl.8*
%{_mandir}/man8/ocfs2_hb_ctl.8*
%{_mandir}/man8/tunefs.ocfs2.8*
%{_mandir}/man8/mount.ocfs2.8*

%files -n ocfs2console
%defattr(-,root,root)
%{py_libdir}/site-packages/ocfs2interface
%{_sbindir}/ocfs2console
%{_mandir}/man8/ocfs2console.8*

%files devel
%defattr(-,root,root)
%{_includedir}/o2cb
%{_includedir}/o2dlm
%{_includedir}/ocfs2
%{_includedir}/ocfs2-kernel
%{_libdir}/pkgconfig/o2cb.pc
%{_libdir}/pkgconfig/o2dlm.pc
%{_libdir}/pkgconfig/ocfs2.pc

%files static-devel
%defattr(-,root,root)
%{_libdir}/libo2cb.a
%{_libdir}/libo2dlm.a
%{_libdir}/libocfs2.a





%changelog
* Sat Aug 06 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1.6.4-1mdv2012.0
+ Revision: 693395
- 1.6.4
  P1 rediffed
  P3 merged upstream

* Fri Nov 19 2010 Funda Wang <fwang@mandriva.org> 1.4.4-1mdv2011.0
+ Revision: 598882
- BR ext2fs
- new version 1.4.4

* Tue Jun 09 2009 Frederic Crozat <fcrozat@mandriva.com> 1.4.1-2mdv2010.0
+ Revision: 384378
- Switch to libblkid-devel

* Sun Mar 08 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1.4.1-1mdv2009.1
+ Revision: 352906
- new version
- fix format errors
- fix missing header
- fix some linking errors
- disable -Wl,--no-undefined for modules

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Thu Mar 13 2008 Andreas Hasenack <andreas@mandriva.com> 1.2.3-3mdv2008.1
+ Revision: 187679
- tarball for 1.2.6 was never uploaded: back to 1.2.3
- rebuild for 2008.1

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Erwan Velu <erwan@mandriva.org>
    - 1.2.6


* Wed Mar 21 2007 Oden Eriksson <oeriksson@mandriva.com> 1.2.3-2mdv2007.1
+ Revision: 147244
- fix deps

* Mon Mar 05 2007 Andreas Hasenack <andreas@mandriva.com> 1.2.3-1mdv2007.1
+ Revision: 133014
- updated to version 1.2.3

* Tue Oct 24 2006 Andreas Hasenack <andreas@mandriva.com> 1.2.2-1mdv2007.1
+ Revision: 71960
- updated to version 1.2.2
- added new devel packages
- Import ocfs2-tools

* Fri Sep 22 2006 Andreas Hasenack <andreas@mandriva.com> 1.2.1-2mdv2007.0
- added buildrequires for ncurses-devel

* Thu Sep 21 2006 Andreas Hasenack <andreas@mandriva.com> 1.2.1-1mdv2007.0
- updated to version 1.2.1
- added missing initscripts and a sysconfig file
- added glibc-static-devel to buildrequires

* Sun Apr 02 2006 Oden Eriksson <oeriksson@mandriva.com> 1.2.0-2mdk
- forgot to add the config file, oops!

* Sun Apr 02 2006 Oden Eriksson <oeriksson@mandriva.com> 1.2.0-1mdk
- initial Mandriva package
- used parts of the provided spec file

