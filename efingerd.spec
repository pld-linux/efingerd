Summary:	Nice finger daemon
Summary(pl.UTF-8):	Sympatyczny serwer finger
Name:		efingerd
Version:	1.6.7
Release:	1
License:	GPL
Group:		Networking/Daemons
# connection refused
#Source0:	http://melkor.dnp.fmph.uniba.sk/~garabik/efingerd/%{name}_%{version}.tar.gz
Source0:	http://deb.debian.org/debian/pool/main/e/efingerd/%{name}_%{version}.orig.tar.gz
# Source0-md5:	0257429419591607508fac1a18dfd6cd
Source1:	%{name}.inetd
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-fortune_path.patch
URL:		http://melkor.dnp.fmph.uniba.sk/~garabik/efingerd.html
BuildRequires:	libident-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	inetdaemon
Requires:	rc-inetd >= 0.8.1
Provides:	fingerd
Obsoletes:	bsd-fingerd
Obsoletes:	cfingerd
Obsoletes:	ffingerd
Obsoletes:	finger-server
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Another finger daemon for Unix capable of fine-tuning your output.
efingerd is a finger daemon, which executes programs and displays
their output. This gives you complete control over what to display and
to who, and an extreme configurability.

%description -l pl.UTF-8
Efingerd jest kolejnym uniksowym demonem finger, który poprzez swoje
możliwości konfiguracji pozwala na pełną kontrolę tego, komu i w jaki
sposób są prezentowane odpowiedzi na zapytania finger - pokazując
wynik zewnętrznych programów.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd

%{__make} install install-doc \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/fingerd

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q rc-inetd reload

%postun
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc README CHANGES examples-{unusual,win95,standard}
%attr(755,root,root) %{_sbindir}/efingerd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/fingerd
%dir %{_sysconfdir}/efingerd
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/efingerd/list
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/efingerd/log
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/efingerd/luser
%attr(755,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/efingerd/nouser
%{_mandir}/man8/efingerd.8*
