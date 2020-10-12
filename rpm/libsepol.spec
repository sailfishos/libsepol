# based on work by The Fedora Project (2017)
# Copyright (c) 1998, 1999, 2000 Thai Open Source Software Center Ltd
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Summary: SELinux binary policy manipulation library
Name: libsepol
Version: 3.1
Release: 1
License: LGPLv2+
URL: https://github.com/SELinuxProject/selinux/wiki
Source: %{name}-%{version}.tar.bz2
Patch0001: 0001-libsepol-do-not-call-malloc-with-0-byte.patch
Patch0002: 0002-Support-Android-M-and-official-v30-sepolicy-format.patch
BuildRequires: dbus-glib-devel
BuildRequires: flex
BuildRequires: pcre-devel
BuildRequires: python3-base

%description
Security-enhanced Linux is a feature of the Linux® kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux.  The Security-enhanced Linux
kernel contains new architectural components originally developed to
improve the security of the Flask operating system. These
architectural components provide general support for the enforcement
of many kinds of mandatory access control policies, including those
based on the concepts of Type Enforcement®, Role-based Access
Control, and Multi-level Security.

libsepol provides an API for the manipulation of SELinux binary policies.
It is used by checkpolicy (the policy compiler) and similar tools, as well
as by programs like load_policy that need to perform specific transformations
on binary policies such as customizing policy boolean settings.

%package devel
Summary: Header files and libraries used to build policy manipulation tools
Requires: %{name} = %{version}-%{release}

%description devel
The libsepol-devel package contains the libraries and header files
needed for developing applications that manipulate binary policies.

%package static
Summary: static libraries used to build policy manipulation tools
Requires: %{name}-devel = %{version}-%{release}

%description static
The libsepol-static package contains the static libraries and header files
needed for developing applications that manipulate binary policies.

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%build
cd %{name}
%make_build CFLAGS="%{optflags}"

%install
mkdir -p ${RPM_BUILD_ROOT}/%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man3
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man8
# only install libsepol files
cd %{name}
make DESTDIR="${RPM_BUILD_ROOT}" LIBDIR="%{_libdir}" SHLIBDIR="%{_libdir}" install
rm -f ${RPM_BUILD_ROOT}%{_bindir}/genpolbools
rm -f ${RPM_BUILD_ROOT}%{_bindir}/genpolusers
rm -f ${RPM_BUILD_ROOT}%{_bindir}/chkcon
rm -rf ${RPM_BUILD_ROOT}%{_mandir}/man8
rm -rf ${RPM_BUILD_ROOT}%{_mandir}/ru/man8


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files static
%defattr(-,root,root)
%{_libdir}/libsepol.a

%files devel
%defattr(-,root,root)
%{_libdir}/libsepol.so
%{_libdir}/pkgconfig/libsepol.pc
%{_includedir}/sepol/*.h
%{_mandir}/man3/*.3.gz
%dir %{_includedir}/sepol
%dir %{_includedir}/sepol/policydb
%{_includedir}/sepol/policydb/*.h
%dir %{_includedir}/sepol/cil
%{_includedir}/sepol/cil/*.h

%files
%defattr(-,root,root)
%license %{name}/COPYING
%{_libdir}/libsepol.so.1
