Summary:	Nice finger daemon
Summary(pl):	Sympatyczny serwer finger
Name:		efingerd
Version:	1.6.1
Release:	4
License:	GPL
Group:		Networking/Daemons
Source0:	http://melkor.dnp.fmph.uniba.sk/~garabik/efingerd/%{name}_%{version}.tar.gz
Source1:	%{name}.inetd
Patch0:		%{name}-DESTDIR.patch
URL:		http://melkor.dnp.fmph.uniba.sk/~garabik/efingerd.html
Requires:	inetdaemon
Prereq:		rc-inetd >= 0.8.1
Provides:	fingerd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	libident-devel
Obsoletes:	bsd-fingerd
Obsoletes:	finger-server
Obsoletes:	cfingerd
Obsoletes:	ffingerd

%description
Another finger daemon for unix capable of fine-tuning your output.
efingerd is a finger daemon, which executes programs and displays
their output. This gives you complete control over what to display and
to who, and an extreme configurability.

%description -l pl
Efingerd jest kolejnym uniksowym demonem finger, kt�ry
poprzez swoje mo�liwo�ci konfiguracji pozwala na pe�n�
kontrol� tego, komu i w jaki spos�b s� prezentowane odpowiedzi
na zapytania finger - pokazuj�c wynik zewn�trznych program�w.

%prep
%setup -q
%patch0 -p1

%build
%{__make} CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd

%{__make} install install-doc DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/fingerd

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README CHANGES examples-{unusual,win95,standard}
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) /etc/sysconfig/rc-inetd/fingerd
%dir %{_sysconfdir}/efingerd
%attr(755,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/efingerd/*
%{_mandir}/man8/*
