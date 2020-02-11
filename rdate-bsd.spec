Summary:	Remote clock reader (and local setter) - NetBSD version
Summary(pl.UTF-8):	Program podający (i ustawiający) zdalny czas zegara - wersja z NetBSD
Name:		rdate-bsd
Version:	1.4
Release:	11
License:	BSD
Group:		Networking/Utilities
Source0:	http://ftp.debian.org/debian/pool/r/rdate/rdate_%{version}.orig.tar.gz
# Source0-md5:	d2c8812d664a1f33886c1be1a6500109
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.cron
Patch0:		%{name}-debian.patch
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Provides:	rdate
Obsoletes:	rdate
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
rdate is a program that can retrieve the time from another machine on
your network. If run as root, it will also set your local time to that
of the machine you queried. It is not super accurate; get ntpd if you
are really worried about milliseconds.

This version was taken from NetBSD and it has useful '-a' option,
which causes using adjtimex() call to gradually skew the local time to
the remote time rather than just hopping.

%description -l pl.UTF-8
rdate jest programem który odczytuje datę i godzinę z innej maszyny w
sieci. Jeżeli jest uruchamiany jako root może także służyć do
synchronizacji lokalnego czasu względem innego komputera w sieci. Nie
jest zbyt dokładny i jeżeli milisekundy mają dla nas znaczenie należy
użyć ntpd.

Ta wersja pochodzi z NetBSD i ma przydatną opcję '-a', która powoduje
używanie wywołania adjtimex() w celu stopniowej zmiany czasu lokalnego
na odczytany zdalnie zamiast przeskoku.

%prep
%setup -q -n rdate-%{version}.orig
%patch0 -p1

%build
%{__cc} -o rdate %{rpmldflags} %{rpmcflags} -Dprogram_invocation_short_name=\"rdate\" -Dlint rdate.c -lutil

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man8,/etc/{rc.d/init.d,sysconfig,cron.daily}}

install rdate $RPM_BUILD_ROOT%{_bindir}
install rdate.8 $RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/rdate
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/rdate
install %{SOURCE3} $RPM_BUILD_ROOT/etc/cron.daily/rdate

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add rdate

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del rdate
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rdate
%attr(754,root,root) /etc/rc.d/init.d/rdate
%attr(755,root,root) /etc/cron.daily/rdate
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rdate
%{_mandir}/man8/*
