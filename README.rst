==============
vsltrans
==============


-----------------------------------
Re-format tool for vsl(varnishlog)
-----------------------------------

:Author: Shohei Tanaka(@xcir)
:Date: 2013-06-24
:Version: 0.1
:Manual section: 1


DESCRIPTION
===========
Re-format tool for vsl(varnishlog)

HOW TO USE
===========

Read from varnish process.(use libvarnishapi)
***********************************************
::

  normal
    python vsltrans.py
  
  Specify libvarnishapi
    python vsltrans.py -libvapi /usr/lib64/libvarnishapi.so.1

Read from logfile
***********************************************
::

  normal
    python vsltrans.py -f test.log


Other option
***********************************************
::

  matches regex(can multiple specify)
    python vsltrans.py -m "rxheader:Cookie: locale"
    python vsltrans.py -m "rxheader:Cookie: locale" -m "rxurl:^/images"
  

Original log
---------------------------------------
::

    0 CLI          - Rd ping
    0 CLI          - Wr 200 19 PONG 1367731836 1.0
    0 CLI          - Rd ping
    0 CLI          - Wr 200 19 PONG 1367731839 1.0
   14 BackendOpen  b default 127.0.0.1 45642 127.0.0.1 88
   14 TxRequest    b GET
   14 TxURL        b /esi.html
   14 TxProtocol   b HTTP/1.1
   14 TxHeader     b User-Agent: Wget/1.12 (linux-gnu)
   14 TxHeader     b Accept: */*
   14 TxHeader     b Host: 192.168.1.199:6081
   14 TxHeader     b restart: 0
   14 TxHeader     b X-Forwarded-For: 192.168.1.199
   14 TxHeader     b hello: 0000000000000000000000000000000000000000000000000000000000000000
   14 TxHeader     b X-Varnish: 2088372858
   14 TxHeader     b Accept-Encoding: gzip
   14 RxProtocol   b HTTP/1.1
   14 RxStatus     b 200
   14 RxResponse   b OK
   14 RxHeader     b Date: Sun, 05 May 2013 05:30:42 GMT
   14 RxHeader     b Server: Apache/2.2.15 (Scientific Linux)
   14 RxHeader     b Accept-Ranges: bytes
   14 RxHeader     b X-Mod-Pagespeed: 1.2.24.1-2581
   14 RxHeader     b Vary: Accept-Encoding
   14 RxHeader     b Content-Encoding: gzip
   14 RxHeader     b Cache-Control: max-age=0, no-cache
   14 RxHeader     b Content-Length: 87
   14 RxHeader     b Connection: close
   14 RxHeader     b Content-Type: text/html; charset=UTF-8
   14 Fetch_Body   b 4(length) cls 0 mklen 1
   14 Length       b 158
   14 BackendClose b default
   14 BackendOpen  b default 127.0.0.1 45643 127.0.0.1 88
   14 TxRequest    b GET
   14 TxURL        b /a.php
   14 TxProtocol   b HTTP/1.1
   14 TxHeader     b User-Agent: Wget/1.12 (linux-gnu)
   14 TxHeader     b Accept: */*
   14 TxHeader     b Host: 192.168.1.199:6081
   14 TxHeader     b restart: 0
   14 TxHeader     b X-Forwarded-For: 192.168.1.199
   14 TxHeader     b hello: 760afe4b8a8c559a63926dace564d5fb568f3e841160be1ebd3d14238fff1ee1
   14 TxHeader     b X-Varnish: 2088372858
   14 TxHeader     b Accept-Encoding: gzip
   14 RxProtocol   b HTTP/1.1
   14 RxStatus     b 200
   14 RxResponse   b OK
   14 RxHeader     b Date: Sun, 05 May 2013 05:30:42 GMT
   14 RxHeader     b Server: Apache/2.2.15 (Scientific Linux)
   14 RxHeader     b X-Powered-By: PHP/5.3.2
   14 RxHeader     b Cache-Control: max-age=0, no-cache
   14 RxHeader     b X-Mod-Pagespeed: 1.2.24.1-2581
   14 RxHeader     b Vary: Accept-Encoding
   14 RxHeader     b Content-Encoding: gzip
   14 RxHeader     b Content-Length: 47
   14 RxHeader     b Connection: close
   14 RxHeader     b Content-Type: text/html; charset=UTF-8
   14 Fetch_Body   b 4(length) cls 0 mklen 1
   14 Length       b 59
   14 BackendClose b default
   14 BackendOpen  b default 127.0.0.1 45644 127.0.0.1 88
   14 TxRequest    b GET
   14 TxURL        b /b.php
   14 TxProtocol   b HTTP/1.1
   14 TxHeader     b User-Agent: Wget/1.12 (linux-gnu)
   14 TxHeader     b Accept: */*
   14 TxHeader     b Host: 192.168.1.199:6081
   14 TxHeader     b restart: 0
   14 TxHeader     b X-Forwarded-For: 192.168.1.199
   14 TxHeader     b hello: b23228308dd19c6ea35060253b30a2df5ec74bcfe275581d22a8831a95f5022a
   14 TxHeader     b X-Varnish: 2088372858
   14 TxHeader     b Accept-Encoding: gzip
   14 RxProtocol   b HTTP/1.1
   14 RxStatus     b 200
   14 RxResponse   b OK
   14 RxHeader     b Date: Sun, 05 May 2013 05:30:42 GMT
   14 RxHeader     b Server: Apache/2.2.15 (Scientific Linux)
   14 RxHeader     b X-Powered-By: PHP/5.3.2
   14 RxHeader     b Cache-Control: max-age=0, no-cache
   14 RxHeader     b X-Mod-Pagespeed: 1.2.24.1-2581
   14 RxHeader     b Vary: Accept-Encoding
   14 RxHeader     b Content-Encoding: gzip
   14 RxHeader     b Content-Length: 47
   14 RxHeader     b Connection: close
   14 RxHeader     b Content-Type: text/html; charset=UTF-8
   14 Fetch_Body   b 4(length) cls 0 mklen 1
   14 Length       b 59
   14 BackendClose b default
   12 SessionOpen  c 192.168.1.199 43051 :6081
   12 ReqStart     c 192.168.1.199 43051 2088372858
   12 RxRequest    c GET
   12 RxURL        c /esi.html
   12 RxProtocol   c HTTP/1.0
   12 RxHeader     c User-Agent: Wget/1.12 (linux-gnu)
   12 RxHeader     c Accept: */*
   12 RxHeader     c Host: 192.168.1.199:6081
   12 RxHeader     c Connection: Keep-Alive
   12 VCL_call     c recv 1 16.1
   12 VCL_Log      c hogehojfdls
   12 VCL_trace    c 5 41.5
   12 VCL_trace    c 6 42.9
   12 VCL_trace    c 8 46.13
   12 VCL_trace    c 9 49.5
   12 VCL_trace    c 11 59.5
   12 VCL_trace    c 13 63.5
   12 VCL_trace    c 15 67.5
   12 VCL_return   c lookup
   12 VCL_call     c hash 2 34.1
   12 Hash         c bar
   12 VCL_trace    c 18 85.5
   12 Hash         c /esi.html
   12 VCL_trace    c 19 87.9
   12 Hash         c 192.168.1.199:6081
   12 VCL_return   c hash
   12 VCL_call     c miss 22 99.5 fetch
   12 Backend      c 14 default default
   12 TTL          c 2088372858 RFC 0 -1 -1 1367731842 0 1367731842 0 0
   12 VCL_call     c fetch 3 41.9 23 103.5 24 109.17
   12 TTL          c 2088372858 VCL 120 -1 -1 1367731842 -0
   12 VCL_return   c hit_for_pass
   12 ObjProtocol  c HTTP/1.1
   12 ObjResponse  c OK
   12 ObjHeader    c Date: Sun, 05 May 2013 05:30:42 GMT
   12 ObjHeader    c Server: Apache/2.2.15 (Scientific Linux)
   12 ObjHeader    c Accept-Ranges: bytes
   12 ObjHeader    c X-Mod-Pagespeed: 1.2.24.1-2581
   12 ObjHeader    c Vary: Accept-Encoding
   12 ObjHeader    c Content-Encoding: gzip
   12 ObjHeader    c Cache-Control: max-age=0, no-cache
   12 ObjHeader    c Content-Length: 87
   12 ObjHeader    c Content-Type: text/html; charset=UTF-8
   12 ESI_xmlerror c WARN at 53 ESI 1.0 <esi:include> lacks final '/'
   12 ESI_xmlerror c WARN at 85 ESI 1.0 <esi:include> lacks final '/'
   12 Gzip         c U F E 87 102 80 80 628
   12 Gzip         c G F E 102 158 80 1184 1194
   12 VCL_call     c deliver 4 45.9 26 116.5 deliver
   12 TxProtocol   c HTTP/1.1
   12 TxStatus     c 200
   12 TxResponse   c OK
   12 TxHeader     c Server: Apache/2.2.15 (Scientific Linux)
   12 TxHeader     c Accept-Ranges: bytes
   12 TxHeader     c X-Mod-Pagespeed: 1.2.24.1-2581
   12 TxHeader     c Vary: Accept-Encoding
   12 TxHeader     c Cache-Control: max-age=0, no-cache
   12 TxHeader     c Content-Type: text/html; charset=UTF-8
   12 TxHeader     c Date: Sun, 05 May 2013 05:30:42 GMT
   12 TxHeader     c X-Varnish: 2088372858
   12 TxHeader     c Age: 0
   12 TxHeader     c Via: 1.1 varnish
   12 TxHeader     c Connection: close
   12 TxHeader     c hello: 760afe4b8a8c559a63926dace564d5fb568f3e841160be1ebd3d14238fff1ee1
   12 TxHeader     c hello2: 0000000000000000000000000000000000000000000000000000000000000000
   12 VCL_call     c recv 1 16.1
   12 VCL_Log      c hogehojfdls
   12 VCL_trace    c 5 41.5
   12 VCL_trace    c 6 42.9
   12 VCL_trace    c 8 46.13
   12 VCL_trace    c 9 49.5
   12 VCL_trace    c 11 59.5
   12 VCL_trace    c 13 63.5
   12 VCL_trace    c 15 67.5
   12 VCL_return   c lookup
   12 VCL_call     c hash 2 34.1
   12 Hash         c bar
   12 VCL_trace    c 18 85.5
   12 Hash         c /a.php
   12 VCL_trace    c 19 87.9
   12 Hash         c 192.168.1.199:6081
   12 VCL_return   c hash
   12 VCL_call     c miss 22 99.5 fetch
   12 Backend      c 14 default default
   12 TTL          c 2088372858 RFC 0 -1 -1 1367731842 0 1367731842 0 0
   12 VCL_call     c fetch 3 41.9 23 103.5 24 109.17
   12 TTL          c 2088372858 VCL 120 -1 -1 1367731842 -0
   12 VCL_return   c hit_for_pass
   12 ObjProtocol  c HTTP/1.1
   12 ObjResponse  c OK
   12 ObjHeader    c Date: Sun, 05 May 2013 05:30:42 GMT
   12 ObjHeader    c Server: Apache/2.2.15 (Scientific Linux)
   12 ObjHeader    c X-Powered-By: PHP/5.3.2
   12 ObjHeader    c Cache-Control: max-age=0, no-cache
   12 ObjHeader    c X-Mod-Pagespeed: 1.2.24.1-2581
   12 ObjHeader    c Vary: Accept-Encoding
   12 ObjHeader    c Content-Encoding: gzip
   12 ObjHeader    c Content-Length: 47
   12 ObjHeader    c Content-Type: text/html; charset=UTF-8
   12 Gzip         c U F E 47 32 80 80 309
   12 Gzip         c G F E 32 59 80 392 402
   12 VCL_call     c deliver 4 45.9 26 116.5 deliver
   12 Gzip         c U D - 59 32 80 392 402
   12 VCL_call     c recv 1 16.1
   12 VCL_Log      c hogehojfdls
   12 VCL_trace    c 5 41.5
   12 VCL_trace    c 6 42.9
   12 VCL_trace    c 8 46.13
   12 VCL_trace    c 9 49.5
   12 VCL_trace    c 11 59.5
   12 VCL_trace    c 13 63.5
   12 VCL_trace    c 15 67.5
   12 VCL_return   c lookup
   12 VCL_call     c hash 2 34.1
   12 Hash         c bar
   12 VCL_trace    c 18 85.5
   12 Hash         c /b.php
   12 VCL_trace    c 19 87.9
   12 Hash         c 192.168.1.199:6081
   12 VCL_return   c hash
   12 VCL_call     c miss 22 99.5 fetch
   12 Backend      c 14 default default
   12 TTL          c 2088372858 RFC 0 -1 -1 1367731842 0 1367731842 0 0
   12 VCL_call     c fetch 3 41.9 23 103.5 24 109.17
   12 TTL          c 2088372858 VCL 120 -1 -1 1367731842 -0
   12 VCL_return   c hit_for_pass
   12 ObjProtocol  c HTTP/1.1
   12 ObjResponse  c OK
   12 ObjHeader    c Date: Sun, 05 May 2013 05:30:42 GMT
   12 ObjHeader    c Server: Apache/2.2.15 (Scientific Linux)
   12 ObjHeader    c X-Powered-By: PHP/5.3.2
   12 ObjHeader    c Cache-Control: max-age=0, no-cache
   12 ObjHeader    c X-Mod-Pagespeed: 1.2.24.1-2581
   12 ObjHeader    c Vary: Accept-Encoding
   12 ObjHeader    c Content-Encoding: gzip
   12 ObjHeader    c Content-Length: 47
   12 ObjHeader    c Content-Type: text/html; charset=UTF-8
   12 Gzip         c U F E 47 32 80 80 309
   12 Gzip         c G F E 32 59 80 392 402
   12 VCL_call     c deliver 4 45.9 26 116.5 deliver
   12 Gzip         c U D - 59 32 80 392 402
   12 Gzip         c U D E 78 50 80 0 0
   12 Length       c 64
   12 ReqEnd       c 2088372858 1367731842.320536137 1367731842.327375412 -0.006782293 nan nan
   12 SessionClose c EOF mode
   12 StatSess     c 192.168.1.199 43051 0 1 1 0 0 3 466 64



Re-formatted log(python vsltrans.py -f test.log)
---------------------------------------------------
::

  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
  START transaction.
  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
  General Info.
  ----------------------------------------------------------------------
  Client ip:port  | 192.168.1.199:43051
  Request host    | 192.168.1.199
  Response size   | 158 byte
  Response Status | HTTP/1.1 200 OK
  Total time      | 0.00684 sec
  Restart count   | 0
  ESI count       | 2
  Backend count   | 3
   +Backend       | default
   +Backend       | default
   +Backend       | default
  ----------------------------------------------------------------------
  
  ######################################################################
  Object infomation.
  ----------------------------------------------------------------------
  Hash        | "bar" + "/esi.html" + "192.168.1.199:6081"
  ----------------------------------------------------------------------
  Vary        | req.http.Accept-Encoding |
  Object size | 158
  Backend     | default
  ----------------------------------------------------------------------
  
  ######################################################################
  Error infomation.
  ----------------------------------------------------------------------
  ESI_xmlerror | WARN at 53 ESI 1.0 <esi:include> lacks final '/'
  ESI_xmlerror | WARN at 85 ESI 1.0 <esi:include> lacks final '/'
  ----------------------------------------------------------------------
  
  ######################################################################
  Action infomation.
  ----------------------------------------------------------------------
  +-------------+
  |    recv     |
  +-------------+
        |
        | VCL_trace | (VRT_Count:1 line:16 pos:1)
        | VCL_Log   | hogehojfdls
        | VCL_trace | (VRT_Count:5 line:41 pos:5)
        | VCL_trace | (VRT_Count:6 line:42 pos:9)
        | VCL_trace | (VRT_Count:8 line:46 pos:13)
        | VCL_trace | (VRT_Count:9 line:49 pos:5)
        | VCL_trace | (VRT_Count:11 line:59 pos:5)
        | VCL_trace | (VRT_Count:13 line:63 pos:5)
        | VCL_trace | (VRT_Count:15 line:67 pos:5)
        |           |
        | return    | lookup
        |
  +-------------+
  |    hash     |
  +-------------+
        |
        | VCL_trace | (VRT_Count:2 line:34 pos:1)
        | Hash      | bar
        | VCL_trace | (VRT_Count:18 line:85 pos:5)
        | Hash      | /esi.html
        | VCL_trace | (VRT_Count:19 line:87 pos:9)
        | Hash      | 192.168.1.199:6081
        |           |
        | return    | hash
        |
  +-------------+
  |    miss     |
  +-------------+
        |
        | VCL_trace | (VRT_Count:22 line:99 pos:5)
        |           |
        | return    | fetch
        |
  +-------------+
  |    fetch    |
  +-------------+
        |
        | VCL_trace | (VRT_Count:3 line:41 pos:9)
        | VCL_trace | (VRT_Count:23 line:103 pos:5)
        | VCL_trace | (VRT_Count:24 line:109 pos:17)
        |           |
        | return    | hit_for_pass
        |
  +-------------+
  |   deliver   |
  +-------------+
        |
        | VCL_trace | (VRT_Count:4 line:45 pos:9)
        | VCL_trace | (VRT_Count:26 line:116 pos:5)
        |           |
        | return    | deliver
        |
  
  ######################################################################
  Variable infomation.
  -----------------------------------------------------------------------------------------------
  req.url                      | /esi.html
  req.request                  | GET
  req.xid                      | 2088372858
  req.http.User-Agent          | Wget/1.12 (linux-gnu)
  req.http.Accept              | */*
  req.http.Host                | 192.168.1.199
  req.http.Connection          | Keep-Alive
  req.proto                    | HTTP/1.0
  -----------------------------------------------------------------------------------------------
  bereq.url                    | /esi.html
  bereq.http.User-Agent        | Wget/1.12 (linux-gnu)
  bereq.http.Accept            | */*
  bereq.http.Host              | 192.168.1.199
  bereq.http.restart           | 0
  bereq.http.X-Forwarded-For   | 192.168.1.199
  bereq.http.hello             | 0000000000000000000000000000000000000000000000000000000000000000
  bereq.http.X-Varnish         | 2088372858
  bereq.http.Accept-Encoding   | gzip
  bereq.request                | GET
  bereq.proto                  | HTTP/1.1
  -----------------------------------------------------------------------------------------------
  beresp.status                | 200
  beresp.http.Date             | Sun, 05 May 2013 05
  beresp.http.Server           | Apache/2.2.15 (Scientific Linux)
  beresp.http.Accept-Ranges    | bytes
  beresp.http.X-Mod-Pagespeed  | 1.2.24.1-2581
  beresp.http.Vary             | Accept-Encoding
  beresp.http.Content-Encoding | gzip
  beresp.http.Cache-Control    | max-age=0, no-cache
  beresp.http.Content-Length   | 87
  beresp.http.Connection       | close
  beresp.http.Content-Type     | text/html; charset=UTF-8
  beresp.response              | OK
  beresp.proto                 | HTTP/1.1
  -----------------------------------------------------------------------------------------------
  obj.http.Date                | Sun, 05 May 2013 05
  obj.http.Server              | Apache/2.2.15 (Scientific Linux)
  obj.http.Accept-Ranges       | bytes
  obj.http.X-Mod-Pagespeed     | 1.2.24.1-2581
  obj.http.Vary                | Accept-Encoding
  obj.http.Content-Encoding    | gzip
  obj.http.Cache-Control       | max-age=0, no-cache
  obj.http.Content-Length      | 87
  obj.http.Content-Type        | text/html; charset=UTF-8
  obj.response                 | OK
  obj.proto                    | HTTP/1.1
  -----------------------------------------------------------------------------------------------
  resp.status                  | 200
  resp.http.Server             | Apache/2.2.15 (Scientific Linux)
  resp.http.Accept-Ranges      | bytes
  resp.http.X-Mod-Pagespeed    | 1.2.24.1-2581
  resp.http.Vary               | Accept-Encoding
  resp.http.Cache-Control      | max-age=0, no-cache
  resp.http.Content-Type       | text/html; charset=UTF-8
  resp.http.Date               | Sun, 05 May 2013 05
  resp.http.X-Varnish          | 2088372858
  resp.http.Age                | 0
  resp.http.Via                | 1.1 varnish
  resp.http.Connection         | close
  resp.http.hello              | 760afe4b8a8c559a63926dace564d5fb568f3e841160be1ebd3d14238fff1ee1
  resp.http.hello2             | 0000000000000000000000000000000000000000000000000000000000000000
  resp.response                | OK
  resp.proto                   | HTTP/1.1
  -----------------------------------------------------------------------------------------------
  
  ######################################################################
  Object infomation.
  ----------------------------------------------------------------------
  Type        | esi
  Hash        | "bar" + "/a.php" + "192.168.1.199:6081"
  Object size | 59
  Backend     | default
  ----------------------------------------------------------------------
  
  ######################################################################
  Action infomation.
  ----------------------------------------------------------------------
  +-------------+
  |    recv     |
  +-------------+
        |
        | VCL_trace | (VRT_Count:1 line:16 pos:1)
        | VCL_Log   | hogehojfdls
        | VCL_trace | (VRT_Count:5 line:41 pos:5)
        | VCL_trace | (VRT_Count:6 line:42 pos:9)
        | VCL_trace | (VRT_Count:8 line:46 pos:13)
        | VCL_trace | (VRT_Count:9 line:49 pos:5)
        | VCL_trace | (VRT_Count:11 line:59 pos:5)
        | VCL_trace | (VRT_Count:13 line:63 pos:5)
        | VCL_trace | (VRT_Count:15 line:67 pos:5)
        |           |
        | return    | lookup
        |
  +-------------+
  |    hash     |
  +-------------+
        |
        | VCL_trace | (VRT_Count:2 line:34 pos:1)
        | Hash      | bar
        | VCL_trace | (VRT_Count:18 line:85 pos:5)
        | Hash      | /a.php
        | VCL_trace | (VRT_Count:19 line:87 pos:9)
        | Hash      | 192.168.1.199:6081
        |           |
        | return    | hash
        |
  +-------------+
  |    miss     |
  +-------------+
        |
        | VCL_trace | (VRT_Count:22 line:99 pos:5)
        |           |
        | return    | fetch
        |
  +-------------+
  |    fetch    |
  +-------------+
        |
        | VCL_trace | (VRT_Count:3 line:41 pos:9)
        | VCL_trace | (VRT_Count:23 line:103 pos:5)
        | VCL_trace | (VRT_Count:24 line:109 pos:17)
        |           |
        | return    | hit_for_pass
        |
  +-------------+
  |   deliver   |
  +-------------+
        |
        | VCL_trace | (VRT_Count:4 line:45 pos:9)
        | VCL_trace | (VRT_Count:26 line:116 pos:5)
        |           |
        | return    | deliver
        |
  
  ######################################################################
  Variable infomation.
  -----------------------------------------------------------------------------------------------
  bereq.url                    | /a.php
  bereq.http.User-Agent        | Wget/1.12 (linux-gnu)
  bereq.http.Accept            | */*
  bereq.http.Host              | 192.168.1.199
  bereq.http.restart           | 0
  bereq.http.X-Forwarded-For   | 192.168.1.199
  bereq.http.hello             | 760afe4b8a8c559a63926dace564d5fb568f3e841160be1ebd3d14238fff1ee1
  bereq.http.X-Varnish         | 2088372858
  bereq.http.Accept-Encoding   | gzip
  bereq.request                | GET
  bereq.proto                  | HTTP/1.1
  -----------------------------------------------------------------------------------------------
  beresp.status                | 200
  beresp.http.Date             | Sun, 05 May 2013 05
  beresp.http.Server           | Apache/2.2.15 (Scientific Linux)
  beresp.http.X-Powered-By     | PHP/5.3.2
  beresp.http.Cache-Control    | max-age=0, no-cache
  beresp.http.X-Mod-Pagespeed  | 1.2.24.1-2581
  beresp.http.Vary             | Accept-Encoding
  beresp.http.Content-Encoding | gzip
  beresp.http.Content-Length   | 47
  beresp.http.Connection       | close
  beresp.http.Content-Type     | text/html; charset=UTF-8
  beresp.response              | OK
  beresp.proto                 | HTTP/1.1
  -----------------------------------------------------------------------------------------------
  obj.http.Date                | Sun, 05 May 2013 05
  obj.http.Server              | Apache/2.2.15 (Scientific Linux)
  obj.http.X-Powered-By        | PHP/5.3.2
  obj.http.Cache-Control       | max-age=0, no-cache
  obj.http.X-Mod-Pagespeed     | 1.2.24.1-2581
  obj.http.Vary                | Accept-Encoding
  obj.http.Content-Encoding    | gzip
  obj.http.Content-Length      | 47
  obj.http.Content-Type        | text/html; charset=UTF-8
  obj.response                 | OK
  obj.proto                    | HTTP/1.1
  -----------------------------------------------------------------------------------------------
  
  ######################################################################
  Object infomation.
  ----------------------------------------------------------------------
  Type        | esi
  Hash        | "bar" + "/b.php" + "192.168.1.199:6081"
  Object size | 64
  Backend     | default
  ----------------------------------------------------------------------
  
  ######################################################################
  Action infomation.
  ----------------------------------------------------------------------
  +-------------+
  |    recv     |
  +-------------+
        |
        | VCL_trace | (VRT_Count:1 line:16 pos:1)
        | VCL_Log   | hogehojfdls
        | VCL_trace | (VRT_Count:5 line:41 pos:5)
        | VCL_trace | (VRT_Count:6 line:42 pos:9)
        | VCL_trace | (VRT_Count:8 line:46 pos:13)
        | VCL_trace | (VRT_Count:9 line:49 pos:5)
        | VCL_trace | (VRT_Count:11 line:59 pos:5)
        | VCL_trace | (VRT_Count:13 line:63 pos:5)
        | VCL_trace | (VRT_Count:15 line:67 pos:5)
        |           |
        | return    | lookup
        |
  +-------------+
  |    hash     |
  +-------------+
        |
        | VCL_trace | (VRT_Count:2 line:34 pos:1)
        | Hash      | bar
        | VCL_trace | (VRT_Count:18 line:85 pos:5)
        | Hash      | /b.php
        | VCL_trace | (VRT_Count:19 line:87 pos:9)
        | Hash      | 192.168.1.199:6081
        |           |
        | return    | hash
        |
  +-------------+
  |    miss     |
  +-------------+
        |
        | VCL_trace | (VRT_Count:22 line:99 pos:5)
        |           |
        | return    | fetch
        |
  +-------------+
  |    fetch    |
  +-------------+
        |
        | VCL_trace | (VRT_Count:3 line:41 pos:9)
        | VCL_trace | (VRT_Count:23 line:103 pos:5)
        | VCL_trace | (VRT_Count:24 line:109 pos:17)
        |           |
        | return    | hit_for_pass
        |
  +-------------+
  |   deliver   |
  +-------------+
        |
        | VCL_trace | (VRT_Count:4 line:45 pos:9)
        | VCL_trace | (VRT_Count:26 line:116 pos:5)
        |           |
        | return    | deliver
        |
  
  ######################################################################
  Variable infomation.
  -----------------------------------------------------------------------------------------------
  bereq.url                    | /b.php
  bereq.http.User-Agent        | Wget/1.12 (linux-gnu)
  bereq.http.Accept            | */*
  bereq.http.Host              | 192.168.1.199
  bereq.http.restart           | 0
  bereq.http.X-Forwarded-For   | 192.168.1.199
  bereq.http.hello             | b23228308dd19c6ea35060253b30a2df5ec74bcfe275581d22a8831a95f5022a
  bereq.http.X-Varnish         | 2088372858
  bereq.http.Accept-Encoding   | gzip
  bereq.request                | GET
  bereq.proto                  | HTTP/1.1
  -----------------------------------------------------------------------------------------------
  beresp.status                | 200
  beresp.http.Date             | Sun, 05 May 2013 05
  beresp.http.Server           | Apache/2.2.15 (Scientific Linux)
  beresp.http.X-Powered-By     | PHP/5.3.2
  beresp.http.Cache-Control    | max-age=0, no-cache
  beresp.http.X-Mod-Pagespeed  | 1.2.24.1-2581
  beresp.http.Vary             | Accept-Encoding
  beresp.http.Content-Encoding | gzip
  beresp.http.Content-Length   | 47
  beresp.http.Connection       | close
  beresp.http.Content-Type     | text/html; charset=UTF-8
  beresp.response              | OK
  beresp.proto                 | HTTP/1.1
  -----------------------------------------------------------------------------------------------
  obj.http.Date                | Sun, 05 May 2013 05
  obj.http.Server              | Apache/2.2.15 (Scientific Linux)
  obj.http.X-Powered-By        | PHP/5.3.2
  obj.http.Cache-Control       | max-age=0, no-cache
  obj.http.X-Mod-Pagespeed     | 1.2.24.1-2581
  obj.http.Vary                | Accept-Encoding
  obj.http.Content-Encoding    | gzip
  obj.http.Content-Length      | 47
  obj.http.Content-Type        | text/html; charset=UTF-8
  obj.response                 | OK
  obj.proto                    | HTTP/1.1
  -----------------------------------------------------------------------------------------------
  
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  END transaction.
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

