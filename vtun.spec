Summary:	Virtual tunnel over TCP/IP networks
Summary(pl):	Wirtualne tunele poprzez sieci TCP/IP
Name:		vtun
Version:	2.4
Release:	5
Epoch:		1
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Vendor:		Maxim Krasnyansky <max_mk@yahoo.com>
Source0:	http://vtun.sourceforge.net/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-makefile.patch
URL:		http://vtun.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	autoconf
BuildRequires:	lzo-devel
BuildRequires:	openssl-devel >= 0.9.6a
BuildRequires:	zlib-devel
Prereq:		rc-scripts
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
VTun umo¿liwia tworzenie Wirtualnych Tunelu poprzez sieci TCP/IP
wraz z przydzielaniem pasma, kompresj±, szyfrowaniem danych w tunelach.
Wspierane typy tuneli to: PPP, IP, Ethernet i wiêkszo¶æ pozosta³ych
protoko³ów szeregowych.

%prep
%setup -q
%patch -p1

%build
aclocal
autoconf
%configure \
	--with-crypto-headers=%{_includedir}/openssl \
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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(754,root,root) /etc/rc.d/init.d/vtund
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/vtun
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/vtund.conf
%attr(755,root,root) %{_sbindir}/vtund
%attr(755,root,root) %dir /var/log/vtund
%{_mandir}/man*/*
