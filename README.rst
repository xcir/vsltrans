==============
vsltrans
==============


-----------------------------------
Re-format tool for vsl(varnishlog)
-----------------------------------

:Author: Shohei Tanaka(@xcir)
:Date: 2015-06-27
:Version: alpha1-varnish40
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

include some bugs.

HOW TO USE
===========


Original log
---------------------------------------
::

  *   << BeReq    >> 34318     
  -   Begin          bereq 34317 pass
  -   Timestamp      Start: 1435404245.847174 0.000000 0.000000
  -   BereqMethod    GET
  -   BereqURL       /esi.html
  -   BereqProtocol  HTTP/1.1
  -   BereqHeader    User-Agent: Wget/1.15 (linux-gnu)
  -   BereqHeader    Accept: */*
  -   BereqHeader    Host: 192.168.1.37:6081
  -   BereqHeader    X-Forwarded-For: 192.168.1.30
  -   BereqHeader    hogehoge: mage
  -   BereqHeader    X-Varnish: 34318
  -   VCL_call       BACKEND_FETCH
  -   VCL_return     fetch
  -   BackendClose   16 default(127.0.0.1,,88) toolate
  -   BackendOpen    16 default(127.0.0.1,,88) 127.0.0.1 36706 
  -   Backend        16 default default(127.0.0.1,,88)
  -   Timestamp      Bereq: 1435404245.847331 0.000157 0.000157
  -   Timestamp      Beresp: 1435404245.847563 0.000390 0.000232
  -   BerespProtocol HTTP/1.1
  -   BerespStatus   200
  -   BerespReason   OK
  -   BerespHeader   Date: Sat, 27 Jun 2015 11:24:05 GMT
  -   BerespHeader   Server: Apache/2.2.22 (Ubuntu)
  -   BerespHeader   Last-Modified: Sat, 27 Jun 2015 08:17:33 GMT
  -   BerespHeader   ETag: "281399-11f-5197b7d0b403a"
  -   BerespHeader   Accept-Ranges: bytes
  -   BerespHeader   Content-Length: 287
  -   BerespHeader   Vary: Accept-Encoding
  -   BerespHeader   Content-Type: text/html
  -   BerespHeader   X-Pad: avoid browser bug
  -   TTL            RFC 120 -1 -1 1435404246 1435404246 1435404245 0 0
  -   VCL_call       BACKEND_RESPONSE
  -   TTL            VCL 120 10 0 1435404246
  -   VCL_return     deliver
  -   Storage        malloc Transient
  -   ObjProtocol    HTTP/1.1
  -   ObjStatus      200
  -   ObjReason      OK
  -   ObjHeader      Date: Sat, 27 Jun 2015 11:24:05 GMT
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
  -   Timestamp      BerespBody: 1435404245.847638 0.000465 0.000075
  -   Length         287
  -   BereqAcct      164 0 164 285 287 572
  -   End            
  
  *   << BeReq    >> 34320     
  -   Begin          bereq 34319 pass
  -   Timestamp      Start: 1435404245.847755 0.000000 0.000000
  -   BereqMethod    GET
  -   BereqURL       /slow.php
  -   BereqProtocol  HTTP/1.1
  -   BereqHeader    User-Agent: Wget/1.15 (linux-gnu)
  -   BereqHeader    Accept: */*
  -   BereqHeader    Host: 192.168.1.37:6081
  -   BereqHeader    X-Forwarded-For: 192.168.1.30
  -   BereqHeader    hogehoge: mage
  -   BereqHeader    X-Varnish: 34320
  -   VCL_call       BACKEND_FETCH
  -   VCL_return     fetch
  -   Backend        16 default default(127.0.0.1,,88)
  -   Timestamp      Bereq: 1435404245.847795 0.000040 0.000040
  -   Timestamp      Beresp: 1435404246.848411 1.000656 1.000616
  -   BerespProtocol HTTP/1.1
  -   BerespStatus   200
  -   BerespReason   OK
  -   BerespHeader   Date: Sat, 27 Jun 2015 11:24:05 GMT
  -   BerespHeader   Server: Apache/2.2.22 (Ubuntu)
  -   BerespHeader   X-Powered-By: PHP/5.3.10-1ubuntu3.13
  -   BerespHeader   Vary: Accept-Encoding
  -   BerespHeader   Content-Length: 3
  -   BerespHeader   Content-Type: text/html
  -   TTL            RFC 120 -1 -1 1435404247 1435404247 1435404245 0 0
  -   VCL_call       BACKEND_RESPONSE
  -   TTL            VCL 120 10 0 1435404247
  -   VCL_return     deliver
  -   Storage        malloc Transient
  -   ObjProtocol    HTTP/1.1
  -   ObjStatus      200
  -   ObjReason      OK
  -   ObjHeader      Date: Sat, 27 Jun 2015 11:24:05 GMT
  -   ObjHeader      Server: Apache/2.2.22 (Ubuntu)
  -   ObjHeader      X-Powered-By: PHP/5.3.10-1ubuntu3.13
  -   ObjHeader      Vary: Accept-Encoding
  -   ObjHeader      Content-Length: 3
  -   ObjHeader      Content-Type: text/html
  -   Fetch_Body     3 length stream
  -   BackendReuse   16 default(127.0.0.1,,88)
  -   Timestamp      BerespBody: 1435404246.848501 1.000746 0.000090
  -   Length         3
  -   BereqAcct      164 0 164 193 3 196
  -   End            
  
  *   << Request  >> 34319     
  -   Begin          req 34317 esi
  -   Timestamp      Start: 1435404245.847712 0.000000 0.000000
  -   ReqStart       192.168.1.30 43807
  -   VCL_call       RECV
  -   VCL_return     pass
  -   VCL_call       HASH
  -   VCL_return     lookup
  -   VCL_call       PASS
  -   VCL_return     fetch
  -   Link           bereq 34320 pass
  -   Timestamp      Fetch: 1435404246.848492 1.000780 1.000780
  -   RespProtocol   HTTP/1.1
  -   RespStatus     200
  -   RespReason     OK
  -   RespHeader     Date: Sat, 27 Jun 2015 11:24:05 GMT
  -   RespHeader     Server: Apache/2.2.22 (Ubuntu)
  -   RespHeader     X-Powered-By: PHP/5.3.10-1ubuntu3.13
  -   RespHeader     Vary: Accept-Encoding
  -   RespHeader     Content-Length: 3
  -   RespHeader     Content-Type: text/html
  -   RespHeader     X-Varnish: 34319
  -   RespHeader     Age: 0
  -   RespHeader     Via: 1.1 varnish-v4
  -   VCL_call       DELIVER
  -   RespUnset      X-Powered-By: PHP/5.3.10-1ubuntu3.13
  -   RespHeader     x-powered-by: hoge
  -   RespUnset      x-powered-by: hoge
  -   RespHeader     restarts: 0
  -   VCL_return     deliver
  -   Timestamp      Process: 1435404246.848513 1.000801 0.000021
  -   RespUnset      Content-Length: 3
  -   RespHeader     Transfer-Encoding: chunked
  -   Debug          "RES_MODE 28"
  -   RespHeader     Connection: keep-alive
  -   Timestamp      Resp: 1435404246.848542 1.000830 0.000029
  -   Debug          "XXX REF 1"
  -   ESI_BodyBytes  3
  -   End            
  
  *   << BeReq    >> 34322     
  -   Begin          bereq 34321 pass
  -   Timestamp      Start: 1435404246.848638 0.000000 0.000000
  -   BereqMethod    GET
  -   BereqURL       /x.html
  -   BereqProtocol  HTTP/1.1
  -   BereqHeader    User-Agent: Wget/1.15 (linux-gnu)
  -   BereqHeader    Accept: */*
  -   BereqHeader    Host: 192.168.1.37:6081
  -   BereqHeader    X-Forwarded-For: 192.168.1.30
  -   BereqHeader    hogehoge: mage
  -   BereqHeader    X-Varnish: 34322
  -   VCL_call       BACKEND_FETCH
  -   VCL_return     fetch
  -   Backend        16 default default(127.0.0.1,,88)
  -   Timestamp      Bereq: 1435404246.848698 0.000060 0.000060
  -   Timestamp      Beresp: 1435404246.848876 0.000238 0.000178
  -   BerespProtocol HTTP/1.1
  -   BerespStatus   200
  -   BerespReason   OK
  -   BerespHeader   Date: Sat, 27 Jun 2015 11:24:06 GMT
  -   BerespHeader   Server: Apache/2.2.22 (Ubuntu)
  -   BerespHeader   Last-Modified: Wed, 18 Feb 2015 16:43:37 GMT
  -   BerespHeader   ETag: "280ea4-b-50f5f855c1b9e"
  -   BerespHeader   Accept-Ranges: bytes
  -   BerespHeader   Content-Length: 11
  -   BerespHeader   Vary: Accept-Encoding
  -   BerespHeader   Content-Type: text/html
  -   TTL            RFC 120 -1 -1 1435404247 1435404247 1435404246 0 0
  -   VCL_call       BACKEND_RESPONSE
  -   TTL            VCL 120 10 0 1435404247
  -   VCL_return     deliver
  -   Storage        malloc Transient
  -   ObjProtocol    HTTP/1.1
  -   ObjStatus      200
  -   ObjReason      OK
  -   ObjHeader      Date: Sat, 27 Jun 2015 11:24:06 GMT
  -   ObjHeader      Server: Apache/2.2.22 (Ubuntu)
  -   ObjHeader      Last-Modified: Wed, 18 Feb 2015 16:43:37 GMT
  -   ObjHeader      ETag: "280ea4-b-50f5f855c1b9e"
  -   ObjHeader      Accept-Ranges: bytes
  -   ObjHeader      Content-Length: 11
  -   ObjHeader      Vary: Accept-Encoding
  -   ObjHeader      Content-Type: text/html
  -   Fetch_Body     3 length stream
  -   BackendReuse   16 default(127.0.0.1,,88)
  -   Timestamp      BerespBody: 1435404246.848939 0.000301 0.000062
  -   Length         11
  -   BereqAcct      162 0 162 256 11 267
  -   End            
  
  *   << Request  >> 34321     
  -   Begin          req 34317 esi
  -   Timestamp      Start: 1435404246.848573 0.000000 0.000000
  -   ReqStart       192.168.1.30 43807
  -   VCL_call       RECV
  -   VCL_return     pass
  -   VCL_call       HASH
  -   VCL_return     lookup
  -   VCL_call       PASS
  -   VCL_return     fetch
  -   Link           bereq 34322 pass
  -   Timestamp      Fetch: 1435404246.848953 0.000380 0.000380
  -   RespProtocol   HTTP/1.1
  -   RespStatus     200
  -   RespReason     OK
  -   RespHeader     Date: Sat, 27 Jun 2015 11:24:06 GMT
  -   RespHeader     Server: Apache/2.2.22 (Ubuntu)
  -   RespHeader     Last-Modified: Wed, 18 Feb 2015 16:43:37 GMT
  -   RespHeader     ETag: "280ea4-b-50f5f855c1b9e"
  -   RespHeader     Accept-Ranges: bytes
  -   RespHeader     Content-Length: 11
  -   RespHeader     Vary: Accept-Encoding
  -   RespHeader     Content-Type: text/html
  -   RespHeader     X-Varnish: 34321
  -   RespHeader     Age: 0
  -   RespHeader     Via: 1.1 varnish-v4
  -   VCL_call       DELIVER
  -   RespHeader     x-powered-by: hoge
  -   RespUnset      x-powered-by: hoge
  -   RespHeader     restarts: 0
  -   VCL_return     deliver
  -   Timestamp      Process: 1435404246.848978 0.000405 0.000025
  -   RespUnset      Content-Length: 11
  -   RespUnset      ETag: "280ea4-b-50f5f855c1b9e"
  -   RespHeader     ETag: W/"280ea4-b-50f5f855c1b9e"
  -   RespHeader     Transfer-Encoding: chunked
  -   Debug          "RES_MODE 28"
  -   RespHeader     Connection: keep-alive
  -   Timestamp      Resp: 1435404246.849002 0.000429 0.000024
  -   Debug          "XXX REF 1"
  -   ESI_BodyBytes  11
  -   End            
  
  *   << Request  >> 34317     
  -   Begin          req 34316 rxreq
  -   Timestamp      Start: 1435404245.847098 0.000000 0.000000
  -   Timestamp      Req: 1435404245.847098 0.000000 0.000000
  -   ReqStart       192.168.1.30 43807
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
  -   Link           bereq 34318 pass
  -   Timestamp      Fetch: 1435404245.847655 0.000557 0.000557
  -   RespProtocol   HTTP/1.1
  -   RespStatus     200
  -   RespReason     OK
  -   RespHeader     Date: Sat, 27 Jun 2015 11:24:05 GMT
  -   RespHeader     Server: Apache/2.2.22 (Ubuntu)
  -   RespHeader     Last-Modified: Sat, 27 Jun 2015 08:17:33 GMT
  -   RespHeader     ETag: "281399-11f-5197b7d0b403a"
  -   RespHeader     Accept-Ranges: bytes
  -   RespHeader     Content-Length: 287
  -   RespHeader     Vary: Accept-Encoding
  -   RespHeader     Content-Type: text/html
  -   RespHeader     X-Pad: avoid browser bug
  -   RespHeader     X-Varnish: 34317
  -   RespHeader     Age: 0
  -   RespHeader     Via: 1.1 varnish-v4
  -   VCL_call       DELIVER
  -   RespHeader     x-powered-by: hoge
  -   RespUnset      x-powered-by: hoge
  -   ReqHeader      hoge: xxx
  -   RespHeader     restarts: 0
  -   VCL_return     deliver
  -   Timestamp      Process: 1435404245.847682 0.000584 0.000027
  -   RespUnset      Content-Length: 287
  -   RespUnset      ETag: "281399-11f-5197b7d0b403a"
  -   RespHeader     ETag: W/"281399-11f-5197b7d0b403a"
  -   RespHeader     Transfer-Encoding: chunked
  -   Debug          "RES_MODE 18"
  -   RespHeader     Connection: keep-alive
  -   Link           req 34319 esi
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
  -   Link           req 34321 esi
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
  -   Timestamp      Resp: 1435404246.849052 1.001954 1.001369
  -   Debug          "XXX REF 1"
  -   ESI_BodyBytes  227
  -   ReqAcct        123 0 123 378 283 661
  -   End            
  
  *   << Session  >> 34316     
  -   Begin          sess 0 HTTP/1
  -   SessOpen       192.168.1.30 43807 :6081 192.168.1.37 6081 1435404245.847059 15
  -   Link           req 34317 rxreq
  -   SessClose      REM_CLOSE 1.003
  -   End            



Re-formatted log(./vsltrans.py)
---------------------------------------------------
I'm thinking output format now...
::

  ############################################################
  #                        VXID:34317                        #
  ############################################################
     | 
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  >                         vcl_recv                         >
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     | 
     | +--------------------------+-------------------------+--------+------+
     | |                      key |          init           |  work  | fini | 
     | +--------------------------+-------------------------+--------+------+
     | |                client.ip | '192.168.1.30 43807'    |        |      | 
     | |          req.http.Accept | '*/*'                   |        |      | 
     | |      req.http.Connection | 'Keep-Alive'            |        |      | 
     | |            req.http.Host | '192.168.1.37:6081'     |        |      | 
     | |      req.http.User-Agent | 'Wget/1.15 (linux-gnu)' |        |      | 
     | | req.http.X-Forwarded-For | '192.168.1.30'          |        |      | 
     | |        req.http.hogehoge |                         | 'mage' |      | 
     | |               req.method | 'GET'                   |        |      | 
     | |                req.proto | 'HTTP/1.1'              |        |      | 
     | |                  req.url | '/esi.html'             |        |      | 
     | +--------------------------+-------------------------+--------+------+
     | 
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  >                         vcl_hash                         >
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     | 
     | +------+------+------+------+
     | |  key | init | work | fini | 
     | +------+------+------+------+
     | +------+------+------+------+
     | 
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  >                         vcl_pass                         >
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     | 
     | +------+------+------+------+
     | |  key | init | work | fini | 
     | +------+------+------+------+
     | +------+------+------+------+
     |                 | 
     |                 > ############################################################
     |                 > #                        VXID:34318                        #
     |                 > ############################################################
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >                    vcl_backend_fetch                     >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    | 
     |                 >    | +----------------------------+-------------------------+------+------+
     |                 >    | |                        key |          init           | work | fini | 
     |                 >    | +----------------------------+-------------------------+------+------+
     |                 >    | |          bereq.http.Accept | '*/*'                   |      |      | 
     |                 >    | |            bereq.http.Host | '192.168.1.37:6081'     |      |      | 
     |                 >    | |      bereq.http.User-Agent | 'Wget/1.15 (linux-gnu)' |      |      | 
     |                 >    | | bereq.http.X-Forwarded-For | '192.168.1.30'          |      |      | 
     |                 >    | |       bereq.http.X-Varnish | '34318'                 |      |      | 
     |                 >    | |        bereq.http.hogehoge | 'mage'                  |      |      | 
     |                 >    | |               bereq.method | 'GET'                   |      |      | 
     |                 >    | |                bereq.proto | 'HTTP/1.1'              |      |      | 
     |                 >    | |                  bereq.url | '/esi.html'             |      |      | 
     |                 >    | +----------------------------+-------------------------+------+------+
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >                   vcl_backend_response                   >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    | 
     |                 >    | +----------------------------+---------------------------------+------+---------------------------------+
     |                 >    | |                        key |              init               | work |              fini               | 
     |                 >    | +----------------------------+---------------------------------+------+---------------------------------+
     |                 >    | |  beresp.http.Accept-Ranges | 'bytes'                         |      |                                 | 
     |                 >    | | beresp.http.Content-Length | '287'                           |      |                                 | 
     |                 >    | |   beresp.http.Content-Type | 'text/html'                     |      |                                 | 
     |                 >    | |           beresp.http.Date | 'Sat, 27 Jun 2015 11:24:05 GMT' |      |                                 | 
     |                 >    | |           beresp.http.ETag | '"281399-11f-5197b7d0b403a"'    |      |                                 | 
     |                 >    | |  beresp.http.Last-Modified | 'Sat, 27 Jun 2015 08:17:33 GMT' |      |                                 | 
     |                 >    | |         beresp.http.Server | 'Apache/2.2.22 (Ubuntu)'        |      |                                 | 
     |                 >    | |           beresp.http.Vary | 'Accept-Encoding'               |      |                                 | 
     |                 >    | |          beresp.http.X-Pad | 'avoid browser bug'             |      |                                 | 
     |                 >    | |               beresp.proto | 'HTTP/1.1'                      |      |                                 | 
     |                 >    | |              beresp.reason | 'OK'                            |      |                                 | 
     |                 >    | |              beresp.status | '200'                           |      |                                 | 
     |                 >    | |     obj.http.Accept-Ranges |                                 |      | 'bytes'                         | 
     |                 >    | |    obj.http.Content-Length |                                 |      | '287'                           | 
     |                 >    | |      obj.http.Content-Type |                                 |      | 'text/html'                     | 
     |                 >    | |              obj.http.Date |                                 |      | 'Sat, 27 Jun 2015 11:24:05 GMT' | 
     |                 >    | |              obj.http.ETag |                                 |      | '"281399-11f-5197b7d0b403a"'    | 
     |                 >    | |     obj.http.Last-Modified |                                 |      | 'Sat, 27 Jun 2015 08:17:33 GMT' | 
     |                 >    | |            obj.http.Server |                                 |      | 'Apache/2.2.22 (Ubuntu)'        | 
     |                 >    | |              obj.http.Vary |                                 |      | 'Accept-Encoding'               | 
     |                 >    | |             obj.http.X-Pad |                                 |      | 'avoid browser bug'             | 
     |                 >    | |                  obj.proto |                                 |      | 'HTTP/1.1'                      | 
     |                 >    | |                 obj.reason |                                 |      | 'OK'                            | 
     |                 >    | |                 obj.status |                                 |      | '200'                           | 
     |                 >    | +----------------------------+---------------------------------+------+---------------------------------+
     | 
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  >                       vcl_deliver                        >
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     | 
     | +-----------------------------+---------------------------------+-------------------+------------------------------------------------------+
     | |                         key |              init               |       work        |                         fini                         | 
     | +-----------------------------+---------------------------------+-------------------+------------------------------------------------------+
     | |             req.http.Accept |                                 |                   | '*/*' -> '*/*'                                       | 
     | |         req.http.Connection |                                 |                   | 'Keep-Alive' -> 'Keep-Alive'                         | 
     | |               req.http.Host |                                 |                   | '192.168.1.37:6081' -> '192.168.1.37:6081'           | 
     | |         req.http.User-Agent |                                 |                   | 'Wget/1.15 (linux-gnu)' -> 'Wget/1.15 (linux-gnu)'   | 
     | |    req.http.X-Forwarded-For |                                 |                   | '192.168.1.30' -> '192.168.1.30'                     | 
     | |               req.http.hoge |                                 | 'xxx'             | 'xxx' -> 'xxx'                                       | 
     | |           req.http.hogehoge |                                 |                   | 'mage' -> 'mage'                                     | 
     | |                  req.method |                                 |                   | 'GET' -> 'GET'                                       | 
     | |                   req.proto |                                 |                   | 'HTTP/1.1' -> 'HTTP/1.1'                             | 
     | |                     req.url |                                 |                   | '/slow.php' -> '/slow.php' -> '/x.html' -> '/x.html' | 
     | |     resp.http.Accept-Ranges | 'bytes'                         |                   |                                                      | 
     | |               resp.http.Age | '0'                             |                   |                                                      | 
     | |        resp.http.Connection |                                 |                   | 'keep-alive'                                         | 
     | |    resp.http.Content-Length | '287'                           |                   | [unset]                                              | 
     | |      resp.http.Content-Type | 'text/html'                     |                   |                                                      | 
     | |              resp.http.Date | 'Sat, 27 Jun 2015 11:24:05 GMT' |                   |                                                      | 
     | |              resp.http.ETag | '"281399-11f-5197b7d0b403a"'    |                   | [unset] -> 'W/"281399-11f-5197b7d0b403a"'            | 
     | |     resp.http.Last-Modified | 'Sat, 27 Jun 2015 08:17:33 GMT' |                   |                                                      | 
     | |            resp.http.Server | 'Apache/2.2.22 (Ubuntu)'        |                   |                                                      | 
     | | resp.http.Transfer-Encoding |                                 |                   | 'chunked'                                            | 
     | |              resp.http.Vary | 'Accept-Encoding'               |                   |                                                      | 
     | |               resp.http.Via | '1.1 varnish-v4'                |                   |                                                      | 
     | |             resp.http.X-Pad | 'avoid browser bug'             |                   |                                                      | 
     | |         resp.http.X-Varnish | '34317'                         |                   |                                                      | 
     | |          resp.http.restarts |                                 | '0'               |                                                      | 
     | |      resp.http.x-powered-by |                                 | 'hoge' -> [unset] |                                                      | 
     | |                  resp.proto | 'HTTP/1.1'                      |                   |                                                      | 
     | |                 resp.reason | 'OK'                            |                   |                                                      | 
     | |                 resp.status | '200'                           |                   |                                                      | 
     | +-----------------------------+---------------------------------+-------------------+------------------------------------------------------+
     |                 | 
     |                 > ############################################################
     |                 > #                           ESI                            #
     |                 > ############################################################
     |                 > #                        VXID:34319                        #
     |                 > ############################################################
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >                         vcl_recv                         >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    | 
     |                 >    | +-----------+----------------------+------+------+
     |                 >    | |       key |         init         | work | fini | 
     |                 >    | +-----------+----------------------+------+------+
     |                 >    | | client.ip | '192.168.1.30 43807' |      |      | 
     |                 >    | +-----------+----------------------+------+------+
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >                         vcl_hash                         >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    | 
     |                 >    | +------+------+------+------+
     |                 >    | |  key | init | work | fini | 
     |                 >    | +------+------+------+------+
     |                 >    | +------+------+------+------+
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >                         vcl_pass                         >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    | 
     |                 >    | +------+------+------+------+
     |                 >    | |  key | init | work | fini | 
     |                 >    | +------+------+------+------+
     |                 >    | +------+------+------+------+
     |                 >    |                 | 
     |                 >    |                 > ############################################################
     |                 >    |                 > #                        VXID:34320                        #
     |                 >    |                 > ############################################################
     |                 >    |                 >    | 
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 > >                    vcl_backend_fetch                     >
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 >    | 
     |                 >    |                 >    | +----------------------------+-------------------------+------+------+
     |                 >    |                 >    | |                        key |          init           | work | fini | 
     |                 >    |                 >    | +----------------------------+-------------------------+------+------+
     |                 >    |                 >    | |          bereq.http.Accept | '*/*'                   |      |      | 
     |                 >    |                 >    | |            bereq.http.Host | '192.168.1.37:6081'     |      |      | 
     |                 >    |                 >    | |      bereq.http.User-Agent | 'Wget/1.15 (linux-gnu)' |      |      | 
     |                 >    |                 >    | | bereq.http.X-Forwarded-For | '192.168.1.30'          |      |      | 
     |                 >    |                 >    | |       bereq.http.X-Varnish | '34320'                 |      |      | 
     |                 >    |                 >    | |        bereq.http.hogehoge | 'mage'                  |      |      | 
     |                 >    |                 >    | |               bereq.method | 'GET'                   |      |      | 
     |                 >    |                 >    | |                bereq.proto | 'HTTP/1.1'              |      |      | 
     |                 >    |                 >    | |                  bereq.url | '/slow.php'             |      |      | 
     |                 >    |                 >    | +----------------------------+-------------------------+------+------+
     |                 >    |                 >    | 
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 > >                   vcl_backend_response                   >
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 >    | 
     |                 >    |                 >    | +----------------------------+---------------------------------+------+---------------------------------+
     |                 >    |                 >    | |                        key |              init               | work |              fini               | 
     |                 >    |                 >    | +----------------------------+---------------------------------+------+---------------------------------+
     |                 >    |                 >    | | beresp.http.Content-Length | '3'                             |      |                                 | 
     |                 >    |                 >    | |   beresp.http.Content-Type | 'text/html'                     |      |                                 | 
     |                 >    |                 >    | |           beresp.http.Date | 'Sat, 27 Jun 2015 11:24:05 GMT' |      |                                 | 
     |                 >    |                 >    | |         beresp.http.Server | 'Apache/2.2.22 (Ubuntu)'        |      |                                 | 
     |                 >    |                 >    | |           beresp.http.Vary | 'Accept-Encoding'               |      |                                 | 
     |                 >    |                 >    | |   beresp.http.X-Powered-By | 'PHP/5.3.10-1ubuntu3.13'        |      |                                 | 
     |                 >    |                 >    | |               beresp.proto | 'HTTP/1.1'                      |      |                                 | 
     |                 >    |                 >    | |              beresp.reason | 'OK'                            |      |                                 | 
     |                 >    |                 >    | |              beresp.status | '200'                           |      |                                 | 
     |                 >    |                 >    | |    obj.http.Content-Length |                                 |      | '3'                             | 
     |                 >    |                 >    | |      obj.http.Content-Type |                                 |      | 'text/html'                     | 
     |                 >    |                 >    | |              obj.http.Date |                                 |      | 'Sat, 27 Jun 2015 11:24:05 GMT' | 
     |                 >    |                 >    | |            obj.http.Server |                                 |      | 'Apache/2.2.22 (Ubuntu)'        | 
     |                 >    |                 >    | |              obj.http.Vary |                                 |      | 'Accept-Encoding'               | 
     |                 >    |                 >    | |      obj.http.X-Powered-By |                                 |      | 'PHP/5.3.10-1ubuntu3.13'        | 
     |                 >    |                 >    | |                  obj.proto |                                 |      | 'HTTP/1.1'                      | 
     |                 >    |                 >    | |                 obj.reason |                                 |      | 'OK'                            | 
     |                 >    |                 >    | |                 obj.status |                                 |      | '200'                           | 
     |                 >    |                 >    | +----------------------------+---------------------------------+------+---------------------------------+
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >                       vcl_deliver                        >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    | 
     |                 >    | +-----------------------------+---------------------------------+-------------------+--------------+
     |                 >    | |                         key |              init               |       work        |     fini     | 
     |                 >    | +-----------------------------+---------------------------------+-------------------+--------------+
     |                 >    | |               resp.http.Age | '0'                             |                   |              | 
     |                 >    | |        resp.http.Connection |                                 |                   | 'keep-alive' | 
     |                 >    | |    resp.http.Content-Length | '3'                             |                   | [unset]      | 
     |                 >    | |      resp.http.Content-Type | 'text/html'                     |                   |              | 
     |                 >    | |              resp.http.Date | 'Sat, 27 Jun 2015 11:24:05 GMT' |                   |              | 
     |                 >    | |            resp.http.Server | 'Apache/2.2.22 (Ubuntu)'        |                   |              | 
     |                 >    | | resp.http.Transfer-Encoding |                                 |                   | 'chunked'    | 
     |                 >    | |              resp.http.Vary | 'Accept-Encoding'               |                   |              | 
     |                 >    | |               resp.http.Via | '1.1 varnish-v4'                |                   |              | 
     |                 >    | |      resp.http.X-Powered-By | 'PHP/5.3.10-1ubuntu3.13'        | [unset]           |              | 
     |                 >    | |         resp.http.X-Varnish | '34319'                         |                   |              | 
     |                 >    | |          resp.http.restarts |                                 | '0'               |              | 
     |                 >    | |      resp.http.x-powered-by |                                 | 'hoge' -> [unset] |              | 
     |                 >    | |                  resp.proto | 'HTTP/1.1'                      |                   |              | 
     |                 >    | |                 resp.reason | 'OK'                            |                   |              | 
     |                 >    | |                 resp.status | '200'                           |                   |              | 
     |                 >    | +-----------------------------+---------------------------------+-------------------+--------------+
     |                 | 
     |                 > ############################################################
     |                 > #                           ESI                            #
     |                 > ############################################################
     |                 > #                        VXID:34321                        #
     |                 > ############################################################
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >                         vcl_recv                         >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    | 
     |                 >    | +-----------+----------------------+------+------+
     |                 >    | |       key |         init         | work | fini | 
     |                 >    | +-----------+----------------------+------+------+
     |                 >    | | client.ip | '192.168.1.30 43807' |      |      | 
     |                 >    | +-----------+----------------------+------+------+
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >                         vcl_hash                         >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    | 
     |                 >    | +------+------+------+------+
     |                 >    | |  key | init | work | fini | 
     |                 >    | +------+------+------+------+
     |                 >    | +------+------+------+------+
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >                         vcl_pass                         >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    | 
     |                 >    | +------+------+------+------+
     |                 >    | |  key | init | work | fini | 
     |                 >    | +------+------+------+------+
     |                 >    | +------+------+------+------+
     |                 >    |                 | 
     |                 >    |                 > ############################################################
     |                 >    |                 > #                        VXID:34322                        #
     |                 >    |                 > ############################################################
     |                 >    |                 >    | 
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 > >                    vcl_backend_fetch                     >
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 >    | 
     |                 >    |                 >    | +----------------------------+-------------------------+------+------+
     |                 >    |                 >    | |                        key |          init           | work | fini | 
     |                 >    |                 >    | +----------------------------+-------------------------+------+------+
     |                 >    |                 >    | |          bereq.http.Accept | '*/*'                   |      |      | 
     |                 >    |                 >    | |            bereq.http.Host | '192.168.1.37:6081'     |      |      | 
     |                 >    |                 >    | |      bereq.http.User-Agent | 'Wget/1.15 (linux-gnu)' |      |      | 
     |                 >    |                 >    | | bereq.http.X-Forwarded-For | '192.168.1.30'          |      |      | 
     |                 >    |                 >    | |       bereq.http.X-Varnish | '34322'                 |      |      | 
     |                 >    |                 >    | |        bereq.http.hogehoge | 'mage'                  |      |      | 
     |                 >    |                 >    | |               bereq.method | 'GET'                   |      |      | 
     |                 >    |                 >    | |                bereq.proto | 'HTTP/1.1'              |      |      | 
     |                 >    |                 >    | |                  bereq.url | '/x.html'               |      |      | 
     |                 >    |                 >    | +----------------------------+-------------------------+------+------+
     |                 >    |                 >    | 
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 > >                   vcl_backend_response                   >
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 >    | 
     |                 >    |                 >    | +----------------------------+---------------------------------+------+---------------------------------+
     |                 >    |                 >    | |                        key |              init               | work |              fini               | 
     |                 >    |                 >    | +----------------------------+---------------------------------+------+---------------------------------+
     |                 >    |                 >    | |  beresp.http.Accept-Ranges | 'bytes'                         |      |                                 | 
     |                 >    |                 >    | | beresp.http.Content-Length | '11'                            |      |                                 | 
     |                 >    |                 >    | |   beresp.http.Content-Type | 'text/html'                     |      |                                 | 
     |                 >    |                 >    | |           beresp.http.Date | 'Sat, 27 Jun 2015 11:24:06 GMT' |      |                                 | 
     |                 >    |                 >    | |           beresp.http.ETag | '"280ea4-b-50f5f855c1b9e"'      |      |                                 | 
     |                 >    |                 >    | |  beresp.http.Last-Modified | 'Wed, 18 Feb 2015 16:43:37 GMT' |      |                                 | 
     |                 >    |                 >    | |         beresp.http.Server | 'Apache/2.2.22 (Ubuntu)'        |      |                                 | 
     |                 >    |                 >    | |           beresp.http.Vary | 'Accept-Encoding'               |      |                                 | 
     |                 >    |                 >    | |               beresp.proto | 'HTTP/1.1'                      |      |                                 | 
     |                 >    |                 >    | |              beresp.reason | 'OK'                            |      |                                 | 
     |                 >    |                 >    | |              beresp.status | '200'                           |      |                                 | 
     |                 >    |                 >    | |     obj.http.Accept-Ranges |                                 |      | 'bytes'                         | 
     |                 >    |                 >    | |    obj.http.Content-Length |                                 |      | '11'                            | 
     |                 >    |                 >    | |      obj.http.Content-Type |                                 |      | 'text/html'                     | 
     |                 >    |                 >    | |              obj.http.Date |                                 |      | 'Sat, 27 Jun 2015 11:24:06 GMT' | 
     |                 >    |                 >    | |              obj.http.ETag |                                 |      | '"280ea4-b-50f5f855c1b9e"'      | 
     |                 >    |                 >    | |     obj.http.Last-Modified |                                 |      | 'Wed, 18 Feb 2015 16:43:37 GMT' | 
     |                 >    |                 >    | |            obj.http.Server |                                 |      | 'Apache/2.2.22 (Ubuntu)'        | 
     |                 >    |                 >    | |              obj.http.Vary |                                 |      | 'Accept-Encoding'               | 
     |                 >    |                 >    | |                  obj.proto |                                 |      | 'HTTP/1.1'                      | 
     |                 >    |                 >    | |                 obj.reason |                                 |      | 'OK'                            | 
     |                 >    |                 >    | |                 obj.status |                                 |      | '200'                           | 
     |                 >    |                 >    | +----------------------------+---------------------------------+------+---------------------------------+
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >                       vcl_deliver                        >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    | 
     |                 >    | +-----------------------------+---------------------------------+-------------------+-----------------------------------------+
     |                 >    | |                         key |              init               |       work        |                  fini                   | 
     |                 >    | +-----------------------------+---------------------------------+-------------------+-----------------------------------------+
     |                 >    | |     resp.http.Accept-Ranges | 'bytes'                         |                   |                                         | 
     |                 >    | |               resp.http.Age | '0'                             |                   |                                         | 
     |                 >    | |        resp.http.Connection |                                 |                   | 'keep-alive'                            | 
     |                 >    | |    resp.http.Content-Length | '11'                            |                   | [unset]                                 | 
     |                 >    | |      resp.http.Content-Type | 'text/html'                     |                   |                                         | 
     |                 >    | |              resp.http.Date | 'Sat, 27 Jun 2015 11:24:06 GMT' |                   |                                         | 
     |                 >    | |              resp.http.ETag | '"280ea4-b-50f5f855c1b9e"'      |                   | [unset] -> 'W/"280ea4-b-50f5f855c1b9e"' | 
     |                 >    | |     resp.http.Last-Modified | 'Wed, 18 Feb 2015 16:43:37 GMT' |                   |                                         | 
     |                 >    | |            resp.http.Server | 'Apache/2.2.22 (Ubuntu)'        |                   |                                         | 
     |                 >    | | resp.http.Transfer-Encoding |                                 |                   | 'chunked'                               | 
     |                 >    | |              resp.http.Vary | 'Accept-Encoding'               |                   |                                         | 
     |                 >    | |               resp.http.Via | '1.1 varnish-v4'                |                   |                                         | 
     |                 >    | |         resp.http.X-Varnish | '34321'                         |                   |                                         | 
     |                 >    | |          resp.http.restarts |                                 | '0'               |                                         | 
     |                 >    | |      resp.http.x-powered-by |                                 | 'hoge' -> [unset] |                                         | 
     |                 >    | |                  resp.proto | 'HTTP/1.1'                      |                   |                                         | 
     |                 >    | |                 resp.reason | 'OK'                            |                   |                                         | 
     |                 >    | |                 resp.status | '200'                           |                   |                                         | 
     |                 >    | +-----------------------------+---------------------------------+-------------------+-----------------------------------------+
  
  
  ############################################################
  #                        VXID:34317                        #
  ############################################################
     |       Timestamp | Start: 1435404245.847098 0.000000 0.000000
     |       Timestamp | Req: 1435404245.847098 0.000000 0.000000
     | 
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  >                         vcl_recv                         >
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 | 
     |          return | pass
     | 
     | 
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  >                         vcl_hash                         >
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 | 
     |          return | lookup
     | 
     | 
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  >                         vcl_pass                         >
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 | 
     |          return | fetch
     | 
     |                 | 
     |            Link | bereq 34318 pass
     |                 > ############################################################
     |                 > #                        VXID:34318                        #
     |                 > ############################################################
     |                 >    |       Timestamp | Start: 1435404245.847174 0.000000 0.000000
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >                    vcl_backend_fetch                     >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 | 
     |                 >    |          return | fetch
     |                 >    | 
     |                 >    |    BackendClose | 16 default(127.0.0.1,,88) toolate
     |                 >    |     BackendOpen | 16 default(127.0.0.1,,88) 127.0.0.1 36706 
     |                 >    |         Backend | 16 default default(127.0.0.1,,88)
     |                 >    |       Timestamp | Bereq: 1435404245.847331 0.000157 0.000157
     |                 >    |       Timestamp | Beresp: 1435404245.847563 0.000390 0.000232
     |                 >    |             TTL | RFC 120 -1 -1 1435404246 1435404246 1435404245 0 0
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >                   vcl_backend_response                   >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |             TTL | VCL 120 10 0 1435404246
     |                 >    |                 | 
     |                 >    |          return | deliver
     |                 >    | 
     |                 >    |         Storage | malloc Transient
     |                 >    |      Fetch_Body | 3 length -
     |                 >    |    BackendReuse | 16 default(127.0.0.1,,88)
     |                 >    |       Timestamp | BerespBody: 1435404245.847638 0.000465 0.000075
     |                 >    |          Length | 287
     |                 >    |       BereqAcct | 164 0 164 285 287 572
     |       Timestamp | Fetch: 1435404245.847655 0.000557 0.000557
     | 
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  >                       vcl_deliver                        >
  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 | 
     |          return | deliver
     | 
     |       Timestamp | Process: 1435404245.847682 0.000584 0.000027
     |           Debug | RES_MODE 18 
     |                 | 
     |            Link | req 34319 esi
     |                 > ############################################################
     |                 > #                           ESI                            #
     |                 > ############################################################
     |                 > #                        VXID:34319                        #
     |                 > ############################################################
     |                 >    |       Timestamp | Start: 1435404245.847712 0.000000 0.000000
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >                         vcl_recv                         >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 | 
     |                 >    |          return | pass
     |                 >    | 
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >                         vcl_hash                         >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 | 
     |                 >    |          return | lookup
     |                 >    | 
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >                         vcl_pass                         >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 | 
     |                 >    |          return | fetch
     |                 >    | 
     |                 >    |                 | 
     |                 >    |            Link | bereq 34320 pass
     |                 >    |                 > ############################################################
     |                 >    |                 > #                        VXID:34320                        #
     |                 >    |                 > ############################################################
     |                 >    |                 >    |       Timestamp | Start: 1435404245.847755 0.000000 0.000000
     |                 >    |                 >    | 
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 > >                    vcl_backend_fetch                     >
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 >    |                 | 
     |                 >    |                 >    |          return | fetch
     |                 >    |                 >    | 
     |                 >    |                 >    |         Backend | 16 default default(127.0.0.1,,88)
     |                 >    |                 >    |       Timestamp | Bereq: 1435404245.847795 0.000040 0.000040
     |                 >    |                 >    |       Timestamp | Beresp: 1435404246.848411 1.000656 1.000616
     |                 >    |                 >    |             TTL | RFC 120 -1 -1 1435404247 1435404247 1435404245 0 0
     |                 >    |                 >    | 
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 > >                   vcl_backend_response                   >
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 >    |             TTL | VCL 120 10 0 1435404247
     |                 >    |                 >    |                 | 
     |                 >    |                 >    |          return | deliver
     |                 >    |                 >    | 
     |                 >    |                 >    |         Storage | malloc Transient
     |                 >    |                 >    |      Fetch_Body | 3 length stream
     |                 >    |                 >    |    BackendReuse | 16 default(127.0.0.1,,88)
     |                 >    |                 >    |       Timestamp | BerespBody: 1435404246.848501 1.000746 0.000090
     |                 >    |                 >    |          Length | 3
     |                 >    |                 >    |       BereqAcct | 164 0 164 193 3 196
     |                 >    |       Timestamp | Fetch: 1435404246.848492 1.000780 1.000780
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >                       vcl_deliver                        >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 | 
     |                 >    |          return | deliver
     |                 >    | 
     |                 >    |       Timestamp | Process: 1435404246.848513 1.000801 0.000021
     |                 >    |           Debug | RES_MODE 28 
     |                 >    |       Timestamp | Resp: 1435404246.848542 1.000830 0.000029
     |                 >    |           Debug | XXX REF 1 
     |                 >    |   ESI_BodyBytes | 3
     |                 | 
     |            Link | req 34321 esi
     |                 > ############################################################
     |                 > #                           ESI                            #
     |                 > ############################################################
     |                 > #                        VXID:34321                        #
     |                 > ############################################################
     |                 >    |       Timestamp | Start: 1435404246.848573 0.000000 0.000000
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >                         vcl_recv                         >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 | 
     |                 >    |          return | pass
     |                 >    | 
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >                         vcl_hash                         >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 | 
     |                 >    |          return | lookup
     |                 >    | 
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >                         vcl_pass                         >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 | 
     |                 >    |          return | fetch
     |                 >    | 
     |                 >    |                 | 
     |                 >    |            Link | bereq 34322 pass
     |                 >    |                 > ############################################################
     |                 >    |                 > #                        VXID:34322                        #
     |                 >    |                 > ############################################################
     |                 >    |                 >    |       Timestamp | Start: 1435404246.848638 0.000000 0.000000
     |                 >    |                 >    | 
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 > >                    vcl_backend_fetch                     >
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 >    |                 | 
     |                 >    |                 >    |          return | fetch
     |                 >    |                 >    | 
     |                 >    |                 >    |         Backend | 16 default default(127.0.0.1,,88)
     |                 >    |                 >    |       Timestamp | Bereq: 1435404246.848698 0.000060 0.000060
     |                 >    |                 >    |       Timestamp | Beresp: 1435404246.848876 0.000238 0.000178
     |                 >    |                 >    |             TTL | RFC 120 -1 -1 1435404247 1435404247 1435404246 0 0
     |                 >    |                 >    | 
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 > >                   vcl_backend_response                   >
     |                 >    |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 >    |             TTL | VCL 120 10 0 1435404247
     |                 >    |                 >    |                 | 
     |                 >    |                 >    |          return | deliver
     |                 >    |                 >    | 
     |                 >    |                 >    |         Storage | malloc Transient
     |                 >    |                 >    |      Fetch_Body | 3 length stream
     |                 >    |                 >    |    BackendReuse | 16 default(127.0.0.1,,88)
     |                 >    |                 >    |       Timestamp | BerespBody: 1435404246.848939 0.000301 0.000062
     |                 >    |                 >    |          Length | 11
     |                 >    |                 >    |       BereqAcct | 162 0 162 256 11 267
     |                 >    |       Timestamp | Fetch: 1435404246.848953 0.000380 0.000380
     |                 >    | 
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 > >                       vcl_deliver                        >
     |                 > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |                 >    |                 | 
     |                 >    |          return | deliver
     |                 >    | 
     |                 >    |       Timestamp | Process: 1435404246.848978 0.000405 0.000025
     |                 >    |           Debug | RES_MODE 28 
     |                 >    |       Timestamp | Resp: 1435404246.849002 0.000429 0.000024
     |                 >    |           Debug | XXX REF 1 
     |                 >    |   ESI_BodyBytes | 11
     |       Timestamp | Resp: 1435404246.849052 1.001954 1.001369
     |           Debug | XXX REF 1 
     |   ESI_BodyBytes | 227
     |         ReqAcct | 123 0 123 378 283 661
  ----------------------------------------------------------------------------------------------------






HISTORY
===========

Version 0.2: Fix parsing of HTTP header. Reopen VSM ,if Varnish restarted. (issue #2,3,4 thanks zstyblik)

Version 0.1: First version
