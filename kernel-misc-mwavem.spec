#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
#
%define		_orig_name	mwavem
%define		_rel		0.1

Summary:	Kernel module - ACP Modem driver
Summary(pl.UTF-8):	Moduł jądra - sterownik do modemu ACP
Name:		kernel-misc-%{_orig_name}
Version:	1.0.4
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	ftp://www-126.ibm.com/pub/acpmodem/%{version}/%{_orig_name}-%{version}.tar.gz
# Source0-md5:	22cd78ade480db8ab5f0d1ca4dee07ec
URL:		http://oss.software.ibm.com/acpmodem/
BuildRequires:	%{kgcc_package}
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_dist_kernel:BuildRequires:	kernel-headers}
BuildRequires:	rpmbuild(macros) >= 1.118
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Provides:	kernel-mwavem-%{_rel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
%{_orig_name} - ACP Modem driver for Linux.

%description -l pl.UTF-8
%{_orig_name} - sterownik do modemu ACP dla Linuksa.

%package -n kernel-smp-misc-%{_orig_name}
Summary:	Kernel SMP module - ACP Modem driver
Summary(pl.UTF-8):	Moduł jądra SMP - sterownik do modemu ACP
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Provides:	kernel-mwavem-%{_rel}

%description -n kernel-smp-misc-%{_orig_name}
%{_orig_name} - ACP Modem driver for Linux SMP.

%description -n kernel-smp-misc-%{_orig_name} -l pl.UTF-8
%{_orig_name} - sterownik do modemu ACP dla Linuksa SMP.

%package -n %{_orig_name}
Summary:	mwavem - utils
Summary(pl.UTF-8):	mwavem - marzędzia
Release:	%{_rel}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires:	kernel-mwavem = %{_rel}

%description -n %{_orig_name}
%{_orig_name} - ACP Modem utils.

%description -n %{_orig_name} -l pl.UTF-8
%{_orig_name} - narzędzia do modemu ACP.

%prep
%setup -q -n %{_orig_name}-%{version}

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure

%{__make}

cd src/drivers

%{__make} \
	CC="%{kgcc} -D__SMP__"

mv -f mwavedd.o mwavedd.o.smp.o

%{__make} \
	CC="%{kgcc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp src/drivers/mwavedd.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
cp src/drivers/mwavedd.o.smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/%{_orig_name}.o

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post	-n kernel-smp-misc-%{_orig_name}
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-misc-%{_orig_name}
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*

%files -n kernel-smp-misc-%{_orig_name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/*

%files -n %{_orig_name}
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog FAQ README README.devfs doc/mwave.txt
%config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(755,root,root) %{_bindir}/%{_orig_name}
%{_datadir}/%{_orig_name}
