### simple_transfer

simple_transfer.pcap

使用binwalk 分离文件

```
# binwalk simple_transfer.pcap

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             Libpcap capture file, little-endian, version 2.4, Ethernet, snaplen: 262144
339380        0x52DB4         PDF document, version: "1.5"
339454        0x52DFE         Zlib compressed data, default compression
340171        0x530CB         Zlib compressed data, default compression
6380104       0x615A48        Zlib compressed data, default compression
6385002       0x616D6A        Zlib compressed data, default compression

```

```
# binwalk -e simple_transfer.pcap 
分离出了一个PDF文件
```

