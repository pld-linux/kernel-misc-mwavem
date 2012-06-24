# bcond
# _without_dist_kernel          without distribution kernel

%define		_orig_name	mwavem
%define		_rel		0.1

Summary:	Kernel module - ACP Modem driver
Summary(pl):	Modu� j�dra - sterownik ACP Modem
Name:		kernel-misc-%{_orig_name}
Version:	1.0.4
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	ftp://www-126.ibm.com/pub/acpmodem/%{version}/%{_orig_name}-%{version}.tar.gz
URL:		http://oss.software.ibm.com/acpmodem/
%{!?_without_dist_kernel:BuildRequires:         kernel-headers}
BuildRequires:	%{kgcc_package}
Prereq:		/sbin/depmod
Provides:	kernel-mwavem-%{_rel}
%{!?_without_dist_kernel:%requires_releq_kernel_up}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
%{_orig_name} - ACP Modem driver

%description -l pl
%{_orig_name} - sterownik ACP Modem

%package -n kernel-smp-misc-%{_orig_name}
Summary:	Kernel modules for transparent dumping of specified processes
Summary(pl):	Modu�y j�dra pozwalaj�ce na zrzucanie proces�w do pliku
Release:	%{_rel}@%{_kernel_ver_str}
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Group:		Base/Kernel
Prereq:		/sbin/depmod
Provides:	kernel-mwavem-%{_rel}

%description -n kernel-smp-misc-%{_orig_name}
%{_orig_name} - ACP Modem driver

%description -n kernel-smp-misc-%{_orig_name} -l pl
%{_orig_name} - sterownik ACP Modem

%package -n %{_orig_name}
Summary:	mwavem - utils
Summary(pl):	mwavem - marzedzia
Release:	%{_rel}
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Group:		Base/Kernel
Requires:	kernel-mwavem = %{_rel}

%description -n %{_orig_name}
%{_orig_name} - ACP Modem utils

%description -n %{_orig_name} -l pl
%{_orig_name} - ACP Modem narz�dzia


%prep
%setup -q -n %{_orig_name}-%{version}

%build
%{__aclocal}
%{__autoconf}
%{__automake}

%configure

%{__make}

cd src/drivers

%{__make} CC="%{kgcc} -D__SMP__"

mv -f mwavedd.o mwavedd.o.smp.o

%{__make} CC="%{kgcc}"


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc


%{__make} DESTDIR=$RPM_BUILD_ROOT install
cp src/drivers/mwavedd.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
cp src/drivers/mwavedd.o.smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/%{_orig_name}.o


%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/depmod -a

%postun
/sbin/depmod -a

%post -n kernel-smp-misc-%{_orig_name}
/sbin/depmod -a

%postun -n kernel-smp-misc-%{_orig_name}
/sbin/depmod -a

%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*

%files -n kernel-smp-misc-%{_orig_name}
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/*

%files -n %{_orig_name}
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog FAQ README README.devfs doc/mwave.txt
%config(noreplace,missingok) %verify(not size mtime md5) %{_sysconfdir}/*
%attr(755,root,root) %{_bindir}/%{_orig_name}
%{_datadir}/%{_orig_name}/*
