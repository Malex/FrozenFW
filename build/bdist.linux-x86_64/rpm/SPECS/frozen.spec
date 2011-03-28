%define name frozen
%define version 2.0_alpha
%define unmangled_version 2.0-alpha
%define unmangled_version 2.0-alpha
%define release 1

Summary: A simple but cool framework for wsgi
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GNU/GPL3
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Malex <malexprojects@gmail.com>
Url: http://malexprojects.ath.cx/?p=frozen

%description
It provides lots of classes and functions for web developing, using wsgi interface and a cool plugin system

%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
