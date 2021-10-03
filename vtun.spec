#
# Conditional build:
%bcond_without	ssl	# build without encryption ability
#
Summary:	Virtual tunnel over TCP/IP networks
Summary(pl.UTF-8):	Wirtualne tunele poprzez sieci TCP/IP
Name:		vtun
Version:	3.0.4
Release:	3
Epoch:		2
License:	GPL v2+
Group:		Networking/Daemons
Source0:	http://download.sourceforge.net/vtun/%{name}-%{version}.tar.gz
# Source0-md5:	f952c5895ae8f40235aaad9a8f41a4bd
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.service
Source4:	%{name}.sh
Patch1:		%{name}-autoheader.patch
Patch2:		%{name}-sslauth.patch
Patch3:		%{name}-linking.patch
Patch4:		%{name}-openssl-1.1.patch
Patch5:		%{name}-dont-inline.patch
Patch6:		no-strip.patch
URL:		http://vtun.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	lzo-devel >= 2.0.1
%{?with_ssl:BuildRequires:	openssl-devel >= 0.9.7d}
BuildRequires:	rpmbuild(macros) >= 1.671
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Requires:	systemd-units >= 206-6
Obsoletes:	vppp
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_localstatedir	/var

%description
VTun provides the method for creating Virtual Tunnels over TCP/IP
networks and allows to shape, compress, encrypt traffic in that
tunnels. Supported type of tunnels are: PPP, IP, Ethernet and most of
other serial protocols and programs. VTun is easily and highly
configurable, it can be used for various network task like VPN, Mobil
IP, Shaped Internet access, IP address saving, etc. It is completely
user space implementation and does not require modification to any
kernel parts. You need SSLeay-devel and lzo-devel to build it.

%description -l pl.UTF-8
VTun umożliwia tworzenie tuneli poprzez sieci TCP/IP wraz z
przydzielaniem pasma, kompresją, szyfrowaniem danych w tunelach.
Wspierane typy tuneli to: PPP, IP, Ethernet i większość pozostałych
protokołów szeregowych. VTun jest łatwy i elastyczny w konfiguracji.
Może zostać wykorzystany do takich sieciowych zastosowań jak VPN,
Mobil IP, łącza o określonym paśmie oraz innych. Działa w warstwie
user space, więc nie wymaga dodatkowego wsparcia w jądrze.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
cp -f /usr/share/automake/config.* .
# aclocal.m4 is only local, don't try to rebuild
#%{__autoheader}
%{__autoconf}
%configure \
	%{?with_ssl:--with-crypto-headers=%{_includedir}/openssl} \
	%{!?with_ssl:--disable-ssl} \
	--enable-lzo
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT{/etc/{sysconfig,rc.d/init.d},%{_localstatedir}/log/vtun} \
	$RPM_BUILD_ROOT{/lib/systemd/pld-helpers.d,%{systemdunitdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL_OWNER=""

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/vtund
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/vtun
install %{SOURCE3} $RPM_BUILD_ROOT%{systemdunitdir}/vtund.service
install %{SOURCE4} $RPM_BUILD_ROOT/lib/systemd/pld-helpers.d/vtund.sh
touch $RPM_BUILD_ROOT%{_sysconfdir}/vtund.conf
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/vtun.8
echo ".so vtund.8" > $RPM_BUILD_ROOT%{_mandir}/man8/vtun.8

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add vtund
%service vtund restart "vtun daemons"
%systemd_post vtund.service

%preun
if [ "$1" = "0" ]; then
	%service vtund stop
	/sbin/chkconfig --del vtund
fi
%systemd_preun vtund.service

%postun
%systemd_reload

%triggerpostun -- %{name} < 2:3.0.3-1
%systemd_trigger vtund.service

%files
%defattr(644,root,root,755)
%doc ChangeLog Credits README README.Setup README.Shaper FAQ TODO vtund.conf
%attr(754,root,root) /etc/rc.d/init.d/vtund
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/vtun
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/vtund.conf
%{systemdunitdir}/vtund.service
%attr(755,root,root) /lib/systemd/pld-helpers.d/vtund.sh
%attr(755,root,root) %{_sbindir}/vtund
%attr(755,root,root) %dir /var/log/vtund
%{_mandir}/man5/vtund.conf.5*
%{_mandir}/man8/vtun.8*
%{_mandir}/man8/vtund.8*
