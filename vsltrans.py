# coding: utf-8
import varnishapi

import threading,time,signal,copy,sys,re,os,time




def main():

	argv = sys.argv
	argc = len(argv)

	vsl = VarnishLog()
	
	opt = {}
	cur = ''
	for v in argv:
		if v[0] == '-':
			cur = v
		elif not cur == '':
			if not opt.has_key(cur):
				opt[cur] = []
			opt[cur].append(v)

	if opt.has_key('-libvapi'):
		vsl.libvap = opt['-libvapi'][0]

	#VarnishAPIに接続
	vsl.attachVarnishAPI()

	if opt.has_key('-m'):
		for v in opt['-m']:
			if not vsl.appendTagFilter(v):
				return
	#-imの対応をそのうち書く(ignore -m)


	if opt.has_key('-f'):
		vsl.runFILE(opt['-f'][0])
	else:
		vsl.runVSL()


class VarnishLog:

	tags      = 0
	vap       = 0
	vslutil   = 0
	endthread = False
	filter    = 0
	logfile   = ''
	rfmt      = 0
	libvap    = 'libvarnishapi.so.1'
	
	tagfilter = {}

	def filterTagFilter(self, type, fd):
		cnt = len(self.tagfilter)
		if cnt == 0:
			return True
		
		base = self.obj[type][fd][-1]
		cmp = []
		#client
		for raw in base['raw']:
			tag = raw['tag']
			msg = raw['msg']
			if self.tagfilter.has_key(tag):
				for tf in self.tagfilter[tag]:
					execFlag = True
					for chk in cmp:
						if tf == chk:
							execFlag = False
							break
					if execFlag and tf.search(msg):
						cmp.append(tf)
						cnt -= 1
						if cnt == 0:
							return True

		#backend
		for idx in range(base['curidx'] + 1):
			if base['data'][idx]['backend'].has_key('raw'):
				for raw in base['data'][idx]['backend']['raw']['raw']:
					tag = raw['tag']
					msg = raw['msg']
					if self.tagfilter.has_key(tag):
						for tf in self.tagfilter[tag]:
							execFlag = True
							for chk in cmp:
								if tf == chk:
									execFlag = False
									break
							if execFlag and tf.search(msg):
								cmp.append(tf)
								cnt -= 1
								if cnt == 0:
									return True
		
		return False

	def appendTagFilter(self, data):
		spl = data.split(':', 2)
		if len(spl) == 1:
			print '[ERROR] -m option format'
			return False
		tag = self.vap.VSL_NameNormalize(spl[0])
		if tag == '':
			print '[ERROR] -m option format'
			return False
		if not self.tagfilter.has_key(tag):
			self.tagfilter[tag] = []
		
		try:
			self.tagfilter[tag].append(re.compile(spl[1]))
		except re.error:
			print '[ERROR] -m regex format'
			return False

		return True
	
	#Trx毎に格納
	obj = {
		1 : {}, #client
		2 : {}, #backend
	}
	#パース前のデータ保存領域
	vslData = []

	#出力順
	prnVarOrder = [
		'client',
		'server',
		'req',
		'bereq',
		'beresp',
		'obj',
		'resp',
		'storage',
		]

	#アクセスを分割するセパレータ
	reqsep  = {
		1 : {
			'open' : {
				'ReqStart'     : 'ReqStart',
				},
			'close' : {
				'ReqEnd'       : 'ReqEnd',
				},
			},
		2 : {
			'open' : {
				'BackendOpen'  : 'BackendOpen',
				'BackendReuse' : 'BackendReuse',
				},
			'close' : {
				'Length'       : 'Length',
				#'BackendClose' : 'BackendClose',
				},
			},
		}

	def __init__(self):
		#ファイル入力用の正規表現
		self.rfmt = re.compile('^ *([^ ]+) +([^ ]+) +([^ ]+) +(.*)$')
		
		self.filter     = {
			0:{},
			#Client
			1:{
				#"Debug"				:"",
				"Error"				: self.filterError,
				#"CLI"				:"",
				#"StatSess"			:"",
				"ReqEnd"			: self.filterReqEnd,
				#"SessionOpen"		:"",
				#"SessionClose"		:"",
				#"BackendOpen"		:"",
				#"BackendXID"		:"",
				#"BackendReuse"		:"",
				#"BackendClose"		:"",
				#"HttpGarbage"		:"",
				"Backend"			: self.filterBackend,
				"Length"			: self.filterLength,
				"FetchError"		: self.filterError,
				"RxRequest"			: self.filterRequest,
				#"RxResponse"		:"",
				#"RxStatus"			:"",
				"RxURL"				: self.filterRequest,
				"RxProtocol"		: self.filterRequest,
				"RxHeader"			: self.filterRequest,
				#"TxRequest"			:"",
				"TxResponse"		: self.filterRequest,
				"TxStatus"			: self.filterRequest,
				#"TxURL"				:"",
				"TxProtocol"		: self.filterRequest,
				"TxHeader"			: self.filterRequest,
				#"ObjRequest"		:"",
				"ObjResponse"		: self.filterRequest,
				#"ObjStatus"			:"",
				#"ObjURL"			:"",
				"ObjProtocol"		: self.filterRequest,
				"ObjHeader"			: self.filterRequest,
				#"LostHeader"		:"",
				"TTL"				: [self.filterTTL, self.filterActItem],
				#"Fetch_Body"		:"",
				#"VCL_acl"			:"",
				"VCL_call"			: self.filterAction,
				"VCL_trace"			: [self.filterTrace, self.filterActItem],
				"VCL_return"		: self.filterAction,
				#"VCL_error"			:"",
				"ReqStart"			: self.filterReqStart,
				#"Hit"				:"",
				"HitPass"			: [self.filterHitPass, self.filterActItem],
				#"ExpBan"			:"",
				#"ExpKill"			:"",
				#"WorkThread"		:"",
				"ESI_xmlerror"		: self.filterError,
				"Hash"				: [self.filterHash, self.filterActItem],
				#"Backend_health"	:"",
				"VCL_Log"			: self.filterActItem,
				#"Gzip"				:"",
			},
			#Backend
			2:{
				#"Debug"				:"",
				"Error"				: self.filterError,
				#"CLI"				:"",
				#"StatSess"			:"",
				#"ReqEnd"			:"",
				#"SessionOpen"		:"",
				#"SessionClose"		:"",
				#"BackendOpen"		:"",
				#"BackendXID"		:"",
				#"BackendReuse"		:"",
				#"BackendClose"		:"",
				#"HttpGarbage"		:"",
				#"Backend"			:"",
				"Length"			: self.filterLength,
				#"FetchError"		:"",
				#"RxRequest"			:"",
				"RxResponse"		: self.filterRequest,
				"RxStatus"			: self.filterRequest,
				"RxURL"				: self.filterRequest,
				"RxProtocol"		: self.filterRequest,
				"RxHeader"			: self.filterRequest,
				"TxRequest"			: self.filterRequest,
				#"TxResponse"		:"",
				#"TxStatus"			:"",
				"TxURL"				: self.filterRequest,
				"TxProtocol"		: self.filterRequest,
				"TxHeader"			: self.filterRequest,
				#"ObjRequest"		:"",
				#"ObjResponse"		:"",
				#"ObjStatus"			:"",
				#"ObjURL"			:"",
				#"ObjProtocol"		:"",
				#"ObjHeader"			:"",
				#"LostHeader"		:"",
				#"TTL"				:"",
				#"Fetch_Body"		:"",
				#"VCL_acl"			:"",
				#"VCL_call"			:"",
				#"VCL_trace"			:"",
				#"VCL_return"		:"",
				#"VCL_error"			:"",
				#"ReqStart"			:"",
				#"Hit"				:"",
				#"HitPass"			:"",
				#"ExpBan"			:"",
				#"ExpKill"			:"",
				#"WorkThread"		:"",
				#"ESI_xmlerror"		:"",
				#"Hash"				:"",
				#"Backend_health"	:"",
				#"VCL_Log"			:"",
				#"Gzip"				:"",
			},
		}
		self.vslutil = varnishapi.VSLUtil()
		self.tags    = self.vslutil.tags
		
	#フィルタのループ
	def loopFilter(self, base):
		raw    = base['raw']
		curidx = base['curidx']
		
		for v in raw:
			type = v['type']
			tag  = v['tag']
			if self.filter[type].has_key(tag):
				if isinstance(self.filter[type][tag], list):
					for func in self.filter[type][tag]:
						func(base,v)
				else:
					self.filter[type][tag](base,v)

	#フィルタ情報を格納
	def filterTTL(self, base, rawline):
		'''
		                       0       1    2     3    4     5      6    7    8      9
		                      xid      src  ttl grace keep basetime age date expire max-age
		  538 TTL          c 2480419881 VCL 864000 -1 -1 1367990868 -0
		  663 TTL          c 2480419886 RFC 3600 -1 -1 1367990868 0 1367990868 1367990968 3600
		'''
		spl = rawline['msg'].split(' ')
		spl[5] = time.strftime("%Y-%m-%d %H:%M:%S +0000" ,time.gmtime(float(spl[5])))
		if spl[1] == 'RFC':
			if int(spl[8]) >0:
				spl[8] = time.strftime("%Y-%m-%d %H:%M:%S +0000" ,time.gmtime(float(spl[8])))
			if int(spl[7]) >0 :
				spl[7] = time.strftime("%Y-%m-%d %H:%M:%S +0000" ,time.gmtime(float(spl[7])))
			rawline['aliasmsg'] = "[RefTime]=%s [src]=RFC [ttl]=%s [grace]=%s [keep]=%s [Age]=%s [Date]=%s [Expires]=%s [Max-Age]=%s" % (spl[5], spl[2], spl[3], spl[4], spl[6], spl[7], spl[8], spl[9])
		else:
			rawline['aliasmsg'] = "[RefTime]=%s [src]=VCL [ttl]=%s [grace]=%s [keep]=%s [Age]=%s" %  ( spl[5], spl[2], spl[3], spl[4], spl[6])
		
		
	#バックエンド情報の格納
	def filterBackend(self, base, rawline):
		curidx          = base['curidx']
		data            = base['data'][curidx]['backend']
		cvar            = base['data'][curidx]['var']

		
		#'msg': '14 default default',
		#         fd name    verbose
		spl                 = rawline['msg'].split(' ')
		backendFd           = long(spl[0])
		#data['raw']        = copy.deepcopy(self.obj[2][backendFd])
		if (not self.obj[2].has_key(backendFd) or len(self.obj[2][backendFd]) == 0):
			return
		data['raw']         = self.obj[2][backendFd].pop(0)
		
		bcuridx             = data['raw']['curidx']
		
		bvar                = data['raw']['data'][bcuridx]['var']
		data['name']                        = spl[1]
		data['verbose']                     = spl[2]
		base['data'][curidx]['backendname'] = spl[2]
		
		base['info']['backend'].append(spl[2])

		base['data'][curidx]['length']          = data['raw']['data'][bcuridx]['length']
		#link var
		for k,v in bvar.items():
			cvar[k] = v
	
	#lengthを取得
	def filterLength(self, base, rawline):

		curidx          = base['curidx']

		base['data'][curidx]['length'] = int(rawline['msg'])

	
	#traceを解釈
	def filterTrace(self, base, rawline):
		spl  = rawline['msg'].split(' ')
		spl2 = spl[1].split('.')
		
		rawline['aliasmsg'] = '(VRT_Count:%s line:%s pos:%s)' % (spl[0], spl2[0], spl2[1])
	
	#error系を格納
	def filterError(self, base, rawline):
		curidx     = base['curidx']
		data       = base['data'][curidx]['error']

		data.append({'key':rawline['tag'],'val':rawline['msg']})

		'''
		  {'fd': 12L,
		   'msg': 'no backend connection',
		   'tag': 'FetchError',
		   'tagname': '',
		   'type': 1L,
		   'typeName': 'c'},
		'''
	
	#Action内のアイテムを格納
	def filterActItem(self, base, rawline):
		curidx     = base['curidx']
		curactidx  = base['data'][curidx]['curactidx']


		data       = base['data'][curidx]['act'][curactidx]['item']
		if rawline.has_key('aliasmsg'):
			data.append({'key' : rawline['tag'],'val' : rawline['aliasmsg']})
		else:
			data.append({'key' : rawline['tag'],'val' : rawline['msg']})
	
	#実行時間を取得
	def filterReqEnd(self, base, rawline):
		spl                          = rawline['msg'].split(' ')
		curidx                       = base['curidx']
		base['data'][curidx]['time'] = {}
		data                         = base['time']
		data['start']   = float(spl[1])
		data['total']   = float(spl[2]) - data['start']
		data['accept']  = float(spl[3])
		data['execute'] = float(spl[4])
		data['exit']    = float(spl[5])

	#アクションを構築
	def filterAction(self, base, rawline):
	
		#12 VCL_call     c fetch 3 41.9 23 103.5 24 109.17
		#   12 VCL_call     c pass 17 81.5 pass
		#

		spl            = rawline['msg'].split(' ')
		msg            = spl.pop(0)
		ret            = ''
		item           = []
		tracetmp       = ''
		#traceとreturnを構築
		if(len(spl) > 0):
			for v in spl:
				if v[0].isdigit():
					#trace
					spl2 = v.split('.')
					if len(spl2)==1:
						#trace count
						tracetmp = '(VRT_Count:' + v + ' '
					else:
						#trace other
						tracetmp += 'line:' + spl2[0] + ' pos:' + spl2[1] + ')'
						item.append({'key':'VCL_trace','val':tracetmp})
				else:
					ret = v

		curidx         = base['curidx']
		
		#ESI-check
		if msg == 'recv' and base['data'][curidx]['curactidx'] > 0:

			self.incrData(base, 'esi')
			curidx = base['curidx']

		data           = base['data'][curidx]['act']
		
		
		if rawline['tag'] == 'VCL_return':
			curactidx = base['data'][curidx]['curactidx']
			data[curactidx]['return'] = msg
			
			#restartとESIの場合はIncrする
			if msg == 'restart':
				self.incrData(base, 'restart')
			
			
		else:
			base['data'][curidx]['curactidx'] += 1
			data.append({'function' : msg,'return' : ret,'item' : item})

	#クライアント情報取得
	def filterReqStart(self, base, rawline):
		#                    client.ip   port     xid
		#          'msg': '192.168.1.199 47475 1642652384',
		#WSP(sp, SLT_ReqStart, "%s %s %u", sp->addr, sp->port,  sp->xid);
		curidx         = base['curidx']
		if not base['data'][curidx]['var'].has_key('req'):
			base['data'][curidx]['var']['req'] = {}
		data           = base['data'][curidx]['var']['req']
		spl = rawline['msg'].split(' ')
		base['client'] = {
			'ip'   : spl[0],
			'port' : spl[1],
			}
		data['xid'] = [{
			'key'  : '',
			'lkey' : '',
			'val'  : spl[2],
			}]

	#restart,ESIの情報を構築
	def conRestartESI(self,base):
		restart = 0
		esi     = 0
		#length  = []
		data = base['data']
		
		for v in data:
			info = v['info']
			if info == 'esi':
				esi += 1
				#length.add(v['length'])
			elif info == 'restart':
				restart += 1
		base['info']['restart']     = restart
		base['info']['esi']         = esi
		#base['info']['extraLength'] = length

	#varyの情報を構築
	def conVary(self,base):
		for trx in base['data']:
			var = trx['var']
			if var.has_key('obj') and var['obj'].has_key('http'):
				for objhttp in var['obj']['http']:
					if 'vary' == objhttp['lkey']:
						spl = objhttp['val'].split(',')
						for tgkey in spl:
							val = ''
							tgkeylow = tgkey.lower()
							if var.has_key('req') and var['req'].has_key('http'):
								for reqhttp in var['req']['http']:
									if tgkeylow == reqhttp['lkey']:
										val = reqhttp['val']
										trx['hash']['vary'].append({'key' : tgkey, 'val' : val})
								if val == '':
									trx['hash']['vary'].append({'key' : tgkey, 'val' : ''})
	#ハッシュ情報を格納
	def filterHash(self, base, rawline):
		curidx = base['curidx']
		data   = base['data'][curidx]['hash']['hash']
		data.append(rawline['msg'])

	def filterHitPass(self, base, rawline):
		base['info']['hitpass']    += 1

	#req.urlなどを格納
	def filterRequest(self, base, rawline):
		curidx = base['curidx']
		data   = base['data'][curidx]['var']
		msg    = rawline['msg']
		spl    = rawline['tagname'].split('.')
		cmpo   = spl[0]
		prop   = spl[1]
		
		
		if not data.has_key(cmpo):
			data[cmpo] = {}
		if not data[cmpo].has_key(prop):
			data[cmpo][prop] = []

		if prop == 'http':
			spl = msg.split(':')
			data[cmpo][prop].append({'key':spl[0], 'lkey':spl[0].lower(), 'val':spl[1].lstrip()})
		else:
			data[cmpo][prop].append({'key':'', 'lkey':'', 'val':msg})
			
	
	
	
	#データ配列の作成
	def incrData(self,base, info=''):
		if not base.has_key('data'):
			base['data']   = []
		base['data'].append({
			'var'         : {},	#req, obj, resp ,beresp
			'act'         : [],	#recv, pass, miss ,fetch ...
			'hash'        : {'hash':[],'vary':[]},
			'backend'     : {},
			'error'       : [],
			'curactidx'   : -1,
			'info'        : info, #esi , restart
			'length'      : 0,
			'backendname' : '',
			})
		base['curidx'] += 1
	
	#トランザクションデータをコミット
	def commitTrx(self, type, fd):
		#if type == 2:
		#	return
		base           = self.obj[type][fd][-1]
		raw            = base['raw']
		base['curidx'] = -1
		base['info']   = {'hitpass':0,'esi':0,'restart':0,'backend':[]}
		base['time']   = {}
		#base['curactidx'] = -1

		self.incrData(base)
		
		#######################
		#ここから詳細データ作成

		#タグ名を付与
		self.apdTagName(raw)

		#フィルタ実行
		self.loopFilter(base)
		
		#Vary情報の取得
		self.conVary(base)
		
		#restart/ESI情報の作成
		self.conRestartESI(base)
		
		#######################
		#for client
		if type == 1:
			#client/server.ip付与
			self.setVarClientServer(base)


	
	
	def printTrx(self,type, fd):
		if not type == 1:
			return
		base           = self.obj[type][fd][-1]
		
		if not self.filterTagFilter(type,fd):
			return
		
		#print var
		#一旦テストで0を指定している（restartとかになると変わるので注意）
		idx = 0
		
		self.printLine('<')
		print 'START transaction.'
		self.printLine('<')
		#全体のInfoを出力
		self.printGeneralInfo(base)
		for idx in range(base['curidx'] + 1):

			#個別のInfoを出力
			self.printInfo(base,idx)

			#エラーを表示
			self.printError(base,idx)

			#アクションを表示
			self.printAction(base,idx)

			#変数情報を表示
			self.printVariable(base,idx)

		self.printLine('>')
		print 'END transaction.'
		self.printLine('>')
		print

		
	def printGeneralInfo(self,base):
		data     = base['data']
		reqdata  = data[0]

		#junkセッション対応
		if data[0]['var'].has_key('resp'):
			respvar  = data[0]['var']['resp']
		else:
			respvar  = False
			
		client   = base['client']
		info     = base['info']
		timeinfo = base['time']
		host    = ''
		if reqdata['var']['req'].has_key('http'):
			for v in reqdata['var']['req']['http']:
				if v['lkey'] == 'host':
					host = v['val']
					break

		print 'General Info.'
		self.printLine()
		print 'Client ip:port  | ' +client['ip'] + ':' + client['port']
		print 'Request host    | ' + host
		print 'Response size   | ' + str(reqdata['length']) + ' byte'
		if respvar:
			print 'Response Status | ' + respvar['proto'][0]['val'] +' '+ respvar['status'][0]['val'] +' ' + respvar['response'][0]['val']
		print 'Total time      | ' + str(round(timeinfo['total'],5)) + ' sec'
		print 'HitPass count   | ' + str(info['hitpass'])
		print 'Restart count   | ' + str(info['restart'])
		print 'ESI count       | ' + str(info['esi'])
		print 'Backend count   | ' + str(len(info['backend']))
		for v in info['backend']:
			print ' +Backend       | ' + v

		self.printLine()
		print

	def printError(self,base,idx):
		data = base['data'][idx]['error']
		if len(data) == 0:
			return

		max = self.chkMaxLength(data,'key')

		self.printLine('#')
		print 'Error infomation.'
		self.printLine()

		for v in data:
			pad = ' ' * (max - len(v['key']))
			print v['key'] + pad + ' | ' + v['val']

		self.printLine()
		print
	
	def printInfo(self,base,idx):
		data     = base['data'][idx]
		hashdata = data['hash']
		
		ret  = ''

		self.printLine('#')
		print 'Object infomation.'
		self.printLine()
		
		#type
		if not data['info'] == '':
			print 'Type        | ' + data['info']

		#hash and vary
		for hash in hashdata['hash']:
			ret += '"' + hash + '" + '
		print 'Hash        | ' + ret.rstrip('+ ')

		if len(hashdata['vary']) > 0:
			maxlen = self.chkMaxLength(hashdata['vary'],'key') + len('req.http.')
			self.printLine()
			for vary in hashdata['vary']:
				pad = ' ' * (maxlen - len('req.http.' + vary['key']))
				print 'Vary        | req.http.' + vary['key'] + pad + ' | ' + vary['val']

		#length
		print 'Object size | ' + str(data['length'])

		#backend
		print 'Backend     | ' + data['backendname']
		
		self.printLine()
		print





	def printAction(self,base,idx):
		data = base['data'][idx]['act']

		max = 6 # return

		self.printLine('#')
		print 'Action infomation.'

			
		self.printLine()

		for v in data:
			length = self.chkMaxLength(v['item'],'key');
			if max < length:
				max = length

		for v in data:
			self._sub_printActionBox(v['function'])
			self._sub_printActionLine(v,max)
		print
		
	def _sub_printActionLine(self , data, max):
		item = data['item']
		ret  = data['return']
		print '      |'
		if len(item) > 0:
			for v in item:
				pad = ' ' * (max - len(v['key']))
				print '      | ' + v['key'] + pad +' | ' + v['val']
		pad = ' ' * (max - 6)
		print '      | ' + max * ' ' + ' |'
		print '      | return' + pad + ' | ' + ret
		print '      |'

	def _sub_printActionBox(self,txt):
		df  = 13 - len(txt)
		spa = ' ' * (df // 2)
		spb = ' ' * ((df // 2) + (df % 2))
		
		print '+-------------+'
		print '|'+spa+txt+spb+'|'
		print '+-------------+'

	def printVariable(self,base,idx):
		data = base['data'][idx]['var']
		prn  = []
		
		for key in self.prnVarOrder:
			self._sub_printVariable(data,key,prn)

		if len(prn) > 0:
			maxLen    = self.chkMaxLength(prn, 'key')
			maxLenVal = self.chkMaxLength(prn, 'val')
			
			lineLen = (maxLen + maxLenVal + len(' | '))

			self.printLine('#')
			print 'Variable infomation.'
			self.printLine('-',lineLen)
			for v in prn:
				if v == 0:
					self.printLine('-',lineLen)
				else:
					self.printPad(v['key'], v['val'], maxLen)
			print

	def _sub_printVariable(self,data,key,prn):
		if not data.has_key(key):
			return prn
		obj = data[key].items()
		for cat,v in obj:
			for vv in v:
				prn.append({
					'key' : (key + '.' + cat + '.' + vv['key']).strip('.'),
					'val' : vv['val']
					})
		prn.append(0)
		return prn

	def printLine(self, char = '-' ,length = 70):
		print char * length
		
	def printPad(self,k, v, maxLen , dlm = " | "):
		fmt    = "%- " + str(maxLen) + "s" + dlm + "%s"
		print fmt % (k , v)
	
	def chkMaxLength(self, data, key=''):
		maxLen = 0
		if isinstance(data, list):
			for v in data:
				if isinstance(v, dict) and v.has_key(key):
					length = len(v[key])
					if maxLen < length:
						maxLen = length
		else:
			for k,v in data.items():
				length = len(k)
				if maxLen < length:
					maxLen = length
		return maxLen
	
	#client.*とserver.*を設定（serverはデータ元がないので・・・）
	def setVarClientServer(self,base):
		data   = base['data']
		for var in data:
			var['client'] = {
				'ip' : [{
					'key'  : '',
					'lkey' : '',
					'val'  : base['client']['ip'],
					}]
				}

	#タグの名称追加
	def apdTagName(self,raw):
		for v in raw:
			v['tagname'] = self.tags[v['type']][v['tag']]
	
	#トランザクションごとのデータ作成
	def conTrx(self,r):
		if not r:
			return
		#値を作成
		type = r['type']
		if type == 0:
			return
		
		tag  = r['tag']
		fd   = r['fd']
		if self.obj[type].has_key(fd):
			#開いてる
			if self.reqsep[type]['close'].has_key(tag):
				#閉じる(Print対象）
				self.obj[type][fd][-1]['raw'].append(r)

				self.commitTrx(type,fd)
				self.printTrx(type,fd)
				if type == 1:
					#データ削除(Clientの場合のみ)
					del self.obj[type][fd]
			elif self.reqsep[type]['open'].has_key(tag):
				if type == 1: #client
					#開く（バックエンドか何かしらのバグ）
					del self.obj[type][fd]
					self.obj[type][fd] = [{'raw' : []}]
					self.obj[type][fd][-1]['raw'].append(r)
				elif type == 2:#Backend
					#開く（バックエンドか何かしらのバグ）
					#ESI対応で使われたかのチェックを行う
					#del self.obj[type][fd]
					self.obj[type][fd].append({'raw' : []})
					self.obj[type][fd][-1]['raw'].append(r)

			else:
				#通常格納
				self.obj[type][fd][-1]['raw'].append(r)
		elif self.reqsep[type]['open'].has_key(tag):
			#開く
			self.obj[type][fd] = [{'raw':[]}]
			self.obj[type][fd][-1]['raw'].append(r)

	#スレッド周りの処理
	def sighandler(self,event, signr, handler):
		event.set()
		
	def vapLoop(self,event):
		while not event.isSet():
			self.vap.VSL_NonBlockingDispatch(self.vapCallBack)
			time.sleep(0.1)
		self.endthread = True


	def fileLoop(self,event):
		if not os.path.exists(self.logfile):
			self.endthread = True
			return

		f = open(self.logfile)
		for line in f.readlines():
			self.vslData.append(self.parseFile(line))
		f.close()
		self.endthread = True





	def printLoop(self,event):
		while not event.isSet():
			if len(self.vslData) == 0:
				
				if self.endthread:
					break
				time.sleep(0.1)
				continue
			while 1:
				if len(self.vslData) == 0:
					break
				self.conTrx( self.vslData.pop(0) )
			if self.endthread:
				break
	

	def startThread(self,inloop):
		threads = []
		e = threading.Event()
		signal.signal(signal.SIGINT, (lambda a, b: self.sighandler(e, a, b)))

		# スレッド作成
		#if self.vap:
		threads.append(threading.Thread(target=inloop, args=(e,)))
		threads[-1].start()
		
		threads.append(threading.Thread(target=self.printLoop, args=(e,)))
		threads[-1].start()

		# 終了待ち
		for th in threads:
			while th.isAlive():
				time.sleep(0.5)
			th.join()

		
	def attachVarnishAPI(self):
		self.vap = varnishapi.VarnishAPI(self.libvap)

	def vapCallBack(self,priv, tag, fd, length, spec, ptr, bm):
		self.vslData.append(self.vap.normalizeDic(priv, tag, fd, length, spec, ptr, bm))

	def parseFile(self, data):
		'''
		{'fd': 0L,
		 'msg': 'Wr 200 19 PONG 1367695724 1.0',
		 'tag': 'CLI',
		 'type': 0L,
		 'typeName': '-'}
		データを読み込む場合
		 1284 RxHeader     b Content-Type: image/png

		'''
		m = self.rfmt.search(data.rstrip("\r\n"))

		if not m:
			return

		r = {
			'fd'       : int(m.group(1)),
			'msg'      : m.group(4),
			'tag'      : m.group(2),
			'typeName' : m.group(3),
			}

		if r['typeName'] == '-':
			r['type'] = 0
		elif r['typeName'] == 'c':
			r['type'] = 1
		elif r['typeName'] == 'b':
			r['type'] = 2
		return(r)

		

		
	def runVSL(self):
		self.startThread(self.vapLoop)

	def runFILE(self,file):
		self.logfile = file
		self.startThread(self.fileLoop)
		
		


#---------------------------------------------------------------------------------------------------
# ref:http://tomoemon.hateblo.jp/entry/20090921/p1
from pprint import pprint
import types

def var_dump(obj):
  pprint(dump(obj))

def dump(obj):
  '''return a printable representation of an object for debugging'''
  newobj = obj
  if isinstance(obj, list):
    # リストの中身を表示できる形式にする
    newobj = []
    for item in obj:
      newobj.append(dump(item))
  elif isinstance(obj, tuple):
    # タプルの中身を表示できる形式にする
    temp = []
    for item in obj:
      temp.append(dump(item))
    newobj = tuple(temp)
  elif isinstance(obj, set):
    # セットの中身を表示できる形式にする
    temp = []
    for item in obj:
      # itemがclassの場合はdump()は辞書を返すが,辞書はsetで使用できないので文字列にする
      temp.append(str(dump(item)))
    newobj = set(temp)
  elif isinstance(obj, dict):
    # 辞書の中身（キー、値）を表示できる形式にする
    newobj = {}
    for key, value in obj.items():
      # keyがclassの場合はdump()はdictを返すが,dictはキーになれないので文字列にする
      newobj[str(dump(key))] = dump(value)
  elif isinstance(obj, types.FunctionType):
    # 関数を表示できる形式にする
    newobj = repr(obj)
  elif '__dict__' in dir(obj):
    # 新しい形式のクラス class Hoge(object)のインスタンスは__dict__を持っている
    newobj = obj.__dict__.copy()
    if ' object at ' in str(obj) and not '__type__' in newobj:
      newobj['__type__']=str(obj).replace(" object at ", " #").replace("__main__.", "")
    for attr in newobj:
      newobj[attr]=dump(newobj[attr])
  return newobj

#---------------------------------------------------------------------------------------------------

main()
