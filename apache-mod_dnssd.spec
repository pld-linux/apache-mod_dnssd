%define		apxs		%{_sbindir}/apxs
Summary:	mod_dnssd - Apache HTTPD module which adds Zeroconf support via DNS-SD using Avahi
Summary(pl.UTF-8):	mod_dnssd - moduł Apache HTTPD oddający obsługę Zeroconfa poprzez DNS-SD przy użyciu Avahi
Name:		apache-mod_dnssd
Version:	0.6
Release:	3
License:	Apache v2.0
Group:		Networking/Daemons/HTTP
Source0:	http://0pointer.de/lennart/projects/mod_dnssd/mod_dnssd-%{version}.tar.gz
# Source0-md5:	bed3d95a98168bf0515922d1c05020c5
Source1:	mod_dnssd.conf
Patch0:		apache-2.4.patch
URL:		http://0pointer.de/lennart/projects/mod_dnssd/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.2
BuildRequires:	apr-devel >= 1
BuildRequires:	avahi-devel >= 0.6
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
mod_dnssd is an Apache HTTPD module which adds Zeroconf support via
DNS-SD using Avahi.

%description -l pl.UTF-8
mod_dnssd to moduł serwera Apache HTTPD dodający obsługę Zeroconfa
poprzez DNS-SD przy użyciu Avahi.

%prep
%setup -q -n mod_dnssd-%{version}
%patch -P0 -p1

%build
%configure \
	APXS="%{apxs}"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}
install -p src/.libs/mod_dnssd.so $RPM_BUILD_ROOT%{_pkglibdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/90_mod_dnssd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_dnssd.conf
%attr(755,root,root) %{_pkglibdir}/mod_dnssd.so
