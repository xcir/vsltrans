# coding: utf-8

import ctypes


VSL_handler_f = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_char_p, ctypes.c_ulonglong)

class VSLUtil:
	tags     = {
		0:{
			"Debug"				:"",
			"Error"				:"",
			"CLI"				:"",
			"StatSess"			:"",
			"ReqEnd"			:"",
			"SessionOpen"		:"",
			"SessionClose"		:"",
			"BackendOpen"		:"",
			"BackendXID"		:"",
			"BackendReuse"		:"",
			"BackendClose"		:"",
			"HttpGarbage"		:"",
			"Backend"			:"",
			"Length"			:"",
			"FetchError"		:"",
			"RxRequest"			:"",
			"RxResponse"		:"",
			"RxStatus"			:"",
			"RxURL"				:"",
			"RxProtocol"		:"",
			"RxHeader"			:"",
			"TxRequest"			:"",
			"TxResponse"		:"",
			"TxStatus"			:"",
			"TxURL"				:"",
			"TxProtocol"		:"",
			"TxHeader"			:"",
			"ObjRequest"		:"",
			"ObjResponse"		:"",
			"ObjStatus"			:"",
			"ObjURL"			:"",
			"ObjProtocol"		:"",
			"ObjHeader"			:"",
			"LostHeader"		:"",
			"TTL"				:"",
			"Fetch_Body"		:"",
			"VCL_acl"			:"",
			"VCL_call"			:"",
			"VCL_trace"			:"",
			"VCL_return"		:"",
			"VCL_error"			:"",
			"ReqStart"			:"",
			"Hit"				:"",
			"HitPass"			:"",
			"ExpBan"			:"",
			"ExpKill"			:"",
			"WorkThread"		:"",
			"ESI_xmlerror"		:"",
			"Hash"				:"",
			"Backend_health"	:"",
			"VCL_Log"			:"",
			"Gzip"				:"",
		},
		#Client
		1:{
			"Debug"				:"",
			"Error"				:"",
			"CLI"				:"",
			"StatSess"			:"",
			"ReqEnd"			:"",
			"SessionOpen"		:"",
			"SessionClose"		:"",
			"BackendOpen"		:"",
			"BackendXID"		:"",
			"BackendReuse"		:"",
			"BackendClose"		:"",
			"HttpGarbage"		:"",
			"Backend"			:"",
			"Length"			:"",
			"FetchError"		:"",
			"RxRequest"			:"req.request",
			"RxResponse"		:"",
			"RxStatus"			:"",
			"RxURL"				:"req.url",
			"RxProtocol"		:"req.proto",
			"RxHeader"			:"req.http",
			"TxRequest"			:"",
			"TxResponse"		:"resp.response",
			"TxStatus"			:"resp.status",
			"TxURL"				:"",
			"TxProtocol"		:"resp.proto",
			"TxHeader"			:"resp.http",
			"ObjRequest"		:"",
			"ObjResponse"		:"obj.response",
			"ObjStatus"			:"",
			"ObjURL"			:"",
			"ObjProtocol"		:"obj.proto",
			"ObjHeader"			:"obj.http",
			"LostHeader"		:"",
			"TTL"				:"",
			"Fetch_Body"		:"",
			"VCL_acl"			:"",
			"VCL_call"			:"",
			"VCL_trace"			:"",
			"VCL_return"		:"",
			"VCL_error"			:"",
			"ReqStart"			:"",
			"Hit"				:"",
			"HitPass"			:"",
			"ExpBan"			:"",
			"ExpKill"			:"",
			"WorkThread"		:"",
			"ESI_xmlerror"		:"",
			"Hash"				:"",
			"Backend_health"	:"",
			"VCL_Log"			:"",
			"Gzip"				:"",
		},
		#Backend
		2:{
			"Debug"				:"",
			"Error"				:"",
			"CLI"				:"",
			"StatSess"			:"",
			"ReqEnd"			:"",
			"SessionOpen"		:"",
			"SessionClose"		:"",
			"BackendOpen"		:"",
			"BackendXID"		:"",
			"BackendReuse"		:"",
			"BackendClose"		:"",
			"HttpGarbage"		:"",
			"Backend"			:"",
			"Length"			:"",
			"FetchError"		:"",
			"RxRequest"			:"",
			"RxResponse"		:"beresp.response",
			"RxStatus"			:"beresp.status",
			"RxURL"				:"",
			"RxProtocol"		:"beresp.proto",
			"RxHeader"			:"beresp.http",
			"TxRequest"			:"bereq.request",
			"TxResponse"		:"",
			"TxStatus"			:"",
			"TxURL"				:"bereq.url",
			"TxProtocol"		:"bereq.proto",
			"TxHeader"			:"bereq.http",
			"ObjRequest"		:"",
			"ObjResponse"		:"",
			"ObjStatus"			:"",
			"ObjURL"			:"",
			"ObjProtocol"		:"",
			"ObjHeader"			:"",
			"LostHeader"		:"",
			"TTL"				:"",
			"Fetch_Body"		:"",
			"VCL_acl"			:"",
			"VCL_call"			:"",
			"VCL_trace"			:"",
			"VCL_return"		:"",
			"VCL_error"			:"",
			"ReqStart"			:"",
			"Hit"				:"",
			"HitPass"			:"",
			"ExpBan"			:"",
			"ExpKill"			:"",
			"WorkThread"		:"",
			"ESI_xmlerror"		:"",
			"Hash"				:"",
			"Backend_health"	:"",
			"VCL_Log"			:"",
			"Gzip"				:"",
		},
	}

class VarnishAPI:

	def __init__(self,sopath = 'libvarnishapi.so.1'):
		self.lib      = ctypes.cdll[sopath]
		VSLTAGS       = ctypes.c_char_p * 256
		self.VSL_tags = VSLTAGS.in_dll(self.lib, "VSL_tags")
		self.vd       = self.lib.VSM_New()
		self.lib.VSL_Setup(self.vd)
		self.lib.VSL_Open(self.vd, 1)


	def VSL_Dispatch(self, func, priv = False):
		cb_func = VSL_handler_f(func)
		if priv:
			self.lib.VSL_Dispatch(self.vd, cb_func, priv)
		else:
			self.lib.VSL_Dispatch(self.vd, cb_func, self.vd)
		

	def VSL_NonBlockingDispatch(self, func, priv = False):
		cb_func = VSL_handler_f(func)
		self.lib.VSL_NonBlocking(self.vd, 1)
		if priv:
			self.lib.VSL_Dispatch(self.vd, cb_func, priv)
		else:
			self.lib.VSL_Dispatch(self.vd, cb_func, self.vd)
		

	def VSL_Name2Tag(self, name):
		return self.lib.VSL_Name2Tag(name, ctypes.c_int(-1))

	def VSL_NameNormalize(self,name):
		r = self.VSL_Name2Tag(name)
		if r >= 0:
			return self.VSL_tags[r]

		return ''
		
	def normalizeDic(self, priv, tag, fd, length, spec, ptr, bm):
		type = '-'
		if spec == 1:
			type = 'c'
		elif spec == 2:
			type = 'b'
		return {
				'fd'      : fd,
				'type'    : spec,
				'typeName': type,
				'tag'     : self.VSL_tags[tag],
				'msg'     : ptr[0:length],
			}
