%define plugin_root /opt/plugins
%define exec_path check_k8s.py
%define pkg_path k8s

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
BuildRequires: wget
BuildRoot: %{_tmppath}/%{name}-%{version}
BuildArch: noarch

%description
Nagios plugin for monitoring Kubernetes Clusters, built using the Python standard library.

%prep
%setup -q -n %{name}-%{version}

%build
python3.4 -m venv .venv
source .venv/bin/activate
python3.4 -m pip install pytest
python3.4 -m pytest

%{__install} -D -p %{exec_path} %{buildroot}/%{plugin_root}/%{exec_path}
cp --archive %{pkg_path} %{buildroot}/%{plugin_root}/

%files
%defattr(-, monitor, root)
%attr(755, monitor, root) %{plugin_root}/%{exec_path}
%attr(755, monitor, root) %{plugin_root}/%{pkg_path}/*

%clean
rm -rf %buildroot
