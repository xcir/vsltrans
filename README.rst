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

   *   << BeReq    >> 99766     
   -   Begin          bereq 99765 pass
   -   Timestamp      Start: 1435388300.471496 0.000000 0.000000
   -   BereqMethod    GET
   -   BereqURL       /
   -   BereqProtocol  HTTP/1.1
   -   BereqHeader    User-Agent: Wget/1.15 (linux-gnu)
   -   BereqHeader    Accept: */*
   -   BereqHeader    Host: 192.168.1.37:6081
   -   BereqHeader    X-Forwarded-For: 192.168.1.30
   -   BereqHeader    hogehoge: mage
   -   BereqHeader    X-Varnish: 99766
   -   VCL_call       BACKEND_FETCH
   -   VCL_return     fetch
   -   BackendClose   16 default(127.0.0.1,,88) toolate
   -   BackendOpen    16 default(127.0.0.1,,88) 127.0.0.1 36643 
   -   Backend        16 default default(127.0.0.1,,88)
   -   Timestamp      Bereq: 1435388300.471642 0.000146 0.000146
   -   Timestamp      Beresp: 1435388300.472332 0.000835 0.000690
   -   BerespProtocol HTTP/1.1
   -   BerespStatus   200
   -   BerespReason   OK
   -   BerespHeader   Date: Sat, 27 Jun 2015 06:58:20 GMT
   -   BerespHeader   Server: Apache/2.2.22 (Ubuntu)
   -   BerespHeader   X-Powered-By: PHP/5.3.10-1ubuntu3.13
   -   BerespHeader   Vary: Accept-Encoding
   -   BerespHeader   Content-Length: 181
   -   BerespHeader   Content-Type: text/html
   -   TTL            RFC 120 -1 -1 1435388300 1435388300 1435388300 0 0
   -   VCL_call       BACKEND_RESPONSE
   -   TTL            VCL 120 10 0 1435388300
   -   VCL_return     deliver
   -   Storage        malloc Transient
   -   ObjProtocol    HTTP/1.1
   -   ObjStatus      200
   -   ObjReason      OK
   -   ObjHeader      Date: Sat, 27 Jun 2015 06:58:20 GMT
   -   ObjHeader      Server: Apache/2.2.22 (Ubuntu)
   -   ObjHeader      X-Powered-By: PHP/5.3.10-1ubuntu3.13
   -   ObjHeader      Vary: Accept-Encoding
   -   ObjHeader      Content-Length: 181
   -   ObjHeader      Content-Type: text/html
   -   Fetch_Body     3 length stream
   -   BackendReuse   16 default(127.0.0.1,,88)
   -   Timestamp      BerespBody: 1435388300.472384 0.000888 0.000053
   -   Length         181
   -   BereqAcct      156 0 156 195 181 376
   -   End            
   
   *   << Request  >> 99765     
   -   Begin          req 99764 rxreq
   -   Timestamp      Start: 1435388300.471404 0.000000 0.000000
   -   Timestamp      Req: 1435388300.471404 0.000000 0.000000
   -   ReqStart       192.168.1.30 43760
   -   ReqMethod      GET
   -   ReqURL         /
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
   -   Link           bereq 99766 pass
   -   Timestamp      Fetch: 1435388300.472398 0.000995 0.000995
   -   RespProtocol   HTTP/1.1
   -   RespStatus     200
   -   RespReason     OK
   -   RespHeader     Date: Sat, 27 Jun 2015 06:58:20 GMT
   -   RespHeader     Server: Apache/2.2.22 (Ubuntu)
   -   RespHeader     X-Powered-By: PHP/5.3.10-1ubuntu3.13
   -   RespHeader     Vary: Accept-Encoding
   -   RespHeader     Content-Length: 181
   -   RespHeader     Content-Type: text/html
   -   RespHeader     X-Varnish: 99765
   -   RespHeader     Age: 0
   -   RespHeader     Via: 1.1 varnish-v4
   -   VCL_call       DELIVER
   -   RespUnset      X-Powered-By: PHP/5.3.10-1ubuntu3.13
   -   RespHeader     x-powered-by: hoge
   -   RespUnset      x-powered-by: hoge
   -   ReqHeader      hoge: xxx
   -   RespHeader     restarts: 0
   -   VCL_return     restart
   -   Timestamp      Process: 1435388300.472427 0.001023 0.000029
   -   Timestamp      Restart: 1435388300.472433 0.001030 0.000006
   -   Link           req 99767 restart
   -   End            
   
   *   << BeReq    >> 99768     
   -   Begin          bereq 99767 pass
   -   Timestamp      Start: 1435388300.472488 0.000000 0.000000
   -   BereqMethod    GET
   -   BereqURL       /
   -   BereqProtocol  HTTP/1.1
   -   BereqHeader    User-Agent: Wget/1.15 (linux-gnu)
   -   BereqHeader    Accept: */*
   -   BereqHeader    Host: 192.168.1.37:6081
   -   BereqHeader    X-Forwarded-For: 192.168.1.30
   -   BereqHeader    hoge: xxx
   -   BereqHeader    hogehoge: mage
   -   BereqHeader    X-Varnish: 99768
   -   VCL_call       BACKEND_FETCH
   -   VCL_return     fetch
   -   Backend        16 default default(127.0.0.1,,88)
   -   Timestamp      Bereq: 1435388300.472528 0.000040 0.000040
   -   Timestamp      Beresp: 1435388300.472968 0.000480 0.000440
   -   BerespProtocol HTTP/1.1
   -   BerespStatus   200
   -   BerespReason   OK
   -   BerespHeader   Date: Sat, 27 Jun 2015 06:58:20 GMT
   -   BerespHeader   Server: Apache/2.2.22 (Ubuntu)
   -   BerespHeader   X-Powered-By: PHP/5.3.10-1ubuntu3.13
   -   BerespHeader   Vary: Accept-Encoding
   -   BerespHeader   Content-Length: 181
   -   BerespHeader   Content-Type: text/html
   -   TTL            RFC 120 -1 -1 1435388300 1435388300 1435388300 0 0
   -   VCL_call       BACKEND_RESPONSE
   -   TTL            VCL 120 10 0 1435388300
   -   VCL_return     deliver
   -   Storage        malloc Transient
   -   ObjProtocol    HTTP/1.1
   -   ObjStatus      200
   -   ObjReason      OK
   -   ObjHeader      Date: Sat, 27 Jun 2015 06:58:20 GMT
   -   ObjHeader      Server: Apache/2.2.22 (Ubuntu)
   -   ObjHeader      X-Powered-By: PHP/5.3.10-1ubuntu3.13
   -   ObjHeader      Vary: Accept-Encoding
   -   ObjHeader      Content-Length: 181
   -   ObjHeader      Content-Type: text/html
   -   Fetch_Body     3 length stream
   -   BackendReuse   16 default(127.0.0.1,,88)
   -   Timestamp      BerespBody: 1435388300.473005 0.000518 0.000037
   -   Length         181
   -   BereqAcct      167 0 167 195 181 376
   -   End            
   
   *   << Request  >> 99767     
   -   Begin          req 99765 restart
   -   Timestamp      Start: 1435388300.472433 0.001030 0.000000
   -   ReqStart       192.168.1.30 43760
   -   ReqMethod      GET
   -   ReqURL         /
   -   ReqProtocol    HTTP/1.1
   -   ReqHeader      User-Agent: Wget/1.15 (linux-gnu)
   -   ReqHeader      Accept: */*
   -   ReqHeader      Host: 192.168.1.37:6081
   -   ReqHeader      Connection: Keep-Alive
   -   ReqHeader      X-Forwarded-For: 192.168.1.30
   -   ReqHeader      hogehoge: mage
   -   ReqHeader      hoge: xxx
   -   VCL_call       RECV
   -   ReqUnset       hogehoge: mage
   -   ReqHeader      hogehoge: mage
   -   VCL_return     pass
   -   VCL_call       HASH
   -   VCL_return     lookup
   -   VCL_call       PASS
   -   VCL_return     fetch
   -   Link           bereq 99768 pass
   -   Timestamp      Fetch: 1435388300.473019 0.001616 0.000586
   -   RespProtocol   HTTP/1.1
   -   RespStatus     200
   -   RespReason     OK
   -   RespHeader     Date: Sat, 27 Jun 2015 06:58:20 GMT
   -   RespHeader     Server: Apache/2.2.22 (Ubuntu)
   -   RespHeader     X-Powered-By: PHP/5.3.10-1ubuntu3.13
   -   RespHeader     Vary: Accept-Encoding
   -   RespHeader     Content-Length: 181
   -   RespHeader     Content-Type: text/html
   -   RespHeader     X-Varnish: 99767
   -   RespHeader     Age: 0
   -   RespHeader     Via: 1.1 varnish-v4
   -   VCL_call       DELIVER
   -   RespUnset      X-Powered-By: PHP/5.3.10-1ubuntu3.13
   -   RespHeader     x-powered-by: hoge
   -   RespUnset      x-powered-by: hoge
   -   ReqUnset       hoge: xxx
   -   ReqHeader      hoge: xxx
   -   RespHeader     restarts: 1
   -   VCL_return     deliver
   -   Timestamp      Process: 1435388300.473040 0.001636 0.000021
   -   Debug          "RES_MODE 2"
   -   RespHeader     Connection: keep-alive
   -   RespHeader     Accept-Ranges: bytes
   -   Timestamp      Resp: 1435388300.473065 0.001662 0.000026
   -   Debug          "XXX REF 1"
   -   ReqAcct        115 0 115 263 181 444
   -   End            
  
   *   << Session  >> 99764     
   -   Begin          sess 0 HTTP/1
   -   SessOpen       192.168.1.30 43760 :6081 192.168.1.37 6081 1435388300.471356 15
   -   Link           req 99765 rxreq
   -   SessClose      REM_CLOSE 0.002
   -   End            

Re-formatted log(./vsltrans.py)
---------------------------------------------------
I'm thinking output format now...
::

   ############################################################
   #                        VXID:99765                        #
   ############################################################
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   >                         vcl_recv                         >
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      | +--------------------------+-------------------------+--------+------+
      | |                      key |          init           |  work  | fini | 
      | +--------------------------+-------------------------+--------+------+
      | |                client.ip | '192.168.1.30 43760'    |        |      | 
      | |          req.http.Accept | '*/*'                   |        |      | 
      | |      req.http.Connection | 'Keep-Alive'            |        |      | 
      | |            req.http.Host | '192.168.1.37:6081'     |        |      | 
      | |      req.http.User-Agent | 'Wget/1.15 (linux-gnu)' |        |      | 
      | | req.http.X-Forwarded-For | '192.168.1.30'          |        |      | 
      | |        req.http.hogehoge |                         | 'mage' |      | 
      | |               req.method | 'GET'                   |        |      | 
      | |                req.proto | 'HTTP/1.1'              |        |      | 
      | |                  req.url | '/'                     |        |      | 
      | +--------------------------+-------------------------+--------+------+
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
   <                     vcl_return(pass)                     <
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      | 
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   >                         vcl_hash                         >
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      | +------+------+------+------+
      | |  key | init | work | fini | 
      | +------+------+------+------+
      | +------+------+------+------+
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
   <                    vcl_return(lookup)                    <
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      | 
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   >                         vcl_pass                         >
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      | +------+------+------+------+
      | |  key | init | work | fini | 
      | +------+------+------+------+
      | +------+------+------+------+
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
   <                    vcl_return(fetch)                     <
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      | 
      |     > ############################################################
      |     > #                        VXID:99766                        #
      |     > ############################################################
      |     > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      |     > >                    vcl_backend_fetch                     >
      |     > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      |     >    | +----------------------------+-------------------------+------+------+
      |     >    | |                        key |          init           | work | fini | 
      |     >    | +----------------------------+-------------------------+------+------+
      |     >    | |          bereq.http.Accept | '*/*'                   |      |      | 
      |     >    | |            bereq.http.Host | '192.168.1.37:6081'     |      |      | 
      |     >    | |      bereq.http.User-Agent | 'Wget/1.15 (linux-gnu)' |      |      | 
      |     >    | | bereq.http.X-Forwarded-For | '192.168.1.30'          |      |      | 
      |     >    | |       bereq.http.X-Varnish | '99766'                 |      |      | 
      |     >    | |        bereq.http.hogehoge | 'mage'                  |      |      | 
      |     >    | |               bereq.method | 'GET'                   |      |      | 
      |     >    | |                bereq.proto | 'HTTP/1.1'              |      |      | 
      |     >    | |                  bereq.url | '/'                     |      |      | 
      |     >    | +----------------------------+-------------------------+------+------+
      |     > <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      |     > <                    vcl_return(fetch)                     <
      |     > <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      |     >    | 
      |     > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      |     > >                   vcl_backend_response                   >
      |     > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      |     >    | +----------------------------+---------------------------------+------+---------------------------------+
      |     >    | |                        key |              init               | work |              fini               | 
      |     >    | +----------------------------+---------------------------------+------+---------------------------------+
      |     >    | | beresp.http.Content-Length | '181'                           |      |                                 | 
      |     >    | |   beresp.http.Content-Type | 'text/html'                     |      |                                 | 
      |     >    | |           beresp.http.Date | 'Sat, 27 Jun 2015 06:58:20 GMT' |      |                                 | 
      |     >    | |         beresp.http.Server | 'Apache/2.2.22 (Ubuntu)'        |      |                                 | 
      |     >    | |           beresp.http.Vary | 'Accept-Encoding'               |      |                                 | 
      |     >    | |   beresp.http.X-Powered-By | 'PHP/5.3.10-1ubuntu3.13'        |      |                                 | 
      |     >    | |               beresp.proto | 'HTTP/1.1'                      |      |                                 | 
      |     >    | |              beresp.reason | 'OK'                            |      |                                 | 
      |     >    | |              beresp.status | '200'                           |      |                                 | 
      |     >    | |    obj.http.Content-Length |                                 |      | '181'                           | 
      |     >    | |      obj.http.Content-Type |                                 |      | 'text/html'                     | 
      |     >    | |              obj.http.Date |                                 |      | 'Sat, 27 Jun 2015 06:58:20 GMT' | 
      |     >    | |            obj.http.Server |                                 |      | 'Apache/2.2.22 (Ubuntu)'        | 
      |     >    | |              obj.http.Vary |                                 |      | 'Accept-Encoding'               | 
      |     >    | |      obj.http.X-Powered-By |                                 |      | 'PHP/5.3.10-1ubuntu3.13'        | 
      |     >    | |                  obj.proto |                                 |      | 'HTTP/1.1'                      | 
      |     >    | |                 obj.reason |                                 |      | 'OK'                            | 
      |     >    | |                 obj.status |                                 |      | '200'                           | 
      |     >    | +----------------------------+---------------------------------+------+---------------------------------+
      |     > <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      |     > <                   vcl_return(deliver)                    <
      |     > <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      |     >    | 
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   >                       vcl_deliver                        >
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      | +--------------------------+---------------------------------+-------------------+------+
      | |                      key |              init               |       work        | fini | 
      | +--------------------------+---------------------------------+-------------------+------+
      | |            req.http.hoge |                                 | 'xxx'             |      | 
      | |            resp.http.Age | '0'                             |                   |      | 
      | | resp.http.Content-Length | '181'                           |                   |      | 
      | |   resp.http.Content-Type | 'text/html'                     |                   |      | 
      | |           resp.http.Date | 'Sat, 27 Jun 2015 06:58:20 GMT' |                   |      | 
      | |         resp.http.Server | 'Apache/2.2.22 (Ubuntu)'        |                   |      | 
      | |           resp.http.Vary | 'Accept-Encoding'               |                   |      | 
      | |            resp.http.Via | '1.1 varnish-v4'                |                   |      | 
      | |   resp.http.X-Powered-By | 'PHP/5.3.10-1ubuntu3.13'        | [unset]           |      | 
      | |      resp.http.X-Varnish | '99765'                         |                   |      | 
      | |       resp.http.restarts |                                 | '0'               |      | 
      | |   resp.http.x-powered-by |                                 | 'hoge' -> [unset] |      | 
      | |               resp.proto | 'HTTP/1.1'                      |                   |      | 
      | |              resp.reason | 'OK'                            |                   |      | 
      | |              resp.status | '200'                           |                   |      | 
      | +--------------------------+---------------------------------+-------------------+------+
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
   <                   vcl_return(restart)                    <
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      | 
   ############################################################
   #                         RESTART                          #
   ############################################################
   ############################################################
   #                        VXID:99767                        #
   ############################################################
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   >                         vcl_recv                         >
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      | +--------------------------+-------------------------+-------------------+------+
      | |                      key |          init           |       work        | fini | 
      | +--------------------------+-------------------------+-------------------+------+
      | |                client.ip | '192.168.1.30 43760'    |                   |      | 
      | |          req.http.Accept | '*/*'                   |                   |      | 
      | |      req.http.Connection | 'Keep-Alive'            |                   |      | 
      | |            req.http.Host | '192.168.1.37:6081'     |                   |      | 
      | |      req.http.User-Agent | 'Wget/1.15 (linux-gnu)' |                   |      | 
      | | req.http.X-Forwarded-For | '192.168.1.30'          |                   |      | 
      | |            req.http.hoge | 'xxx'                   |                   |      | 
      | |        req.http.hogehoge | 'mage'                  | [unset] -> 'mage' |      | 
      | |               req.method | 'GET'                   |                   |      | 
      | |                req.proto | 'HTTP/1.1'              |                   |      | 
      | |                  req.url | '/'                     |                   |      | 
      | +--------------------------+-------------------------+-------------------+------+
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
   <                     vcl_return(pass)                     <
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      | 
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   >                         vcl_hash                         >
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      | +------+------+------+------+
      | |  key | init | work | fini | 
      | +------+------+------+------+
      | +------+------+------+------+
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
   <                    vcl_return(lookup)                    <
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      | 
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   >                         vcl_pass                         >
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      | +------+------+------+------+
      | |  key | init | work | fini | 
      | +------+------+------+------+
      | +------+------+------+------+
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
   <                    vcl_return(fetch)                     <
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      | 
      |     > ############################################################
      |     > #                        VXID:99768                        #
      |     > ############################################################
      |     > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      |     > >                    vcl_backend_fetch                     >
      |     > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      |     >    | +----------------------------+-------------------------+------+------+
      |     >    | |                        key |          init           | work | fini | 
      |     >    | +----------------------------+-------------------------+------+------+
      |     >    | |          bereq.http.Accept | '*/*'                   |      |      | 
      |     >    | |            bereq.http.Host | '192.168.1.37:6081'     |      |      | 
      |     >    | |      bereq.http.User-Agent | 'Wget/1.15 (linux-gnu)' |      |      | 
      |     >    | | bereq.http.X-Forwarded-For | '192.168.1.30'          |      |      | 
      |     >    | |       bereq.http.X-Varnish | '99768'                 |      |      | 
      |     >    | |            bereq.http.hoge | 'xxx'                   |      |      | 
      |     >    | |        bereq.http.hogehoge | 'mage'                  |      |      | 
      |     >    | |               bereq.method | 'GET'                   |      |      | 
      |     >    | |                bereq.proto | 'HTTP/1.1'              |      |      | 
      |     >    | |                  bereq.url | '/'                     |      |      | 
      |     >    | +----------------------------+-------------------------+------+------+
      |     > <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      |     > <                    vcl_return(fetch)                     <
      |     > <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      |     >    | 
      |     > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      |     > >                   vcl_backend_response                   >
      |     > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      |     >    | +----------------------------+---------------------------------+------+---------------------------------+
      |     >    | |                        key |              init               | work |              fini               | 
      |     >    | +----------------------------+---------------------------------+------+---------------------------------+
      |     >    | | beresp.http.Content-Length | '181'                           |      |                                 | 
      |     >    | |   beresp.http.Content-Type | 'text/html'                     |      |                                 | 
      |     >    | |           beresp.http.Date | 'Sat, 27 Jun 2015 06:58:20 GMT' |      |                                 | 
      |     >    | |         beresp.http.Server | 'Apache/2.2.22 (Ubuntu)'        |      |                                 | 
      |     >    | |           beresp.http.Vary | 'Accept-Encoding'               |      |                                 | 
      |     >    | |   beresp.http.X-Powered-By | 'PHP/5.3.10-1ubuntu3.13'        |      |                                 | 
      |     >    | |               beresp.proto | 'HTTP/1.1'                      |      |                                 | 
      |     >    | |              beresp.reason | 'OK'                            |      |                                 | 
      |     >    | |              beresp.status | '200'                           |      |                                 | 
      |     >    | |    obj.http.Content-Length |                                 |      | '181'                           | 
      |     >    | |      obj.http.Content-Type |                                 |      | 'text/html'                     | 
      |     >    | |              obj.http.Date |                                 |      | 'Sat, 27 Jun 2015 06:58:20 GMT' | 
      |     >    | |            obj.http.Server |                                 |      | 'Apache/2.2.22 (Ubuntu)'        | 
      |     >    | |              obj.http.Vary |                                 |      | 'Accept-Encoding'               | 
      |     >    | |      obj.http.X-Powered-By |                                 |      | 'PHP/5.3.10-1ubuntu3.13'        | 
      |     >    | |                  obj.proto |                                 |      | 'HTTP/1.1'                      | 
      |     >    | |                 obj.reason |                                 |      | 'OK'                            | 
      |     >    | |                 obj.status |                                 |      | '200'                           | 
      |     >    | +----------------------------+---------------------------------+------+---------------------------------+
      |     > <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      |     > <                   vcl_return(deliver)                    <
      |     > <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      |     >    | 
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   >                       vcl_deliver                        >
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      | +--------------------------+---------------------------------+-------------------+--------------+
      | |                      key |              init               |       work        |     fini     | 
      | +--------------------------+---------------------------------+-------------------+--------------+
      | |            req.http.hoge |                                 | [unset] -> 'xxx'  |              | 
      | |  resp.http.Accept-Ranges |                                 |                   | 'bytes'      | 
      | |            resp.http.Age | '0'                             |                   |              | 
      | |     resp.http.Connection |                                 |                   | 'keep-alive' | 
      | | resp.http.Content-Length | '181'                           |                   |              | 
      | |   resp.http.Content-Type | 'text/html'                     |                   |              | 
      | |           resp.http.Date | 'Sat, 27 Jun 2015 06:58:20 GMT' |                   |              | 
      | |         resp.http.Server | 'Apache/2.2.22 (Ubuntu)'        |                   |              | 
      | |           resp.http.Vary | 'Accept-Encoding'               |                   |              | 
      | |            resp.http.Via | '1.1 varnish-v4'                |                   |              | 
      | |   resp.http.X-Powered-By | 'PHP/5.3.10-1ubuntu3.13'        | [unset]           |              | 
      | |      resp.http.X-Varnish | '99767'                         |                   |              | 
      | |       resp.http.restarts |                                 | '1'               |              | 
      | |   resp.http.x-powered-by |                                 | 'hoge' -> [unset] |              | 
      | |               resp.proto | 'HTTP/1.1'                      |                   |              | 
      | |              resp.reason | 'OK'                            |                   |              | 
      | |              resp.status | '200'                           |                   |              | 
      | +--------------------------+---------------------------------+-------------------+--------------+
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
   <                   vcl_return(deliver)                    <
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      | 
  
  
   ############################################################
   #                        VXID:99765                        #
   ############################################################
      | Timestamp | Start: 1435388300.471404 0.000000 0.000000
      | Timestamp | Req: 1435388300.471404 0.000000 0.000000
      |      call | RECV
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   >                         vcl_recv                         >
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      |    return | pass
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
   <                     vcl_return(pass)                     <
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      | 
      |   call | HASH
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   >                         vcl_hash                         >
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      | return | lookup
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
   <                    vcl_return(lookup)                    <
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      | 
      |   call | PASS
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   >                         vcl_pass                         >
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      | return | fetch
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
   <                    vcl_return(fetch)                     <
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      | 
      |      Link | bereq 99766 pass
      |           > ############################################################
      |           > #                        VXID:99766                        #
      |           > ############################################################
      |           >    | Timestamp | Start: 1435388300.471496 0.000000 0.000000
      |           >    |      call | BACKEND_FETCH
      |           > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      |           > >                    vcl_backend_fetch                     >
      |           > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      |           >    |    return | fetch
      |           > <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      |           > <                    vcl_return(fetch)                     <
      |           > <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      |           >    | 
      |           >    | BackendClose | 16 default(127.0.0.1,,88) toolate
      |           >    |  BackendOpen | 16 default(127.0.0.1,,88) 127.0.0.1 36643 
      |           >    |      Backend | 16 default default(127.0.0.1,,88)
      |           >    |    Timestamp | Bereq: 1435388300.471642 0.000146 0.000146
      |           >    |    Timestamp | Beresp: 1435388300.472332 0.000835 0.000690
      |           >    |          TTL | RFC 120 -1 -1 1435388300 1435388300 1435388300 0 0
      |           >    |         call | BACKEND_RESPONSE
      |           > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      |           > >                   vcl_backend_response                   >
      |           > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      |           >    |          TTL | VCL 120 10 0 1435388300
      |           >    |       return | deliver
      |           > <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      |           > <                   vcl_return(deliver)                    <
      |           > <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      |           >    | 
      |           >    |      Storage | malloc Transient
      |           >    |   Fetch_Body | 3 length stream
      |           >    | BackendReuse | 16 default(127.0.0.1,,88)
      |           >    |    Timestamp | BerespBody: 1435388300.472384 0.000888 0.000053
      |           >    |       Length | 181
      |           >    |    BereqAcct | 156 0 156 195 181 376
      | Timestamp | Fetch: 1435388300.472398 0.000995 0.000995
      |      call | DELIVER
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   >                       vcl_deliver                        >
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      |    return | restart
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
   <                   vcl_return(restart)                    <
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      | 
      | Timestamp | Process: 1435388300.472427 0.001023 0.000029
      | Timestamp | Restart: 1435388300.472433 0.001030 0.000006
      |      Link | req 99767 restart
   ############################################################
   #                         RESTART                          #
   ############################################################
   ############################################################
   #                        VXID:99767                        #
   ############################################################
      | Timestamp | Start: 1435388300.472433 0.001030 0.000000
      |      call | RECV
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   >                         vcl_recv                         >
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      |    return | pass
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
   <                     vcl_return(pass)                     <
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      | 
      |   call | HASH
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   >                         vcl_hash                         >
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      | return | lookup
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
   <                    vcl_return(lookup)                    <
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      | 
      |   call | PASS
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   >                         vcl_pass                         >
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      | return | fetch
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
   <                    vcl_return(fetch)                     <
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      | 
      |      Link | bereq 99768 pass
      |           > ############################################################
      |           > #                        VXID:99768                        #
      |           > ############################################################
      |           >    | Timestamp | Start: 1435388300.472488 0.000000 0.000000
      |           >    |      call | BACKEND_FETCH
      |           > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      |           > >                    vcl_backend_fetch                     >
      |           > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      |           >    |    return | fetch
      |           > <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      |           > <                    vcl_return(fetch)                     <
      |           > <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      |           >    | 
      |           >    |      Backend | 16 default default(127.0.0.1,,88)
      |           >    |    Timestamp | Bereq: 1435388300.472528 0.000040 0.000040
      |           >    |    Timestamp | Beresp: 1435388300.472968 0.000480 0.000440
      |           >    |          TTL | RFC 120 -1 -1 1435388300 1435388300 1435388300 0 0
      |           >    |         call | BACKEND_RESPONSE
      |           > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      |           > >                   vcl_backend_response                   >
      |           > >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      |           >    |          TTL | VCL 120 10 0 1435388300
      |           >    |       return | deliver
      |           > <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      |           > <                   vcl_return(deliver)                    <
      |           > <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      |           >    | 
      |           >    |      Storage | malloc Transient
      |           >    |   Fetch_Body | 3 length stream
      |           >    | BackendReuse | 16 default(127.0.0.1,,88)
      |           >    |    Timestamp | BerespBody: 1435388300.473005 0.000518 0.000037
      |           >    |       Length | 181
      |           >    |    BereqAcct | 167 0 167 195 181 376
      | Timestamp | Fetch: 1435388300.473019 0.001616 0.000586
      |      call | DELIVER
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
   >                       vcl_deliver                        >
   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      |    return | deliver
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
   <                   vcl_return(deliver)                    <
   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
      | 
      | Timestamp | Process: 1435388300.473040 0.001636 0.000021
      |     Debug | RES_MODE 2 
      | Timestamp | Resp: 1435388300.473065 0.001662 0.000026
      |     Debug | XXX REF 1 
      |   ReqAcct | 115 0 115 263 181 444
   ----------------------------------------------------------------------------------------------------




HISTORY
===========

Version 0.2: Fix parsing of HTTP header. Reopen VSM ,if Varnish restarted. (issue #2,3,4 thanks zstyblik)

Version 0.1: First version
