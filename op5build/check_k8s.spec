%define plugin_root /opt/plugins
%define check_k8s check_k8s.py

Summary: Kubernetes plugin for Nagios
Name: monitor-plugin-check_k8s
Version: %{op5version}
Release: %{op5release}%{?dist}
Vendor: OP5 AB
License: GPL-2.0
Group: op5/system-addons
URL: http://www.op5.com/support
Prefix: /opt/plugins
Requires: python34
Source: %{name}-%{version}.tar.gz
BuildRequires: python34
BuildRequires: python34-setuptools
BuildRoot: %{_tmppath}/%{name}-%{version}
BuildArch: noarch

%description
Nagios plugin for monitoring Kubernetes Clusters, built using the Python standard library.

%prep
%setup -q -n %{name}-%{version}

%build
easy_install-3.4 --user pip
pip3.4 install poetry

# Install build-deps
poetry update

# Run tests
poetry run pytest

# Install scripts with preserved timestamps
%{__install} -D -p check_k8s.py %{buildroot}/%{plugin_root}/%{check_k8s}

%files
%defattr(-, monitor, root)
%attr(755, monitor, root) %{plugin_root}/%{check_k8s}

%clean
rm -rf %buildroot
