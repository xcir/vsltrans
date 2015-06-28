==============
vsltrans
==============


-----------------------------------
Re-format tool for vsl(varnishlog)
-----------------------------------

:Author: Shohei Tanaka(@xcir)
:Date: 2015-06-28
:Version: alpha2-varnish40
:Support Varnish Version: 4.0.x
:Manual section: 1

For Varnish3.0.x
=================
See this link.
https://github.com/xcir/vsltrans/tree/varnish30



DESCRIPTION
===========
Re-format tool for vsl(varnishlog)

ATTENTION
===========
This version is under development.

HOW TO USE
===========

Read from log-file(raw/vxid/request/session)
---------------------------------------------
::

  ./vsltrans.py -f test.log

Using VSL Query Expressions
--------------------------------------------
::

  # Does not support the VSL-Query, if read from log-file.
  ./vsltrans.py -q "requrl ~ '^/test'"

OUTPUT SAMPLE
===============

Original log
---------------------------------------
::

  *   << BeReq    >> 34472     
  -   Begin          bereq 34471 pass
  -   Timestamp      Start: 1435425942.277824 0.000000 0.000000
  -   BereqMethod    GET
  -   BereqURL       /esi.html
  -   BereqProtocol  HTTP/1.1
  -   BereqHeader    User-Agent: Wget/1.15 (linux-gnu)
  -   BereqHeader    Accept: */*
  -   BereqHeader    Host: 192.168.1.37:6081
  -   BereqHeader    X-Forwarded-For: 192.168.1.30
  -   BereqHeader    hogehoge: mage
  -   BereqHeader    X-Varnish: 34472
  -   VCL_call       BACKEND_FETCH
  -   VCL_return     fetch
  -   BackendClose   16 default(127.0.0.1,,88) toolate
  -   BackendOpen    16 default(127.0.0.1,,88) 127.0.0.1 36750 
  -   Backend        16 default default(127.0.0.1,,88)
  -   Timestamp      Bereq: 1435425942.277981 0.000157 0.000157
  -   Timestamp      Beresp: 1435425942.278194 0.000370 0.000213
  -   BerespProtocol HTTP/1.1
  -   BerespStatus   200
  -   BerespReason   OK
  -   BerespHeader   Date: Sat, 27 Jun 2015 17:25:42 GMT
  -   BerespHeader   Server: Apache/2.2.22 (Ubuntu)
  -   BerespHeader   Last-Modified: Sat, 27 Jun 2015 08:17:33 GMT
  -   BerespHeader   ETag: "281399-11f-5197b7d0b403a"
  -   BerespHeader   Accept-Ranges: bytes
  -   BerespHeader   Content-Length: 287
  -   BerespHeader   Vary: Accept-Encoding
  -   BerespHeader   Content-Type: text/html
  -   BerespHeader   X-Pad: avoid browser bug
  -   TTL            RFC 120 -1 -1 1435425942 1435425942 1435425942 0 0
  -   VCL_call       BACKEND_RESPONSE
  -   TTL            VCL 120 10 0 1435425942
  -   VCL_return     deliver
  -   Storage        malloc Transient
  -   ObjProtocol    HTTP/1.1
  -   ObjStatus      200
  -   ObjReason      OK
  -   ObjHeader      Date: Sat, 27 Jun 2015 17:25:42 GMT
  -   ObjHeader      Server: Apache/2.2.22 (Ubuntu)
  -   ObjHeader      Last-Modified: Sat, 27 Jun 2015 08:17:33 GMT
  -   ObjHeader      ETag: "281399-11f-5197b7d0b403a"
  -   ObjHeader      Accept-Ranges: bytes
  -   ObjHeader      Content-Length: 287
  -   ObjHeader      Vary: Accept-Encoding
  -   ObjHeader      Content-Type: text/html
  -   ObjHeader      X-Pad: avoid browser bug
  -   Fetch_Body     3 length -
  -   BackendReuse   16 default(127.0.0.1,,88)
  -   Timestamp      BerespBody: 1435425942.278284 0.000460 0.000090
  -   Length         287
  -   BereqAcct      164 0 164 285 287 572
  -   End            
  
  *   << BeReq    >> 34474     
  -   Begin          bereq 34473 pass
  -   Timestamp      Start: 1435425942.278412 0.000000 0.000000
  -   BereqMethod    GET
  -   BereqURL       /slow.php
  -   BereqProtocol  HTTP/1.1
  -   BereqHeader    User-Agent: Wget/1.15 (linux-gnu)
  -   BereqHeader    Accept: */*
  -   BereqHeader    Host: 192.168.1.37:6081
  -   BereqHeader    X-Forwarded-For: 192.168.1.30
  -   BereqHeader    hogehoge: mage
  -   BereqHeader    X-Varnish: 34474
  -   VCL_call       BACKEND_FETCH
  -   VCL_return     fetch
  -   Backend        16 default default(127.0.0.1,,88)
  -   Timestamp      Bereq: 1435425942.278457 0.000045 0.000045
  -   Timestamp      Beresp: 1435425943.279145 1.000733 1.000688
  -   BerespProtocol HTTP/1.1
  -   BerespStatus   200
  -   BerespReason   OK
  -   BerespHeader   Date: Sat, 27 Jun 2015 17:25:42 GMT
  -   BerespHeader   Server: Apache/2.2.22 (Ubuntu)
  -   BerespHeader   X-Powered-By: PHP/5.3.10-1ubuntu3.13
  -   BerespHeader   Vary: Accept-Encoding
  -   BerespHeader   Content-Length: 3
  -   BerespHeader   Content-Type: text/html
  -   TTL            RFC 120 -1 -1 1435425943 1435425943 1435425942 0 0
  -   VCL_call       BACKEND_RESPONSE
  -   TTL            VCL 120 10 0 1435425943
  -   VCL_return     deliver
  -   Storage        malloc Transient
  -   ObjProtocol    HTTP/1.1
  -   ObjStatus      200
  -   ObjReason      OK
  -   ObjHeader      Date: Sat, 27 Jun 2015 17:25:42 GMT
  -   ObjHeader      Server: Apache/2.2.22 (Ubuntu)
  -   ObjHeader      X-Powered-By: PHP/5.3.10-1ubuntu3.13
  -   ObjHeader      Vary: Accept-Encoding
  -   ObjHeader      Content-Length: 3
  -   ObjHeader      Content-Type: text/html
  -   Fetch_Body     3 length stream
  -   BackendReuse   16 default(127.0.0.1,,88)
  -   Timestamp      BerespBody: 1435425943.279240 1.000828 0.000095
  -   Length         3
  -   BereqAcct      164 0 164 193 3 196
  -   End            
  
  *   << Request  >> 34473     
  -   Begin          req 34471 esi
  -   Timestamp      Start: 1435425942.278370 0.000000 0.000000
  -   ReqStart       192.168.1.30 43851
  -   VCL_call       RECV
  -   VCL_return     pass
  -   VCL_call       HASH
  -   VCL_return     lookup
  -   VCL_call       PASS
  -   VCL_return     fetch
  -   Link           bereq 34474 pass
  -   Timestamp      Fetch: 1435425943.279234 1.000863 1.000863
  -   RespProtocol   HTTP/1.1
  -   RespStatus     200
  -   RespReason     OK
  -   RespHeader     Date: Sat, 27 Jun 2015 17:25:42 GMT
  -   RespHeader     Server: Apache/2.2.22 (Ubuntu)
  -   RespHeader     X-Powered-By: PHP/5.3.10-1ubuntu3.13
  -   RespHeader     Vary: Accept-Encoding
  -   RespHeader     Content-Length: 3
  -   RespHeader     Content-Type: text/html
  -   RespHeader     X-Varnish: 34473
  -   RespHeader     Age: 0
  -   RespHeader     Via: 1.1 varnish-v4
  -   VCL_call       DELIVER
  -   RespUnset      X-Powered-By: PHP/5.3.10-1ubuntu3.13
  -   RespHeader     x-powered-by: hoge
  -   RespUnset      x-powered-by: hoge
  -   RespHeader     restarts: 0
  -   VCL_return     deliver
  -   Timestamp      Process: 1435425943.279256 1.000885 0.000022
  -   RespUnset      Content-Length: 3
  -   RespHeader     Transfer-Encoding: chunked
  -   Debug          "RES_MODE 28"
  -   RespHeader     Connection: keep-alive
  -   Timestamp      Resp: 1435425943.279294 1.000924 0.000039
  -   Debug          "XXX REF 1"
  -   ESI_BodyBytes  3
  -   End            
  
  *   << BeReq    >> 34476     
  -   Begin          bereq 34475 pass
  -   Timestamp      Start: 1435425943.279357 0.000000 0.000000
  -   BereqMethod    GET
  -   BereqURL       /x.html
  -   BereqProtocol  HTTP/1.1
  -   BereqHeader    User-Agent: Wget/1.15 (linux-gnu)
  -   BereqHeader    Accept: */*
  -   BereqHeader    Host: 192.168.1.37:6081
  -   BereqHeader    X-Forwarded-For: 192.168.1.30
  -   BereqHeader    hogehoge: mage
  -   BereqHeader    X-Varnish: 34476
  -   VCL_call       BACKEND_FETCH
  -   VCL_return     fetch
  -   Backend        16 default default(127.0.0.1,,88)
  -   Timestamp      Bereq: 1435425943.279407 0.000050 0.000050
  -   Timestamp      Beresp: 1435425943.279580 0.000223 0.000173
  -   BerespProtocol HTTP/1.1
  -   BerespStatus   200
  -   BerespReason   OK
  -   BerespHeader   Date: Sat, 27 Jun 2015 17:25:43 GMT
  -   BerespHeader   Server: Apache/2.2.22 (Ubuntu)
  -   BerespHeader   Last-Modified: Wed, 18 Feb 2015 16:43:37 GMT
  -   BerespHeader   ETag: "280ea4-b-50f5f855c1b9e"
  -   BerespHeader   Accept-Ranges: bytes
  -   BerespHeader   Content-Length: 11
  -   BerespHeader   Vary: Accept-Encoding
  -   BerespHeader   Content-Type: text/html
  -   TTL            RFC 120 -1 -1 1435425943 1435425943 1435425943 0 0
  -   VCL_call       BACKEND_RESPONSE
  -   TTL            VCL 120 10 0 1435425943
  -   VCL_return     deliver
  -   Storage        malloc Transient
  -   ObjProtocol    HTTP/1.1
  -   ObjStatus      200
  -   ObjReason      OK
  -   ObjHeader      Date: Sat, 27 Jun 2015 17:25:43 GMT
  -   ObjHeader      Server: Apache/2.2.22 (Ubuntu)
  -   ObjHeader      Last-Modified: Wed, 18 Feb 2015 16:43:37 GMT
  -   ObjHeader      ETag: "280ea4-b-50f5f855c1b9e"
  -   ObjHeader      Accept-Ranges: bytes
  -   ObjHeader      Content-Length: 11
  -   ObjHeader      Vary: Accept-Encoding
  -   ObjHeader      Content-Type: text/html
  -   Fetch_Body     3 length stream
  -   BackendReuse   16 default(127.0.0.1,,88)
  -   Timestamp      BerespBody: 1435425943.279640 0.000283 0.000060
  -   Length         11
  -   BereqAcct      162 0 162 256 11 267
  -   End            
  
  *   << Request  >> 34475     
  -   Begin          req 34471 esi
  -   Timestamp      Start: 1435425943.279320 0.000000 0.000000
  -   ReqStart       192.168.1.30 43851
  -   VCL_call       RECV
  -   VCL_return     pass
  -   VCL_call       HASH
  -   VCL_return     lookup
  -   VCL_call       PASS
  -   VCL_return     fetch
  -   Link           bereq 34476 pass
  -   Timestamp      Fetch: 1435425943.279660 0.000340 0.000340
  -   RespProtocol   HTTP/1.1
  -   RespStatus     200
  -   RespReason     OK
  -   RespHeader     Date: Sat, 27 Jun 2015 17:25:43 GMT
  -   RespHeader     Server: Apache/2.2.22 (Ubuntu)
  -   RespHeader     Last-Modified: Wed, 18 Feb 2015 16:43:37 GMT
  -   RespHeader     ETag: "280ea4-b-50f5f855c1b9e"
  -   RespHeader     Accept-Ranges: bytes
  -   RespHeader     Content-Length: 11
  -   RespHeader     Vary: Accept-Encoding
  -   RespHeader     Content-Type: text/html
  -   RespHeader     X-Varnish: 34475
  -   RespHeader     Age: 0
  -   RespHeader     Via: 1.1 varnish-v4
  -   VCL_call       DELIVER
  -   RespHeader     x-powered-by: hoge
  -   RespUnset      x-powered-by: hoge
  -   RespHeader     restarts: 0
  -   VCL_return     deliver
  -   Timestamp      Process: 1435425943.279692 0.000372 0.000033
  -   RespUnset      Content-Length: 11
  -   RespUnset      ETag: "280ea4-b-50f5f855c1b9e"
  -   RespHeader     ETag: W/"280ea4-b-50f5f855c1b9e"
  -   RespHeader     Transfer-Encoding: chunked
  -   Debug          "RES_MODE 28"
  -   RespHeader     Connection: keep-alive
  -   Timestamp      Resp: 1435425943.279728 0.000408 0.000036
  -   Debug          "XXX REF 1"
  -   ESI_BodyBytes  11
  -   End            
  
  *   << Request  >> 34471     
  -   Begin          req 34470 rxreq
  -   Timestamp      Start: 1435425942.277738 0.000000 0.000000
  -   Timestamp      Req: 1435425942.277738 0.000000 0.000000
  -   ReqStart       192.168.1.30 43851
  -   ReqMethod      GET
  -   ReqURL         /esi.html
  -   ReqProtocol    HTTP/1.1
  -   ReqHeader      User-Agent: Wget/1.15 (linux-gnu)
  -   ReqHeader      Accept: */*
  -   ReqHeader      Host: 192.168.1.37:6081
  -   ReqHeader      Connection: Keep-Alive
  -   ReqHeader      X-Forwarded-For: 192.168.1.30
  -   VCL_call       RECV
  -   ReqHeader      hogehoge: mage
  -   VCL_return     pass
  -   VCL_call       HASH
  -   VCL_return     lookup
  -   VCL_call       PASS
  -   VCL_return     fetch
  -   Link           bereq 34472 pass
  -   Timestamp      Fetch: 1435425942.278297 0.000559 0.000559
  -   RespProtocol   HTTP/1.1
  -   RespStatus     200
  -   RespReason     OK
  -   RespHeader     Date: Sat, 27 Jun 2015 17:25:42 GMT
  -   RespHeader     Server: Apache/2.2.22 (Ubuntu)
  -   RespHeader     Last-Modified: Sat, 27 Jun 2015 08:17:33 GMT
  -   RespHeader     ETag: "281399-11f-5197b7d0b403a"
  -   RespHeader     Accept-Ranges: bytes
  -   RespHeader     Content-Length: 287
  -   RespHeader     Vary: Accept-Encoding
  -   RespHeader     Content-Type: text/html
  -   RespHeader     X-Pad: avoid browser bug
  -   RespHeader     X-Varnish: 34471
  -   RespHeader     Age: 0
  -   RespHeader     Via: 1.1 varnish-v4
  -   VCL_call       DELIVER
  -   RespHeader     x-powered-by: hoge
  -   RespUnset      x-powered-by: hoge
  -   ReqHeader      hoge: xxx
  -   RespHeader     restarts: 0
  -   VCL_return     deliver
  -   Timestamp      Process: 1435425942.278331 0.000592 0.000034
  -   RespUnset      Content-Length: 287
  -   RespUnset      ETag: "281399-11f-5197b7d0b403a"
  -   RespHeader     ETag: W/"281399-11f-5197b7d0b403a"
  -   RespHeader     Transfer-Encoding: chunked
  -   Debug          "RES_MODE 18"
  -   RespHeader     Connection: keep-alive
  -   Link           req 34473 esi
  -   ReqURL         /slow.php
  -   ReqMethod      GET
  -   ReqURL         /slow.php
  -   ReqProtocol    HTTP/1.1
  -   ReqHeader      User-Agent: Wget/1.15 (linux-gnu)
  -   ReqHeader      Accept: */*
  -   ReqHeader      Host: 192.168.1.37:6081
  -   ReqHeader      Connection: Keep-Alive
  -   ReqHeader      X-Forwarded-For: 192.168.1.30
  -   ReqHeader      hogehoge: mage
  -   ReqHeader      hoge: xxx
  -   Link           req 34475 esi
  -   ReqURL         /x.html
  -   ReqMethod      GET
  -   ReqURL         /x.html
  -   ReqProtocol    HTTP/1.1
  -   ReqHeader      User-Agent: Wget/1.15 (linux-gnu)
  -   ReqHeader      Accept: */*
  -   ReqHeader      Host: 192.168.1.37:6081
  -   ReqHeader      Connection: Keep-Alive
  -   ReqHeader      X-Forwarded-For: 192.168.1.30
  -   ReqHeader      hogehoge: mage
  -   ReqHeader      hoge: xxx
  -   Timestamp      Resp: 1435425943.279789 1.002051 1.001459
  -   Debug          "XXX REF 1"
  -   ESI_BodyBytes  227
  -   ReqAcct        123 0 123 378 283 661
  -   End            
  
  *   << Session  >> 34470     
  -   Begin          sess 0 HTTP/1
  -   SessOpen       192.168.1.30 43851 :6081 192.168.1.37 6081 1435425942.277663 15
  -   Link           req 34471 rxreq
  -   SessClose      REM_CLOSE 1.003
  -   End            
  


Re-formatted log(./vsltrans.py)
---------------------------------------------------
I'm thinking output format now...
::

  ************************************************************
  *                         Variable                         *
  ************************************************************
  
  ########################################
  #                Start                 #
  ########################################
  #              VXID:34478              #
  ########################################
     | 
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  >               vcl_recv               >
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     | 
     | +--------------------------+-------------------------+---------------------+---------------------+
     | |                      key |   Before vcl funciton   |   In vcl function   | After vcl function  | 
     | +--------------------------+-------------------------+---------------------+---------------------+
     | |                client.ip | '192.168.1.30 43853'    |                     |                     | 
     | |          req.http.Accept | '*/*'                   |                     |                     | 
     | |      req.http.Connection | 'Keep-Alive'            |                     |                     | 
     | |            req.http.Host | '192.168.1.37:6081'     |                     |                     | 
     | |      req.http.User-Agent | 'Wget/1.15 (linux-gnu)' |                     |                     | 
     | | req.http.X-Forwarded-For | '192.168.1.30'          |                     |                     | 
     | |        req.http.hogehoge |                         | 'mage'              |                     | 
     | |               req.method | 'GET'                   |                     |                     | 
     | |                req.proto | 'HTTP/1.1'              |                     |                     | 
     | |                  req.url | '/esi.html'             |                     |                     | 
     | +--------------------------+-------------------------+---------------------+---------------------+
     | 
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  >               vcl_hash               >
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     | 
     | 
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  >               vcl_pass               >
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     | 
     |                 | 
     |                 > ########################################
     |                 > #              VXID:34479              #
     |                 > ########################################
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >          vcl_backend_fetch           >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    | 
     |                 >    | +----------------------------+-------------------------+---------------------+---------------------+
     |                 >    | |                        key |   Before vcl funciton   |   In vcl function   | After vcl function  | 
     |                 >    | +----------------------------+-------------------------+---------------------+---------------------+
     |                 >    | |          bereq.http.Accept | '*/*'                   |                     |                     | 
     |                 >    | |            bereq.http.Host | '192.168.1.37:6081'     |                     |                     | 
     |                 >    | |      bereq.http.User-Agent | 'Wget/1.15 (linux-gnu)' |                     |                     | 
     |                 >    | | bereq.http.X-Forwarded-For | '192.168.1.30'          |                     |                     | 
     |                 >    | |       bereq.http.X-Varnish | '34479'                 |                     |                     | 
     |                 >    | |        bereq.http.hogehoge | 'mage'                  |                     |                     | 
     |                 >    | |               bereq.method | 'GET'                   |                     |                     | 
     |                 >    | |                bereq.proto | 'HTTP/1.1'              |                     |                     | 
     |                 >    | |                  bereq.url | '/esi.html'             |                     |                     | 
     |                 >    | +----------------------------+-------------------------+---------------------+---------------------+
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >         vcl_backend_response         >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    | 
     |                 >    | +----------------------------+---------------------------------+---------------------+---------------------------------+
     |                 >    | |                        key |       Before vcl funciton       |   In vcl function   |       After vcl function        | 
     |                 >    | +----------------------------+---------------------------------+---------------------+---------------------------------+
     |                 >    | |  beresp.http.Accept-Ranges | 'bytes'                         |                     |                                 | 
     |                 >    | | beresp.http.Content-Length | '287'                           |                     |                                 | 
     |                 >    | |   beresp.http.Content-Type | 'text/html'                     |                     |                                 | 
     |                 >    | |           beresp.http.Date | 'Sat, 27 Jun 2015 17:26:06 GMT' |                     |                                 | 
     |                 >    | |           beresp.http.ETag | '"281399-11f-5197b7d0b403a"'    |                     |                                 | 
     |                 >    | |  beresp.http.Last-Modified | 'Sat, 27 Jun 2015 08:17:33 GMT' |                     |                                 | 
     |                 >    | |         beresp.http.Server | 'Apache/2.2.22 (Ubuntu)'        |                     |                                 | 
     |                 >    | |           beresp.http.Vary | 'Accept-Encoding'               |                     |                                 | 
     |                 >    | |          beresp.http.X-Pad | 'avoid browser bug'             |                     |                                 | 
     |                 >    | |               beresp.proto | 'HTTP/1.1'                      |                     |                                 | 
     |                 >    | |              beresp.reason | 'OK'                            |                     |                                 | 
     |                 >    | |              beresp.status | '200'                           |                     |                                 | 
     |                 >    | |     obj.http.Accept-Ranges |                                 |                     | 'bytes'                         | 
     |                 >    | |    obj.http.Content-Length |                                 |                     | '287'                           | 
     |                 >    | |      obj.http.Content-Type |                                 |                     | 'text/html'                     | 
     |                 >    | |              obj.http.Date |                                 |                     | 'Sat, 27 Jun 2015 17:26:06 GMT' | 
     |                 >    | |              obj.http.ETag |                                 |                     | '"281399-11f-5197b7d0b403a"'    | 
     |                 >    | |     obj.http.Last-Modified |                                 |                     | 'Sat, 27 Jun 2015 08:17:33 GMT' | 
     |                 >    | |            obj.http.Server |                                 |                     | 'Apache/2.2.22 (Ubuntu)'        | 
     |                 >    | |              obj.http.Vary |                                 |                     | 'Accept-Encoding'               | 
     |                 >    | |             obj.http.X-Pad |                                 |                     | 'avoid browser bug'             | 
     |                 >    | |                  obj.proto |                                 |                     | 'HTTP/1.1'                      | 
     |                 >    | |                 obj.reason |                                 |                     | 'OK'                            | 
     |                 >    | |                 obj.status |                                 |                     | '200'                           | 
     |                 >    | +----------------------------+---------------------------------+---------------------+---------------------------------+
     | 
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  >             vcl_deliver              >
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     | 
     | +-----------------------------+---------------------------------+---------------------+------------------------------------------------------+
     | |                         key |       Before vcl funciton       |   In vcl function   |                  After vcl function                  | 
     | +-----------------------------+---------------------------------+---------------------+------------------------------------------------------+
     | |             req.http.Accept |                                 |                     | '*/*' -> '*/*'                                       | 
     | |         req.http.Connection |                                 |                     | 'Keep-Alive' -> 'Keep-Alive'                         | 
     | |               req.http.Host |                                 |                     | '192.168.1.37:6081' -> '192.168.1.37:6081'           | 
     | |         req.http.User-Agent |                                 |                     | 'Wget/1.15 (linux-gnu)' -> 'Wget/1.15 (linux-gnu)'   | 
     | |    req.http.X-Forwarded-For |                                 |                     | '192.168.1.30' -> '192.168.1.30'                     | 
     | |               req.http.hoge |                                 | 'xxx'               | 'xxx' -> 'xxx'                                       | 
     | |           req.http.hogehoge |                                 |                     | 'mage' -> 'mage'                                     | 
     | |                  req.method |                                 |                     | 'GET' -> 'GET'                                       | 
     | |                   req.proto |                                 |                     | 'HTTP/1.1' -> 'HTTP/1.1'                             | 
     | |                     req.url |                                 |                     | '/slow.php' -> '/slow.php' -> '/x.html' -> '/x.html' | 
     | |     resp.http.Accept-Ranges | 'bytes'                         |                     |                                                      | 
     | |               resp.http.Age | '0'                             |                     |                                                      | 
     | |        resp.http.Connection |                                 |                     | 'keep-alive'                                         | 
     | |    resp.http.Content-Length | '287'                           |                     | [unset]                                              | 
     | |      resp.http.Content-Type | 'text/html'                     |                     |                                                      | 
     | |              resp.http.Date | 'Sat, 27 Jun 2015 17:26:06 GMT' |                     |                                                      | 
     | |              resp.http.ETag | '"281399-11f-5197b7d0b403a"'    |                     | [unset] -> 'W/"281399-11f-5197b7d0b403a"'            | 
     | |     resp.http.Last-Modified | 'Sat, 27 Jun 2015 08:17:33 GMT' |                     |                                                      | 
     | |            resp.http.Server | 'Apache/2.2.22 (Ubuntu)'        |                     |                                                      | 
     | | resp.http.Transfer-Encoding |                                 |                     | 'chunked'                                            | 
     | |              resp.http.Vary | 'Accept-Encoding'               |                     |                                                      | 
     | |               resp.http.Via | '1.1 varnish-v4'                |                     |                                                      | 
     | |             resp.http.X-Pad | 'avoid browser bug'             |                     |                                                      | 
     | |         resp.http.X-Varnish | '34478'                         |                     |                                                      | 
     | |          resp.http.restarts |                                 | '0'                 |                                                      | 
     | |      resp.http.x-powered-by |                                 | 'hoge' -> [unset]   |                                                      | 
     | |                  resp.proto | 'HTTP/1.1'                      |                     |                                                      | 
     | |                 resp.reason | 'OK'                            |                     |                                                      | 
     | |                 resp.status | '200'                           |                     |                                                      | 
     | +-----------------------------+---------------------------------+---------------------+------------------------------------------------------+
     |                 | 
     |                 > ########################################
     |                 > #                 ESI                  #
     |                 > ########################################
     |                 > #              VXID:34480              #
     |                 > ########################################
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >               vcl_recv               >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    | 
     |                 >    | +---------------------+----------------------+---------------------+---------------------+
     |                 >    | |                 key | Before vcl funciton  |   In vcl function   | After vcl function  | 
     |                 >    | +---------------------+----------------------+---------------------+---------------------+
     |                 >    | |           client.ip | '192.168.1.30 43853' |                     |                     | 
     |                 >    | +---------------------+----------------------+---------------------+---------------------+
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >               vcl_hash               >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    | 
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >               vcl_pass               >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    | 
     |                 >    |                 | 
     |                 >    |                 > ########################################
     |                 >    |                 > #              VXID:34481              #
     |                 >    |                 > ########################################
     |                 >    |                 >    | 
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 > >          vcl_backend_fetch           >
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 >    | 
     |                 >    |                 >    | +----------------------------+-------------------------+---------------------+---------------------+
     |                 >    |                 >    | |                        key |   Before vcl funciton   |   In vcl function   | After vcl function  | 
     |                 >    |                 >    | +----------------------------+-------------------------+---------------------+---------------------+
     |                 >    |                 >    | |          bereq.http.Accept | '*/*'                   |                     |                     | 
     |                 >    |                 >    | |            bereq.http.Host | '192.168.1.37:6081'     |                     |                     | 
     |                 >    |                 >    | |      bereq.http.User-Agent | 'Wget/1.15 (linux-gnu)' |                     |                     | 
     |                 >    |                 >    | | bereq.http.X-Forwarded-For | '192.168.1.30'          |                     |                     | 
     |                 >    |                 >    | |       bereq.http.X-Varnish | '34481'                 |                     |                     | 
     |                 >    |                 >    | |        bereq.http.hogehoge | 'mage'                  |                     |                     | 
     |                 >    |                 >    | |               bereq.method | 'GET'                   |                     |                     | 
     |                 >    |                 >    | |                bereq.proto | 'HTTP/1.1'              |                     |                     | 
     |                 >    |                 >    | |                  bereq.url | '/slow.php'             |                     |                     | 
     |                 >    |                 >    | +----------------------------+-------------------------+---------------------+---------------------+
     |                 >    |                 >    | 
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 > >         vcl_backend_response         >
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 >    | 
     |                 >    |                 >    | +----------------------------+---------------------------------+---------------------+---------------------------------+
     |                 >    |                 >    | |                        key |       Before vcl funciton       |   In vcl function   |       After vcl function        | 
     |                 >    |                 >    | +----------------------------+---------------------------------+---------------------+---------------------------------+
     |                 >    |                 >    | | beresp.http.Content-Length | '3'                             |                     |                                 | 
     |                 >    |                 >    | |   beresp.http.Content-Type | 'text/html'                     |                     |                                 | 
     |                 >    |                 >    | |           beresp.http.Date | 'Sat, 27 Jun 2015 17:26:06 GMT' |                     |                                 | 
     |                 >    |                 >    | |         beresp.http.Server | 'Apache/2.2.22 (Ubuntu)'        |                     |                                 | 
     |                 >    |                 >    | |           beresp.http.Vary | 'Accept-Encoding'               |                     |                                 | 
     |                 >    |                 >    | |   beresp.http.X-Powered-By | 'PHP/5.3.10-1ubuntu3.13'        |                     |                                 | 
     |                 >    |                 >    | |               beresp.proto | 'HTTP/1.1'                      |                     |                                 | 
     |                 >    |                 >    | |              beresp.reason | 'OK'                            |                     |                                 | 
     |                 >    |                 >    | |              beresp.status | '200'                           |                     |                                 | 
     |                 >    |                 >    | |    obj.http.Content-Length |                                 |                     | '3'                             | 
     |                 >    |                 >    | |      obj.http.Content-Type |                                 |                     | 'text/html'                     | 
     |                 >    |                 >    | |              obj.http.Date |                                 |                     | 'Sat, 27 Jun 2015 17:26:06 GMT' | 
     |                 >    |                 >    | |            obj.http.Server |                                 |                     | 'Apache/2.2.22 (Ubuntu)'        | 
     |                 >    |                 >    | |              obj.http.Vary |                                 |                     | 'Accept-Encoding'               | 
     |                 >    |                 >    | |      obj.http.X-Powered-By |                                 |                     | 'PHP/5.3.10-1ubuntu3.13'        | 
     |                 >    |                 >    | |                  obj.proto |                                 |                     | 'HTTP/1.1'                      | 
     |                 >    |                 >    | |                 obj.reason |                                 |                     | 'OK'                            | 
     |                 >    |                 >    | |                 obj.status |                                 |                     | '200'                           | 
     |                 >    |                 >    | +----------------------------+---------------------------------+---------------------+---------------------------------+
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >             vcl_deliver              >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    | 
     |                 >    | +-----------------------------+---------------------------------+---------------------+---------------------+
     |                 >    | |                         key |       Before vcl funciton       |   In vcl function   | After vcl function  | 
     |                 >    | +-----------------------------+---------------------------------+---------------------+---------------------+
     |                 >    | |               resp.http.Age | '0'                             |                     |                     | 
     |                 >    | |        resp.http.Connection |                                 |                     | 'keep-alive'        | 
     |                 >    | |    resp.http.Content-Length | '3'                             |                     | [unset]             | 
     |                 >    | |      resp.http.Content-Type | 'text/html'                     |                     |                     | 
     |                 >    | |              resp.http.Date | 'Sat, 27 Jun 2015 17:26:06 GMT' |                     |                     | 
     |                 >    | |            resp.http.Server | 'Apache/2.2.22 (Ubuntu)'        |                     |                     | 
     |                 >    | | resp.http.Transfer-Encoding |                                 |                     | 'chunked'           | 
     |                 >    | |              resp.http.Vary | 'Accept-Encoding'               |                     |                     | 
     |                 >    | |               resp.http.Via | '1.1 varnish-v4'                |                     |                     | 
     |                 >    | |      resp.http.X-Powered-By | 'PHP/5.3.10-1ubuntu3.13'        | [unset]             |                     | 
     |                 >    | |         resp.http.X-Varnish | '34480'                         |                     |                     | 
     |                 >    | |          resp.http.restarts |                                 | '0'                 |                     | 
     |                 >    | |      resp.http.x-powered-by |                                 | 'hoge' -> [unset]   |                     | 
     |                 >    | |                  resp.proto | 'HTTP/1.1'                      |                     |                     | 
     |                 >    | |                 resp.reason | 'OK'                            |                     |                     | 
     |                 >    | |                 resp.status | '200'                           |                     |                     | 
     |                 >    | +-----------------------------+---------------------------------+---------------------+---------------------+
     |                 | 
     |                 > ########################################
     |                 > #                 ESI                  #
     |                 > ########################################
     |                 > #              VXID:34482              #
     |                 > ########################################
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >               vcl_recv               >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    | 
     |                 >    | +---------------------+----------------------+---------------------+---------------------+
     |                 >    | |                 key | Before vcl funciton  |   In vcl function   | After vcl function  | 
     |                 >    | +---------------------+----------------------+---------------------+---------------------+
     |                 >    | |           client.ip | '192.168.1.30 43853' |                     |                     | 
     |                 >    | +---------------------+----------------------+---------------------+---------------------+
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >               vcl_hash               >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    | 
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >               vcl_pass               >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    | 
     |                 >    |                 | 
     |                 >    |                 > ########################################
     |                 >    |                 > #              VXID:34483              #
     |                 >    |                 > ########################################
     |                 >    |                 >    | 
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 > >          vcl_backend_fetch           >
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 >    | 
     |                 >    |                 >    | +----------------------------+-------------------------+---------------------+---------------------+
     |                 >    |                 >    | |                        key |   Before vcl funciton   |   In vcl function   | After vcl function  | 
     |                 >    |                 >    | +----------------------------+-------------------------+---------------------+---------------------+
     |                 >    |                 >    | |          bereq.http.Accept | '*/*'                   |                     |                     | 
     |                 >    |                 >    | |            bereq.http.Host | '192.168.1.37:6081'     |                     |                     | 
     |                 >    |                 >    | |      bereq.http.User-Agent | 'Wget/1.15 (linux-gnu)' |                     |                     | 
     |                 >    |                 >    | | bereq.http.X-Forwarded-For | '192.168.1.30'          |                     |                     | 
     |                 >    |                 >    | |       bereq.http.X-Varnish | '34483'                 |                     |                     | 
     |                 >    |                 >    | |        bereq.http.hogehoge | 'mage'                  |                     |                     | 
     |                 >    |                 >    | |               bereq.method | 'GET'                   |                     |                     | 
     |                 >    |                 >    | |                bereq.proto | 'HTTP/1.1'              |                     |                     | 
     |                 >    |                 >    | |                  bereq.url | '/x.html'               |                     |                     | 
     |                 >    |                 >    | +----------------------------+-------------------------+---------------------+---------------------+
     |                 >    |                 >    | 
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 > >         vcl_backend_response         >
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 >    | 
     |                 >    |                 >    | +----------------------------+---------------------------------+---------------------+---------------------------------+
     |                 >    |                 >    | |                        key |       Before vcl funciton       |   In vcl function   |       After vcl function        | 
     |                 >    |                 >    | +----------------------------+---------------------------------+---------------------+---------------------------------+
     |                 >    |                 >    | |  beresp.http.Accept-Ranges | 'bytes'                         |                     |                                 | 
     |                 >    |                 >    | | beresp.http.Content-Length | '11'                            |                     |                                 | 
     |                 >    |                 >    | |   beresp.http.Content-Type | 'text/html'                     |                     |                                 | 
     |                 >    |                 >    | |           beresp.http.Date | 'Sat, 27 Jun 2015 17:26:07 GMT' |                     |                                 | 
     |                 >    |                 >    | |           beresp.http.ETag | '"280ea4-b-50f5f855c1b9e"'      |                     |                                 | 
     |                 >    |                 >    | |  beresp.http.Last-Modified | 'Wed, 18 Feb 2015 16:43:37 GMT' |                     |                                 | 
     |                 >    |                 >    | |         beresp.http.Server | 'Apache/2.2.22 (Ubuntu)'        |                     |                                 | 
     |                 >    |                 >    | |           beresp.http.Vary | 'Accept-Encoding'               |                     |                                 | 
     |                 >    |                 >    | |               beresp.proto | 'HTTP/1.1'                      |                     |                                 | 
     |                 >    |                 >    | |              beresp.reason | 'OK'                            |                     |                                 | 
     |                 >    |                 >    | |              beresp.status | '200'                           |                     |                                 | 
     |                 >    |                 >    | |     obj.http.Accept-Ranges |                                 |                     | 'bytes'                         | 
     |                 >    |                 >    | |    obj.http.Content-Length |                                 |                     | '11'                            | 
     |                 >    |                 >    | |      obj.http.Content-Type |                                 |                     | 'text/html'                     | 
     |                 >    |                 >    | |              obj.http.Date |                                 |                     | 'Sat, 27 Jun 2015 17:26:07 GMT' | 
     |                 >    |                 >    | |              obj.http.ETag |                                 |                     | '"280ea4-b-50f5f855c1b9e"'      | 
     |                 >    |                 >    | |     obj.http.Last-Modified |                                 |                     | 'Wed, 18 Feb 2015 16:43:37 GMT' | 
     |                 >    |                 >    | |            obj.http.Server |                                 |                     | 'Apache/2.2.22 (Ubuntu)'        | 
     |                 >    |                 >    | |              obj.http.Vary |                                 |                     | 'Accept-Encoding'               | 
     |                 >    |                 >    | |                  obj.proto |                                 |                     | 'HTTP/1.1'                      | 
     |                 >    |                 >    | |                 obj.reason |                                 |                     | 'OK'                            | 
     |                 >    |                 >    | |                 obj.status |                                 |                     | '200'                           | 
     |                 >    |                 >    | +----------------------------+---------------------------------+---------------------+---------------------------------+
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >             vcl_deliver              >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    | 
     |                 >    | +-----------------------------+---------------------------------+---------------------+-----------------------------------------+
     |                 >    | |                         key |       Before vcl funciton       |   In vcl function   |           After vcl function            | 
     |                 >    | +-----------------------------+---------------------------------+---------------------+-----------------------------------------+
     |                 >    | |     resp.http.Accept-Ranges | 'bytes'                         |                     |                                         | 
     |                 >    | |               resp.http.Age | '0'                             |                     |                                         | 
     |                 >    | |        resp.http.Connection |                                 |                     | 'keep-alive'                            | 
     |                 >    | |    resp.http.Content-Length | '11'                            |                     | [unset]                                 | 
     |                 >    | |      resp.http.Content-Type | 'text/html'                     |                     |                                         | 
     |                 >    | |              resp.http.Date | 'Sat, 27 Jun 2015 17:26:07 GMT' |                     |                                         | 
     |                 >    | |              resp.http.ETag | '"280ea4-b-50f5f855c1b9e"'      |                     | [unset] -> 'W/"280ea4-b-50f5f855c1b9e"' | 
     |                 >    | |     resp.http.Last-Modified | 'Wed, 18 Feb 2015 16:43:37 GMT' |                     |                                         | 
     |                 >    | |            resp.http.Server | 'Apache/2.2.22 (Ubuntu)'        |                     |                                         | 
     |                 >    | | resp.http.Transfer-Encoding |                                 |                     | 'chunked'                               | 
     |                 >    | |              resp.http.Vary | 'Accept-Encoding'               |                     |                                         | 
     |                 >    | |               resp.http.Via | '1.1 varnish-v4'                |                     |                                         | 
     |                 >    | |         resp.http.X-Varnish | '34482'                         |                     |                                         | 
     |                 >    | |          resp.http.restarts |                                 | '0'                 |                                         | 
     |                 >    | |      resp.http.x-powered-by |                                 | 'hoge' -> [unset]   |                                         | 
     |                 >    | |                  resp.proto | 'HTTP/1.1'                      |                     |                                         | 
     |                 >    | |                 resp.reason | 'OK'                            |                     |                                         | 
     |                 >    | |                 resp.status | '200'                           |                     |                                         | 
     |                 >    | +-----------------------------+---------------------------------+---------------------+-----------------------------------------+
  
  
  ************************************************************
  *                          Event                           *
  ************************************************************
  
  ########################################
  #                Start                 #
  ########################################
  #              VXID:34478              #
  ########################################
     |       Timestamp | Start: 2015/06/27 17:26:06.837718 GMT (last +0.000000s)
     |       Timestamp | Req: 2015/06/27 17:26:06.837718 GMT (last +0.000000s)
     | 
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  >               vcl_recv               >
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 | 
     |          return | pass
     | 
     | 
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  >               vcl_hash               >
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 | 
     |          return | lookup
     | 
     | 
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  >               vcl_pass               >
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 | 
     |          return | fetch
     | 
     |                 | 
     |            Link | bereq 34479 pass
     |                 > ########################################
     |                 > #              VXID:34479              #
     |                 > ########################################
     |                 >    |       Timestamp | Start: 2015/06/27 17:26:06.837826 GMT (last +0.000000s)
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >          vcl_backend_fetch           >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 | 
     |                 >    |          return | fetch
     |                 >    | 
     |                 >    |    BackendClose | 16 default(127.0.0.1,,88) toolate
     |                 >    |     BackendOpen | 16 default(127.0.0.1,,88) 127.0.0.1 36752 
     |                 >    |         Backend | 16 default default(127.0.0.1,,88)
     |                 >    |       Timestamp | Bereq: 2015/06/27 17:26:06.837955 GMT (last +0.000128s)
     |                 >    |       Timestamp | Beresp: 2015/06/27 17:26:06.838173 GMT (last +0.000218s)
     |                 >    |             TTL | RFC 120 -1 -1 1435425967 1435425967 1435425966 0 0
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >         vcl_backend_response         >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |             TTL | VCL 120 10 0 1435425967
     |                 >    |                 | 
     |                 >    |          return | deliver
     |                 >    | 
     |                 >    |         Storage | malloc Transient
     |                 >    |      Fetch_Body | 3 length -
     |                 >    |    BackendReuse | 16 default(127.0.0.1,,88)
     |                 >    |       Timestamp | BerespBody: 2015/06/27 17:26:06.838244 GMT (last +0.000071s)
     |                 >    |          Length | 287
     |                 >    |       BereqAcct | 164 0 164 285 287 572
     |       Timestamp | Fetch: 2015/06/27 17:26:06.838258 GMT (last +0.000541s)
     | 
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  >             vcl_deliver              >
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 | 
     |          return | deliver
     | 
     |       Timestamp | Process: 2015/06/27 17:26:06.838285 GMT (last +0.000027s)
     |           Debug | "RES_MODE 18"
     |                 | 
     |            Link | req 34480 esi
     |                 > ########################################
     |                 > #                 ESI                  #
     |                 > ########################################
     |                 > #              VXID:34480              #
     |                 > ########################################
     |                 >    |       Timestamp | Start: 2015/06/27 17:26:06.838316 GMT (last +0.000000s)
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >               vcl_recv               >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 | 
     |                 >    |          return | pass
     |                 >    | 
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >               vcl_hash               >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 | 
     |                 >    |          return | lookup
     |                 >    | 
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >               vcl_pass               >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 | 
     |                 >    |          return | fetch
     |                 >    | 
     |                 >    |                 | 
     |                 >    |            Link | bereq 34481 pass
     |                 >    |                 > ########################################
     |                 >    |                 > #              VXID:34481              #
     |                 >    |                 > ########################################
     |                 >    |                 >    |       Timestamp | Start: 2015/06/27 17:26:06.838346 GMT (last +0.000000s)
     |                 >    |                 >    | 
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 > >          vcl_backend_fetch           >
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 >    |                 | 
     |                 >    |                 >    |          return | fetch
     |                 >    |                 >    | 
     |                 >    |                 >    |         Backend | 16 default default(127.0.0.1,,88)
     |                 >    |                 >    |       Timestamp | Bereq: 2015/06/27 17:26:06.838387 GMT (last +0.000041s)
     |                 >    |                 >    |       Timestamp | Beresp: 2015/06/27 17:26:07.838981 GMT (last +1.000593s)
     |                 >    |                 >    |             TTL | RFC 120 -1 -1 1435425968 1435425968 1435425966 0 0
     |                 >    |                 >    | 
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 > >         vcl_backend_response         >
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 >    |             TTL | VCL 120 10 0 1435425968
     |                 >    |                 >    |                 | 
     |                 >    |                 >    |          return | deliver
     |                 >    |                 >    | 
     |                 >    |                 >    |         Storage | malloc Transient
     |                 >    |                 >    |      Fetch_Body | 3 length stream
     |                 >    |                 >    |    BackendReuse | 16 default(127.0.0.1,,88)
     |                 >    |                 >    |       Timestamp | BerespBody: 2015/06/27 17:26:07.839064 GMT (last +0.000083s)
     |                 >    |                 >    |          Length | 3
     |                 >    |                 >    |       BereqAcct | 164 0 164 193 3 196
     |                 >    |       Timestamp | Fetch: 2015/06/27 17:26:07.839078 GMT (last +1.000763s)
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >             vcl_deliver              >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 | 
     |                 >    |          return | deliver
     |                 >    | 
     |                 >    |       Timestamp | Process: 2015/06/27 17:26:07.839111 GMT (last +0.000032s)
     |                 >    |           Debug | "RES_MODE 28"
     |                 >    |       Timestamp | Resp: 2015/06/27 17:26:07.839139 GMT (last +0.000028s)
     |                 >    |           Debug | "XXX REF 1"
     |                 >    |   ESI_BodyBytes | 3
     |                 | 
     |            Link | req 34482 esi
     |                 > ########################################
     |                 > #                 ESI                  #
     |                 > ########################################
     |                 > #              VXID:34482              #
     |                 > ########################################
     |                 >    |       Timestamp | Start: 2015/06/27 17:26:07.839205 GMT (last +0.000000s)
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >               vcl_recv               >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 | 
     |                 >    |          return | pass
     |                 >    | 
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >               vcl_hash               >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 | 
     |                 >    |          return | lookup
     |                 >    | 
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >               vcl_pass               >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 | 
     |                 >    |          return | fetch
     |                 >    | 
     |                 >    |                 | 
     |                 >    |            Link | bereq 34483 pass
     |                 >    |                 > ########################################
     |                 >    |                 > #              VXID:34483              #
     |                 >    |                 > ########################################
     |                 >    |                 >    |       Timestamp | Start: 2015/06/27 17:26:07.839273 GMT (last +0.000000s)
     |                 >    |                 >    | 
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 > >          vcl_backend_fetch           >
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 >    |                 | 
     |                 >    |                 >    |          return | fetch
     |                 >    |                 >    | 
     |                 >    |                 >    |         Backend | 16 default default(127.0.0.1,,88)
     |                 >    |                 >    |       Timestamp | Bereq: 2015/06/27 17:26:07.839332 GMT (last +0.000059s)
     |                 >    |                 >    |       Timestamp | Beresp: 2015/06/27 17:26:07.839624 GMT (last +0.000292s)
     |                 >    |                 >    |             TTL | RFC 120 -1 -1 1435425968 1435425968 1435425967 0 0
     |                 >    |                 >    | 
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 > >         vcl_backend_response         >
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 >    |             TTL | VCL 120 10 0 1435425968
     |                 >    |                 >    |                 | 
     |                 >    |                 >    |          return | deliver
     |                 >    |                 >    | 
     |                 >    |                 >    |         Storage | malloc Transient
     |                 >    |                 >    |      Fetch_Body | 3 length stream
     |                 >    |                 >    |    BackendReuse | 16 default(127.0.0.1,,88)
     |                 >    |                 >    |       Timestamp | BerespBody: 2015/06/27 17:26:07.839690 GMT (last +0.000066s)
     |                 >    |                 >    |          Length | 11
     |                 >    |                 >    |       BereqAcct | 162 0 162 256 11 267
     |                 >    |       Timestamp | Fetch: 2015/06/27 17:26:07.839721 GMT (last +0.000516s)
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >             vcl_deliver              >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 | 
     |                 >    |          return | deliver
     |                 >    | 
     |                 >    |       Timestamp | Process: 2015/06/27 17:26:07.839754 GMT (last +0.000033s)
     |                 >    |           Debug | "RES_MODE 28"
     |                 >    |       Timestamp | Resp: 2015/06/27 17:26:07.839784 GMT (last +0.000030s)
     |                 >    |           Debug | "XXX REF 1"
     |                 >    |   ESI_BodyBytes | 11
     |       Timestamp | Resp: 2015/06/27 17:26:07.839822 GMT (last +1.001536s)
     |           Debug | "XXX REF 1"
     |   ESI_BodyBytes | 227
     |         ReqAcct | 123 0 123 378 283 661
  ----------------------------------------------------------------------------------------------------


HISTORY
===========

Version 0.2: Fix parsing of HTTP header. Reopen VSM ,if Varnish restarted. (issue #2,3,4 thanks zstyblik)

Version 0.1: First version
