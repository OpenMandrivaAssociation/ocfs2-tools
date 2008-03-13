%define _requires_exceptions pkgconfig(com_err) 

Summary:	Tools for managing the Oracle Cluster Filesystem 2
Name:		ocfs2-tools
Version:	1.2.3
Release:	%mkrel 3
License:	GPL
Group:		System/Base
URL:		http://oss.oracle.com/projects/ocfs2-tools/
Source0:	http://oss.oracle.com/projects/ocfs2-tools/dist/files/source/v1.2/%{name}-%{version}.tar.gz
BuildRequires:	e2fsprogs-devel
BuildRequires:	glib2-devel >= 2.2.3
BuildRequires:	glibc-static-devel
BuildRequires:	pygtk2.0 >= 1.99.16
BuildRequires:	python-devel
BuildRequires:	pkgconfig
BuildRequires:	libreadline-devel
BuildRequires:	ncurses-devel
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
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ocfs2/cluster.conf
%attr(0755,root,root) /sbin/debugfs.ocfs2
%attr(0755,root,root) /sbin/fsck.ocfs2
%attr(0755,root,root) /sbin/mkfs.ocfs2
%attr(0755,root,root) /sbin/mount.ocfs2
%attr(0755,root,root) /sbin/mounted.ocfs2
%attr(0755,root,root) /sbin/o2cb_ctl
%attr(0755,root,root) /sbin/ocfs2_hb_ctl
%attr(0755,root,root) /sbin/ocfs2cdsl
%attr(0755,root,root) /sbin/tunefs.ocfs2
%attr(0755,root,root) %{_sbindir}/compute_groups
%attr(0755,root,root) %{_sbindir}/decode_lockres
%attr(0755,root,root) %{_sbindir}/encode_lockres
%attr(0755,root,root) %{_sbindir}/find_allocation_fragments
%attr(0755,root,root) %{_sbindir}/find_dup_extents
%attr(0755,root,root) %{_sbindir}/find_hardlinks
%attr(0755,root,root) %{_sbindir}/find_inode_paths
%attr(0755,root,root) %{_sbindir}/mark_journal_dirty
%attr(0755,root,root) %{_sbindir}/set_random_bits
%attr(0644,root,root) %{_mandir}/man8/debugfs.ocfs2.8*
%attr(0644,root,root) %{_mandir}/man8/fsck.ocfs2.8*
%attr(0644,root,root) %{_mandir}/man8/fsck.ocfs2.checks.8*
%attr(0644,root,root) %{_mandir}/man8/mkfs.ocfs2.8*
%attr(0644,root,root) %{_mandir}/man8/mounted.ocfs2.8*
%attr(0644,root,root) %{_mandir}/man8/o2cb_ctl.8*
%attr(0644,root,root) %{_mandir}/man8/ocfs2_hb_ctl.8*
%attr(0644,root,root) %{_mandir}/man8/ocfs2cdsl.8*
%attr(0644,root,root) %{_mandir}/man8/tunefs.ocfs2.8*
%attr(0644,root,root) %{_mandir}/man8/mount.ocfs2.8*

%files -n ocfs2console
%defattr(-,root,root)
%{py_libdir}/site-packages/ocfs2interface
%attr(0755,root,root) %{_sbindir}/ocfs2console
%attr(0644,root,root) %{_mandir}/man8/ocfs2console.8*

%files devel
%defattr(-,root,root)
%{_includedir}/o2cb
%{_includedir}/o2dlm
%{_includedir}/ocfs2
%{_libdir}/pkgconfig/o2cb.pc
%{_libdir}/pkgconfig/o2dlm.pc
%{_libdir}/pkgconfig/ocfs2.pc

%files static-devel
%defattr(-,root,root)
%{_libdir}/libo2cb.a
%{_libdir}/libo2dlm.a
%{_libdir}/libocfs2.a



