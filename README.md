# jool-exporter

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Actions Status](https://github.com/cooperlees/jool-exporter/workflows/ci/badge.svg)](https://github.com/cooperlees/jool-exporter/actions)
[![PyPI](https://img.shields.io/pypi/v/jool-exporter)](https://pypi.org/project/jool-exporter/)
[![Downloads](https://pepy.tech/badge/jool-exporter/week)](https://pepy.tech/project/jool-exporter/week)

jool SIIT-DC + NAT64 stats prometheus exporter

## What is this?

jool-exporter is a prometheus exporter HTTP service that wraps `jool stats display`
and reads the statistics at the time of the request into promerthues compatible
format.

- jool-exporter changes `JSTAT` prefix to `jool_` prefix for key names
- We attach the explanation of each stat to the guages

## Install

From PyPI:

- `pip install jool-exporter`

From GitHub:

- `pip install git+git://github.com/cooperlees/jool-exporter`

## Running

`jool` CLI needs `CAP_NET_ADMIN` capability in order to pull the statistics. Due to this,
so does the jool-exporter process. It also need to ability to pass the capability to child
processes.

- From version **4.1.5** jool will no longer require this capability to query stats

The process can also just run was `root`, but running things listening externally as `root`
is a bad security process.

### SystemD

We have a [Systemd Service](jool-exporter.service) unit file commited to the repo that runs as nobody and passes the
capability to all children process.
- This is the recommended way to run the service

#### SystemD install

- `cp jool-exporter.service /etc/systemd/system`
- `sudo systemctl daemon-reload`
- `sudo systemctl enable jool-exporter`
- `sudo systemctl start jool-exporter`

Logs will by default go to journald

- `journalctl -u jool-exporter [-f]`

## Example Return

- curl http://localhost:6971/metrics

```prometheus
cooper@home1:~$ curl http://localhost:6971/metrics
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 373.0
python_gc_objects_collected_total{generation="1"} 0.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable object found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 40.0
python_gc_collections_total{generation="1"} 3.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="8",patchlevel="5",version="3.8.5"} 1.0
# HELP process_virtual_memory_bytes Virtual memory size in bytes.
# TYPE process_virtual_memory_bytes gauge
process_virtual_memory_bytes 1.81788672e+08
# HELP process_resident_memory_bytes Resident memory size in bytes.
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes 2.0611072e+07
# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1.60830649484e+09
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 15.11
# HELP process_open_fds Number of open file descriptors.
# TYPE process_open_fds gauge
process_open_fds 6.0
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 1024.0
# HELP jool_received6 jool metric
# TYPE jool_received6 gauge
jool_received6{hostname="home1.cooperlees.com"} 7.9109475e+07
# HELP jool_received4 jool metric
# TYPE jool_received4 gauge
jool_received4{hostname="home1.cooperlees.com"} 1.3273675e+08
# HELP jool_success Successful translations. (Note: 'Successful translation' does not imply that the packet was actually delivered.)
# TYPE jool_success gauge
jool_success{hostname="home1.cooperlees.com"} 4.501274e+06
# HELP jool_bib_entries Number of BIB entries currently held in the BIB.
# TYPE jool_bib_entries gauge
jool_bib_entries{hostname="home1.cooperlees.com"} 245.0
# HELP jool_sessions Number of session entries currently held in the BIB.
# TYPE jool_sessions gauge
jool_sessions{hostname="home1.cooperlees.com"} 245.0
# HELP jool_unknown_l4_proto Translations cancelled: Packet carried an unknown transport protocol. (Untranslatable by NAT64.)
# TYPE jool_unknown_l4_proto gauge
jool_unknown_l4_proto{hostname="home1.cooperlees.com"} 6783.0
# HELP jool_unknown_icmp6_type Translations cancelled: ICMPv6 header's type value has no ICMPv4 counterpart.
# TYPE jool_unknown_icmp6_type gauge
jool_unknown_icmp6_type{hostname="home1.cooperlees.com"} 279293.0
# HELP jool_pool6_mismatch Translations cancelled: IPv6 packet's destination address did not match pool6. (ie. Packet was not meant to be translated.)
# TYPE jool_pool6_mismatch gauge
jool_pool6_mismatch{hostname="home1.cooperlees.com"} 7.7009472e+07
# HELP jool_pool4_mismatch Translations cancelled: IPv4 packet's destination address and transport protocol did not match pool4. (ie. Packet was not meant to be translated.)\nIf the instance is a Netfilter translator, this counter increases randomly from normal operation, and is harmless.\nIf the instance is an iptables translator, this counter being positive suggests a mismatch between the IPv4 iptables rule(s) and the instance's configuration.
# TYPE jool_pool4_mismatch gauge
jool_pool4_mismatch{hostname="home1.cooperlees.com"} 1.30048136e+08
# HELP jool_bib4_not_found Translations cancelled: IPv4 packet did not match a BIB entry from the database.
# TYPE jool_bib4_not_found gauge
jool_bib4_not_found{hostname="home1.cooperlees.com"} 238.0
# HELP jool_syn6_expected Translations cancelled: Incoming IPv6 packet was the first of a TCP connection, but its SYN flag was disabled.
# TYPE jool_syn6_expected gauge
jool_syn6_expected{hostname="home1.cooperlees.com"} 268.0
# HELP jool_syn4_expected Translations cancelled: Incoming IPv4 packet was the first of a TCP connection, but its SYN flag was disabled.
# TYPE jool_syn4_expected gauge
jool_syn4_expected{hostname="home1.cooperlees.com"} 461.0
# HELP jool_type1pkt Total number of Type 1 packets stored. (See https://github.com/NICMx/Jool/blob/584a846d09e891a0cd6342426b7a25c6478c90d6/src/mod/nat64/bib/pkt_queue.h#L77) (This counter is not decremented when a packet leaves the queue.)
# TYPE jool_type1pkt gauge
jool_type1pkt{hostname="home1.cooperlees.com"} 299.0
# HELP jool_so_exists Translations cancelled: Packet was a Simultaneous Open retry. (Client was trying to punch a hole, and was being unnecessarily greedy.)
# TYPE jool_so_exists gauge
jool_so_exists{hostname="home1.cooperlees.com"} 1.0
```

## Grafana Dashbaord Example

![Grafana jool Dashboard Example](https://github.com/cooperlees/jool-exporter/blob/main/grafana_jool_example.png)

## Development

We use Facebook's [ptr](https://github.com/facebookincubator/ptr) for testing.

- `pip install ptr`
- `cd .`  # This repo
- `ptr [-k]`

It is driven by config in setup.py.
