%define exec_path check_k8s.py
%define pkg_path k8s

Summary: Kubernetes plugin for Nagios
Name: monitor-plugin-check_k8s
Version: %{op5version}
Release: %{op5release}%{?dist}
Vendor: OP5 AB
License: GPLv2
Group: op5/system-addons
URL: https://www.itrsgroup.com
Prefix: /opt/plugins
Requires: python3
BuildRequires: python3
Requires: op5-monitor-user
Source: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}
BuildArch: noarch

%description
Nagios plugin for monitoring Kubernetes Clusters, built using the Python standard library.

%prep
%setup -q -n %{name}-%{version}

%build
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install pytest
python3 -m pytest

%{__install} -D -p %{exec_path} %{buildroot}%{prefix}/%{exec_path}
cp --archive %{pkg_path} %{buildroot}%{prefix}/

%files
%{prefix}
%license LICENSE
%doc README.md

%clean
rm -rf %buildroot

%changelog
* Fri Aug 07 2020 Jacob Hansen <jhansen@op5.com> - 0.1.0
- Add OP5-monitor-user requirement
* Fri Aug 16 2019 Robert Wikman <rwikman@op5.com> - 0.1.0
- Init
