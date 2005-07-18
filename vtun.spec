#
# Conditional build:
%bcond_without	ssl	# build without encryption ability
#
Summary:	Virtual tunnel over TCP/IP networks
Summary(pl):	Wirtualne tunele poprzez sieci TCP/IP
Name:		vtun
Version:	2.6
Release:	2
Epoch:		2
License:	GPL
Group:		Networking/Daemons
Vendor:		Maxim Krasnyansky <max_mk@yahoo.com>
# Source0-md5:	309534fd03c5d13a19c43916f61f4bbf
Source0:	http://dl.sourceforge.net/vtun/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-expect.patch
Patch2:		%{name}-autoheader.patch
Patch3:		%{name}-getpt.patch
Patch4:		%{name}-sslauth.patch
Patch5:		%{name}-ac.patch
Patch6:		%{name}-lzo2.patch
URL:		http://vtun.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	lzo-devel >= 2.0.1
%{?with_ssl:BuildRequires:	openssl-devel >= 0.9.7d}
BuildRequires:	zlib-devel
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
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

%description -l pl
VTun umo¿liwia tworzenie tuneli poprzez sieci TCP/IP wraz
z przydzielaniem pasma, kompresj±, szyfrowaniem danych w tunelach.
Wspierane typy tuneli to: PPP, IP, Ethernet i wiêkszo¶æ pozosta³ych
protoko³ów szeregowych. VTun jest ³atwy i elastyczny w konfiguracji.
Mo¿e zostaæ wykorzystany do takich sieciowych zastosowañ jak VPN, 
Mobil IP, ³±cza o okre¶lonym pa¶mie oraz innych. Dzia³a w warstwie
user space, wiêc nie wymaga dodatkowego wsparcia w j±drze.

%prep
%setup -q -n vtun
%patch2 -p1
%patch5 -p1
%patch6 -p1
# must be ported
#%%patch4 -p1

%build
cp -f /usr/share/automake/config.* .
# aclocal.m4 is only local, don't try to rebuild
%{__autoheader}
%{__autoconf}
%configure \
	%{?with_ssl:--with-crypto-headers=%{_includedir}/openssl} \
	%{!?with_ssl:--disable-ssl} \
	--enable-lzo
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT{/etc/{sysconfig,rc.d/init.d},%{_localstatedir}/log/vtun}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL_OWNER=""

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/vtund
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/vtun
touch $RPM_BUILD_ROOT%{_sysconfdir}/vtund.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add vtund
if [ -f /var/lock/subsys/vtund ]; then
	/etc/rc.d/init.d/vtund restart >&2
else
	echo "Run \"/etc/rc.d/init.d/vtund start\" to start vtun daemons."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/vtund ]; then
		/etc/rc.d/init.d/vtund stop >&2
	fi
	/sbin/chkconfig --del vtund
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog Credits README README.Setup README.Shaper FAQ TODO vtund.conf
%attr(754,root,root) /etc/rc.d/init.d/vtund
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/vtun
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/vtund.conf
%attr(755,root,root) %{_sbindir}/vtund
%attr(755,root,root) %dir /var/log/vtund
%{_mandir}/man*/*
