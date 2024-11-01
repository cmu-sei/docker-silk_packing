[![Software Engineering Institute](https://avatars.githubusercontent.com/u/12465755?s=200&v=4)](https://www.sei.cmu.edu/)

[![Blog](https://img.shields.io/static/v1.svg?color=468f8b&labelColor=555555&logoColor=ffffff&style=for-the-badge&label=SEI&message=Blog)](https://insights.sei.cmu.edu/blog/ "blog posts from our experts in Software Engineering.")
[![Youtube](https://img.shields.io/static/v1.svg?color=468f8b&labelColor=555555&logoColor=ffffff&style=for-the-badge&label=SEI&message=Youtube&logo=youtube)](https://www.youtube.com/@TheSEICMU/ "vidoes from our experts in Software Engineering.")
[![Podcasts](https://img.shields.io/static/v1.svg?color=468f8b&labelColor=555555&logoColor=ffffff&style=for-the-badge&label=SEI&message=Podcasts&logo=applepodcasts)](https://insights.sei.cmu.edu/podcasts/ "podcasts from our experts in Software Engineering.")
[![GitHub](https://img.shields.io/static/v1.svg?color=468f8b&labelColor=555555&logoColor=ffffff&style=for-the-badge&label=SEI&message=GitHub&logo=github)](https://github.com/cmu-sei "view the source for all of our repositories.")
[![Flow Tools](https://img.shields.io/static/v1.svg?color=468f8b&labelColor=555555&logoColor=ffffff&style=for-the-badge&label=SEI&message=Flow%20Tools)](https://tools.netsa.cert.org/ "documentation and source for all our flow collection and analysis tools.")


At the [SEI](https://www.sei.cmu.edu/), we research software engineering, cybersecurity, and AI engineering problems; create innovative technologies; and put solutions into practice.

Find us at:

* [Blog](https://insights.sei.cmu.edu/blog/) - blog posts from our experts in Software Engineering.
* [Youtube](https://www.youtube.com/@TheSEICMU/) - vidoes from our experts in Software Engineering.
* [Podcasts](https://insights.sei.cmu.edu/podcasts/) - podcasts from our experts in Software Engineering.
* [GitHub](https://github.com/cmu-sei) - view the source for all of our repositories.
* [Flow Tools](https://tools.netsa.cert.org/) - documentation and source for all our flow collection and analysis tools.

# [certcc/silk](https://tools.netsa.cert.org/silk/docs.html)

[![CI](https://img.shields.io/github/actions/workflow/status/cmu-sei/docker-silk_packing/release.yml?style=for-the-badge&logo=github)](https://github.com/cmu-sei/docker-silk_packing/actions?query=workflow%3ARelease) [![Docker pulls](https://img.shields.io/docker/pulls/cmusei/silk_packing?color=468f8b&labelColor=555555&logoColor=ffffff&style=for-the-badge&label=pulls&logo=docker)](https://hub.docker.com/r/cmusei/silk_packing/)

SiLK, the System for Internet-Level Knowledge, is a collection of traffic analysis tools developed by the [CERT Network Situational Awareness Team](www.cert.org/netsa) (CERT NetSA) to facilitate security analysis of large networks. The SiLK tool suite supports the efficient collection, storage, and analysis of network flow data, enabling network security analysts to rapidly query large historical traffic data sets. SiLK is ideally suited for analyzing traffic on the backbone or border of a large, distributed enterprise or mid-sized ISP.

A SiLK installation consists of two categories of applications: the packing system and the analysis suite. The packing system collects IPFIX, NetFlow v9, or NetFlow v5 and converts the data into a more space efficient format, recording the packed records into service-specific binary flat files. The analysis suite consists of tools which read these flat files and perform various query operations, ranging from per-record filtering to statistical analysis of groups of records. The analysis tools interoperate using pipes, allowing a user to develop a relatively sophisticated query from a simple beginning.  This image contains **only** the packing suite tools.

The vast majority of the current code-base is implemented in C, Perl, or Python. This code has been tested on Linux, Solaris, OpenBSD, Mac OS X, and Cygwin, but should be usable with little or no change on other Unix platforms.

The SiLK software components are released under [the GNU General Public License V2](https://tools.netsa.cert.org/silk/license.html). 

## Documentation

More information [here](https://tools.netsa.cert.org/silk/docs.html).

## Usage

The intention of this container image is to allow for usage of the SiLK packing collection of command-line tools. The [SiLK Packing System](https://tools.netsa.cert.org/silk/docs.html#packing) is comprised of daemon applications that collect flow data (IPFIX flows from [yaf](https://tools.netsa.cert.org/yaf/index.html) or NetFlow v5 or v9 PDUs from a router) and convert them into a more space efficient format, storing the packed records into service-specific binary flat files for use by the [analysis suite](https://tools.netsa.cert.org/silk/docs.html#analysis). Files are organized in a time-based directory hierarchy with files covering each hour at the leaves. 

Here is an example scenario to help get you started.

### Connect [rwflowpack](https://tools.netsa.cert.org/silk/rwflowpack.html) to [yaf](https://tools.netsa.cert.org/yaf/index.html)

The following example configures yaf to continuously capture packets from the host `ens192` interface and output them to a container running rwflowpack listening on port 18001 in order to collect and store binary SiLK Flow files.

First, we start rwflowpack by running the `silk_packing` container. We can make use of the [silk.conf](examples/rwflowpack/silk.conf) and [sensor.conf](examples/rwflowpack/sensor.conf) files included in the [examples](examples/) folder.  Make sure to edit the internal-ipblocks in the [sensor.conf](examples/rwflowpack/sensor.conf) to match your network:

```bash
docker run --name rwflowpack -v $PWD/examples/rwflowpack:/data \
  -p 18001:18001 \
  -d cmusei/silk_packing:latest \
  rwflowpack \
  --input-mode=stream \
  --root-directory=/data \
  --sensor-configuration=/data/sensor.conf \
  --site-config-file=/data/silk.conf \
  --output-mode=local-storage \
  --log-destination=stdout \
  --no-daemon
```

Second, we start yaf through the `yaf` container and configure it to continuously capture packets from the host `ens192` interface. This time we have it output to the rwflowpack container listening on port 18001:
```bash
docker run --name yaf --cap-add NET_ADMIN --net=host \
  -d cmusei/yaf:latest \
  --in ens192 \
  --live pcap \
  --ipfix tcp \
  --out localhost \
  --silk \
  --verbose \
  --ipfix-port=18001 \
  --applabel \
  --max-payload 2048 \
  --plugin-name=/netsa/lib/yaf/dpacketplugin.so
```

We can check on the status of our containers via:
```bash
docker logs -f yaf
docker logs -f rwflowpack
```

Eventually you should see rwflowpack output some log lines similar to the following:
```bash
Oct 30 18:57:43 d23189499d6a rwflowpack[1]: /data/in/2023/10/30/in-S0_20231030.18: 15 recs
Oct 30 18:57:43 d23189499d6a rwflowpack[1]: /data/out/2023/10/30/out-S0_20231030.18: 15 recs
Oct 30 18:57:43 d23189499d6a rwflowpack[1]: /data/inweb/2023/10/30/iw-S0_20231030.18: 1 recs
Oct 30 18:57:43 d23189499d6a rwflowpack[1]: /data/outweb/2023/10/30/ow-S0_20231030.18: 1 recs
```

We can confirm SiLK is creating records by using the `silk_analysis` container:
```bash
docker run -v $PWD/examples/rwflowpack:/data --rm -it \
  --entrypoint=/bin/bash \
  cmusei/silk_analysis:latest \
  -c 'rwfilter --proto=0- --type=all --pass=stdout | rwcut | head'
```
```
     sIP|        dIP|sPort|dPort|pro|   packets|     bytes|   flags|                  sTime| duration|                  eTime|sen|
10.0.0.1|   10.0.0.2| 9998|33342|  6|         8|       447|   PA   |2023/10/30T18:49:20.567|    8.201|2023/10/30T18:49:28.768| S0|
10.0.0.1|   10.0.0.2| 9998|33342|  6|         1|        52|F   A   |2023/10/30T18:49:28.768|    0.000|2023/10/30T18:49:28.768| S0|
10.0.0.3|   10.0.0.2|45476| 5666|  6|        11|      2511|FS PA   |2023/10/30T18:49:47.027|    0.296|2023/10/30T18:49:47.323| S0|
10.0.0.4|   10.0.0.2| 9998|42162|  6|        23|      4408| S PA   |2023/10/30T18:49:28.675|   29.994|2023/10/30T18:49:58.669| S0|
10.0.0.4|   10.0.0.2| 9998|42162|  6|         1|        52|F   A   |2023/10/30T18:49:58.669|    0.000|2023/10/30T18:49:58.669| S0|
10.0.0.3|   10.0.0.2|45698| 5666|  6|        15|      2767|FS PA   |2023/10/30T18:50:17.146|    0.011|2023/10/30T18:50:17.157| S0|
10.0.0.3|   10.0.0.2|45698| 5666|  6|         1|        52|    A   |2023/10/30T18:50:17.157|    0.000|2023/10/30T18:50:17.157| S0|
10.0.0.3|   10.0.0.2|45692| 5666|  6|        15|      2767|FS PA   |2023/10/30T18:50:17.142|    0.038|2023/10/30T18:50:17.180| S0|
10.0.0.3|   10.0.0.2|45692| 5666|  6|         1|        52|    A   |2023/10/30T18:50:17.180|    0.000|2023/10/30T18:50:17.180| S0|
```

We can achieve the same thing by using docker-compose (recommended):
```yaml
---
version: '2.2'

services:
  rwflowpack:
    image: cmusei/silk_packing:latest
    container_name: rwflowpack
    ports:
      - 18001:18001
    volumes:
      - "./examples/rwflowpack:/data"
    command: >
        rwflowpack
        --input-mode=stream
        --root-directory=/data
        --sensor-configuration=/data/sensor.conf
        --site-config-file=/data/silk.conf
        --output-mode=local-storage
        --log-destination=stdout
        --no-daemon
    healthcheck:
      test: timeout 10s bash -c ':> /dev/tcp/127.0.0.1/18001' || exit 1
      interval: 10s
      timeout: 5s
      retries: 3
  yaf:
    image: cmusei/yaf:latest
    container_name: yaf
    cap_add:
      - NET_ADMIN
    network_mode: "host"
    command: >
        --in ens192 
        --live pcap 
        --ipfix tcp 
        --out localhost 
        --silk 
        --verbose 
        --ipfix-port=18001 
        --applabel 
        --max-payload 2048 
        --plugin-name=/netsa/lib/yaf/dpacketplugin.so
    depends_on:
      rwflowpack:
        condition: service_healthy
```
