# Conditional build:
# _without_ssl - build without encryption ability

Summary:	Virtual tunnel over TCP/IP networks
Summary(pl):	Wirtualne tunele poprzez sieci TCP/IP
Name:		vtun
Version:	2.5
Release:	4
Epoch:		2
License:	GPL
Group:		Networking/Daemons
Vendor:		Maxim Krasnyansky <max_mk@yahoo.com>
Source0:	http://prdownloads.sourceforge.net/vtun/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-expect.patch
Patch2:		%{name}-autoheader.patch
Patch3:		%{name}-getpt.patch
Patch4:		%{name}-sslauth.patch
URL:		http://vtun.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	lzo-devel
%{!?_without_ssl:BuildRequires:	openssl-devel >= 0.9.6a}
BuildRequires:	zlib-devel
BuildRequires:	bison
BuildRequires:	flex
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	vppp

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
VTun umo¿liwia tworzenie Wirtualnych Tunelu poprzez sieci TCP/IP wraz
z przydzielaniem pasma, kompresj±, szyfrowaniem danych w tunelach.
Wspierane typy tuneli to: PPP, IP, Ethernet i wiêkszo¶æ pozosta³ych
protoko³ów szeregowych.

%prep
%setup -q -n vtun
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__aclocal}
%{__autoheader}
%{__autoconf}
%configure \
	%{!?_without_ssl:--with-crypto-headers=%{_includedir}/openssl} \
	%{?_without_ssl:--disable-ssl} \
	--enable-lzo
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT{/etc/{sysconfig,rc.d/init.d},%{_localstatedir}/log/vtun}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/vtund
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/vtun

gzip -9nf ChangeLog Credits README README.Setup README.Shaper FAQ TODO

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
%doc *.gz
%attr(754,root,root) /etc/rc.d/init.d/vtund
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/vtun
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/vtund.conf
%attr(755,root,root) %{_sbindir}/vtund
%attr(755,root,root) %dir /var/log/vtund
%{_mandir}/man*/*
