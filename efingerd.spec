Summary:	Nice finger daemon
Summary(pl):	Sympatyczny serwer finger
Name:		efingerd
Version:	1.4.1
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
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
Jeszcze jeden fingerd dla unixa umo¿liwiaj±cy dok³adne sterowanie
wyj¶ciem. efingerd jest demonem finger który mo¿e uruchamiaæ programy
i wy¶wietlaæ ich wyj¶cie. Daje tobie kompletn± kontrolê nad tym co
jest wy¶wietlane oraz komu i jest extremalnie configurowalny.

%prep
%setup -q
%patch0 -p1

%build
%{__make} CFLAGS="%{?debug:-O0 -g}%{!?debug:$RPM_OPT_FLAGS}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd

%{__make} install install-doc DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/fingerd

gzip -9nf README CHANGES examples-{unusual,win95,standard}/*

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet sever" 1>&2
fi

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz examples-{unusual,win95,standard}
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) /etc/sysconfig/rc-inetd/fingerd
%dir %{_sysconfdir}/efingerd
%attr(755,root,root) %{_sysconfdir}/efingerd/*
%{_mandir}/man8/*
