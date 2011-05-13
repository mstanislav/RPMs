# This is an RPM spec file for Duo Security's 'duo_unix' package

%define _topdir         /root/duo_unix
%define name            duo_unix
%define release         1
%define version         1.6
%define buildroot       %{_topdir}/%{name}-%{version}-root

Name:                   %{name}
Vendor:                 Duo Security
Summary:                duo_unix - Duo two-factor authentication for Unix systems
Version:                %{version}
Release:                %{release}
License:                GPLv2
Group:                  Productivity/Security
URL:                    https://github.com/duosecurity/duo_unix
Source:                 %{name}-%{version}.tar.gz
Requires:               curl-devel,openssl-devel,pam-devel
Prefix:                 /usr
BuildArch:              noarch
BuildRoot:              %{buildroot}
Packager:               Mark Stanislav <mark.stanislav@gmail.com>

%description
Duo provides simple two-factor authentication as a service via:

 1.  Phone callback
 2.  SMS-delivered one-time passcodes
 3.  Duo mobile app to generate one-time passcodes
 4.  Duo mobile app for smartphone push authentication
 5.  Duo hardware token to generate one-time passcodes

This package allows an admin (or ordinary user) to quickly add Duo
authentication to any Unix login without setting up secondary user
accounts, directory synchronization, servers, or hardware.

%prep
%setup -q

%build
./configure --with-pam --with-privsep-user=sshd --sysconfdir=/etc/duo
make

%install
make install prefix=$RPM_BUILD_ROOT/usr

%files
%defattr(-,root,root)
/usr/include/duo.h
/usr/lib/libduo.a
/usr/lib/libduo.la
/usr/lib/libduo.so
/usr/lib/libduo.so.1
/usr/lib/libduo.so.1.0.0
/usr/lib/pkgconfig/libduo.pc
/usr/sbin/login_duo
/usr/share/man/man3/duo.3.gz
/usr/share/man/man8/login_duo.8.gz
/usr/share/man/man8/pam_duo.8.gz

%doc AUTHORS CHANGES LICENSE README README.pam README.ssh

%post
mkdir -p /etc/duo
if [ ! -f /etc/duo/login_duo.conf ]; then
	echo -e "[duo]\n; Duo integration key\nikey = \n; Duo secret key\nskey = \n; Duo API host\nhost = api-eval.duosecurity.com" > /etc/duo/login_duo.conf
	chown sshd:sshd /etc/duo/login_duo.conf
	chmod 600 /etc/duo/login_duo.conf
fi
/sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu May 12 2011 Mark Stanislav <mark.stanislav@gmail.com> - 1.6-1
- Initial packaging of duo_sec version 1.6
- Check for existence of login_duo.conf before generating a template version
- Remove debug files from being included in the RPM
* Tue Apr 19 2011 Mark Stanislav <mark.stanislav@gmail.com> - 1.5-1
- Initial packaging of duo_sec version 1.5
