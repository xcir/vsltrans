# coding: utf-8
import varnishapi

import threading,time,signal,copy,sys,re,os,time


'''
- [VXID-TREE]
  self.sess = {
    1:[None,2,3,None],#idx=0 is parent vxid. value is "None" if have not parent vxid(RootVXID)
    2:[1,4,None]
    3:[1,None]
    4:[2,None]#If last value is "None", closed VXID array.
  }
  self.vxid = {
      vxid : [
          1,2,3.... # 
      ]
      data : {
          actionidx:['recv','hash'...]
          action : {
              recv:
                # [init] --#call vcl_func#--> [work] --#return vcl_func#--> [fini]
                init:{
                  var:{
                    'req.http.hoge':['/a','/b',None], # None is unset value.
                  },
                  event:[
                      {k:'TimeStamp',v:'hogehoge'},
                      {k:'...',v:'...'},
                  ]
                },
                work:{
                  var:{
                    'req.http.hoge':['/a','/b',None], # None is unset value.
                  },
                  event:[
                      {k:'TimeStamp',v:'hogehoge'},
                      {k:'',v:''},
                  ]
                },
                fini:{
                  var:{
                    'req.http.hoge':['/a','/b',None], # None is unset value.
                  },
                  event:[
                      {k:'TimeStamp',v:'hogehoge'},
                      {k:'',v:''},
                  ]
                }
              hash:{...}
              ...
              tmp:{...}# uncommitted data.
          }
      },
  }


self.vxid[vxid] = {'actidx':[], 'act':{},'actcur':'initial','actnxt':None,'actstat':'init'}
actcur = 現在のアクション
actnxt = 次のアクション(vcl_callで変更）
actstat= 初期状態なのかwork状態なのか
              +-

'''



#actはvcl_recvを呼び出される前にCALLされるものがあるのでそこら辺を考慮する
#junkデータを排除するようにする

class vslTrans:
	def dataClear(self):
		self.sess  = {}
		self.vxid  = {}
		

	def __init__(self, opts):
		self.debug = 1
		self.debug = 0
		
		self.mode = 'request'
		#self.mode = 'session'
		#一旦requestで、sessionも対応する
		vops = ['-g',self.mode]
		if isinstance(opts, list):
			for o,a in opts:
				if o == '-q':
					vops.append(o)
					vops.append(a)
		self.vap     = varnishapi.VarnishLog(vops)
		self.vslutil = varnishapi.VSLUtil()
		self.dataClear()
		self.__filter = {
			'ReqURL':		[self.fExistVXID, self.fRequest],
			'ReqStart':		[self.fExistVXID, self.fRequest],
			'ReqMethod':	[self.fExistVXID, self.fRequest],
			'ReqProtocol':	[self.fExistVXID, self.fRequest],
			'ReqHeader':	[self.fExistVXID, self.fRequest],
			'ReqUnset':		[self.fExistVXID, self.fRequest],

			'BereqURL':			[self.fExistVXID, self.fRequest],
			'BereqMethod':		[self.fExistVXID, self.fRequest],
			'BereqProtocol':	[self.fExistVXID, self.fRequest],
			'BereqHeader':		[self.fExistVXID, self.fRequest],
			'BereqUnset':		[self.fExistVXID, self.fRequest],

			'BerespHeader':		[self.fExistVXID, self.fRequest],
			'BerespUnset':		[self.fExistVXID, self.fRequest],
			'BerespProtocol':	[self.fExistVXID, self.fRequest],
			'BerespStatus':		[self.fExistVXID, self.fRequest],
			'BerespReason':		[self.fExistVXID, self.fRequest],

			'RespHeader':	[self.fExistVXID, self.fRequest],
			'RespUnset':	[self.fExistVXID, self.fRequest],
			'RespProtocol':	[self.fExistVXID, self.fRequest],
			'RespStatus':	[self.fExistVXID, self.fRequest],
			'RespReason':	[self.fExistVXID, self.fRequest],

			'ObjHeader':	[self.fExistVXID, self.fRequest],
			'ObjUnset':		[self.fExistVXID, self.fRequest],
			'ObjProtocol':	[self.fExistVXID, self.fRequest],
			'ObjStatus':	[self.fExistVXID, self.fRequest],
			'ObjReason':	[self.fExistVXID, self.fRequest],


			'Begin':		self.fBegin,
			'End':			[self.fExistVXID, self.fEnd],
			'Link':			[self.fExistVXID, self.fLink],
			'VCL_call':		[self.fExistVXID, self.fVCLCall],
			'VCL_return':	[self.fExistVXID, self.fVCLReturn],

			'__default':	[self.fExistVXID, self.fEventStor],

		}
		
	
	def execute(self):
		while 1:
			#dispatch
			self.state = 0
			ret = self.vap.Dispatch(self.vapCallBack)
			if 0 == ret:
				time.sleep(0.1)
				
	def vapCallBack(self, vap, cbd, priv):
		if not cbd['isbin']:
			cbd['length'] = cbd['length'] -1;
			cbd['data']   = cbd['data'][:-1]
			
		self.filter(cbd)
	
	def filter(self,cbd):
		ttag = self.vap.VSL_tags[cbd['tag']]
		
		vxid = cbd['vxid']
		key = ttag
		if key not in self.__filter:
			key = '__default'
			if self.debug:
				print "%15s " % ttag,
				print cbd

		if isinstance(self.__filter[key], list):
			for func in self.__filter[key]:
				if not func(ttag, vxid, cbd):
					break
		else:
			self.__filter[key](ttag, vxid, cbd)

	def appendVar(self,vxid,k,v):
		vd = self.vxid[vxid]
		cv = vd['act']['temp'][vd['actstat']]['var']
		if k not in cv:
			cv[k] = []
		cv[k].append(v)

	def appendEvent(self,vxid,k,v):
		vd = self.vxid[vxid]
		act = vd['act']['temp'][vd['actstat']]
		act['event'].append({'k':k,'v':v})

	def searchKey(self,k,ar):
		for v in ar:
			if v['k'] == k:
				return v['v']
		return ''




		
	def flushSess(self,vxid,lv,mode,prnDone):
		
		if vxid not in prnDone:
			print self.flushAct(vxid,'',lv,mode,prnDone),
			prnDone[vxid] = vxid
		for v in self.sess[vxid][1:-1]:
			self.flushSess(v,lv+1,mode,prnDone)
	

		
	def rebuildVar(self,vdi,minsize):
		#key=varName
		retv  = {}
		reti  = {'init':minsize,'work':minsize,'fini':minsize}
		keysz = minsize
		for k in ['init','work','fini']:
			for kk,vv in vdi[k]['var'].items():
				if kk not in retv:
					retv[kk] = {'init':'','work':'','fini':''}
				tmp = []
				for vvv in vv:
					if vvv == None:
						tmp.append('[unset]')
					else:
						tmp.append("'%s'" % vvv)
				retv[kk][k] = " -> ".join(tmp)
				l = len(retv[kk][k])
				if l > reti[k]:
					reti[k] = l
				l = len(kk)
				if l > keysz:
					keysz = l
		return {'val':retv,'size':reti,'keysz':keysz}


	def printVar(self,vdi,prefix):
		'''
		+-----------+-----------+------------+----+
		|        var|init       |work        |fini|
		+-----------+-----------+------------+----+
		|req.url    | '/'       |            |    |
		|req.http.x |           | 'x'->'y'   |    |
		+-----------+-----------+------------+----+
		
		'''
		ret = ''
		rv = self.rebuildVar(vdi,4)
		tmp =  '+-' +('-'* rv['keysz']) + '-+-'
		sar = ['init','work','fini']
		for step in sar:
			tmp = tmp + ('-'* rv['size'][step]) + '-+-'
		line = prefix + tmp[:-1]
		ret = ret + line + "\n"
		
		tmp =  '| ' +("%" + str(rv['keysz']) + "s | ")  % 'key'
		for step in sar:
			tmp = tmp + self.printCenter(rv['size'][step],step) + " | "
			#tmp = tmp + ("%" + str(rv['size'][step]) + "s | ")  % step
		ret = ret + prefix + tmp + "\n"
		ret = ret + line + "\n"
		
		
		for vk, vv in sorted(rv['val'].items()):
			tmp =  '| '+("%" + str(rv['keysz']) + "s | ")  % vk
			for step in sar:
				vvv = vv[step]
				tmp = tmp + ("%-" + str(rv['size'][step]) + "s | ")  % vvv
			ret = ret + prefix + tmp + "\n"
		ret = ret + line + "\n"
		return ret
	
	def flushActEvent(self,vdi,prefix,lv,mode,prnDone):
		sk = ['init','work','fini']
		ret = ''
		sp  = ' '*3+'| '
		
		max = 3
		if mode == 'event':
			for step in sk:
				for v in vdi[step]['event']:
					l = len(v['k'])
					if l > max:
						max = l
		
		for step in sk:
			for v in vdi[step]['event']:
				if mode == 'event':
					ret = ret + prefix + sp + (("%"+str(max)+"s | %s") % (v['k'],v['v'])) + "\n"
				if v['k'] == 'Link':
					spl = v['v'].split(' ', 3)
					lvxid = int(spl[1])
					prnDone[lvxid]=lvxid
					if spl[2] == 'restart':
						ret = ret + self.printBox(prefix,'#',"RESTART")
						ret = ret + self.flushAct(lvxid, '' ,lv,mode,prnDone)
					if spl[2] == 'esi':
						ret = ret + self.printBox(prefix+sp+' '*max + " > ",'#',"ESI")
						ret = ret + self.flushAct(lvxid, prefix+sp+' '*max + " > " ,lv+1,mode,prnDone)
					else:
						ret = ret + self.flushAct(lvxid, prefix+sp+' '*max + " > " ,lv+1,mode,prnDone)
				elif v['k'] == 'call':
					ret = ret + self.printBox(prefix,'>',"vcl_%s" % (v['v'].lower()))
				elif v['k'] == 'return':
					if   mode == 'var':
						ret = ret + self.printVar(vdi,prefix + sp)
					ret = ret + self.printBox(prefix,'<',"return(%s)" % (v['v'].lower()))
					ret = ret + prefix + sp + "\n"
		return ret
			
	def printBox(self,prefix,wrd,txt):
		ret = prefix + wrd*60+"\n"
		ret = ret + prefix + wrd + self.printCenter(58,txt)+wrd+"\n"
		ret = ret + prefix + wrd*60+"\n"
		return ret
	def flushAct(self,vxid,prefix,lv,mode,prnDone):
		ret = self.printBox(prefix,'#',"VXID:%d" % vxid)
		#ret =  prefix + "<<VXID:%d>>\n" % vxid
		vd = self.vxid[vxid]
		for k in vd['actidx']:
			vdi = vd['act'][k]
			retval = self.searchKey('return',vdi['work']['event'])
			'''
			ret = ret+ prefix + '#'*60+"\n"
			ret = ret + prefix + '#' + self.printCenter(58,"vcl_%s / return(%s)" % (k.lower(),retval))+"#\n"
			ret = ret + prefix + '#'*60+"\n"
			'''
			ret = ret + self.flushActEvent(vdi,prefix,lv,mode,prnDone)
			if   mode == 'var':
				#ret = ret + prefix + '<<Variable>>' + "\n"
				#ret = ret + self.printVar(vdi,prefix)
				pass
			#elif mode == 'event':
			#	ret = ret + prefix + '<<Event>>' + "\n"
		return ret

	def rmData(self,prnDone):
		for vxid in prnDone.values():
			del self.sess[vxid]
			del self.vxid[vxid]
	
	def flush(self,vxid):
		#val
		prnDone = {}
		self.flushSess(self.getRootVXID(vxid),1,'var',prnDone)
		#event
		print "\n"
		prnDone = {}
		self.flushSess(self.getRootVXID(vxid),1,'event',prnDone)
		print '-'*100
		print "\n"
		
		#flush
		self.rmData(prnDone)
		
		
	
	def printVal(self,k,v):
		print "%30s | %s" % (k,v)

	def printCenter(self,num,str):
		l  = len(str)
		ll = (num - l)/2
		rr = num - l - ll
		
		return (' '*ll + str + ' '*rr)
	########################################################################
	def fExistVXID(self, ttag, vxid, cbd):
		if vxid in self.sess:
			return 1
		return 0
	
	def getRootVXID(self,vxid):
		if self.sess[vxid][0] == None:
			return vxid
		return self.getRootVXID(self.sess[vxid][0])
	
	def __chkEndSess(self,vxid):
		if not vxid in self.sess:
			return 0
		sesslen = len(self.sess[vxid])
		if sesslen == 1 or self.sess[vxid][-1] != None:
			return 0
		elif sesslen == 2:
			return 1
		
		for v in self.sess[vxid][1:-1]:
			if self.__chkEndSess(v) == 0:
				return 0
		return 1

	def chkEndSess(self,vxid):
		vxidr = self.getRootVXID(vxid)
		return self.__chkEndSess(vxidr)
		
		
	########################################################################
	def fEnd(self, ttag, vxid, cbd):
		#vxid flush
		vd = self.vxid[vxid]
		ak = vd['actidx'][-1]
		vd['act'][ak]['fini'] = copy.deepcopy(vd['act']['temp']['init'])
		vd['act']['temp']['fini'] = {'var':{},'event':[]}
		
		
		ss = self.sess[vxid]
		ss.append(None)
		if self.chkEndSess(vxid):
			#Flush Data
			self.flush(vxid)
		return 1
	
	#初期化する
	def fBegin(self, ttag, vxid, cbd):
		vxidp = cbd['vxid_parent']
		#Start Session or Request
		if vxidp == 0:
			self.sess[vxid] = [None]
		else:
			self.sess[vxid] = [vxidp]
		self.vxid[vxid] = {'actidx':[], 'act':{},'actcur':'initial','actstat':'init'}
		self.vxid[vxid]['act']['temp']    = {'init':{'var':{},'event':[]},'work':{'var':{},'event':[]},'fini':{'var':{},'event':[]}}
		return 1
		
	def fLink(self, ttag, vxid, cbd):
		self.appendEvent(vxid,'Link',cbd['data'])
		#{'level': 1L, 'type': 'c', 'reason': 4, 'vxid_parent': 98889, 'length': 16L, 'tag': 73L, 'vxid': 98891, 'data': 'bereq 98892 pass', 'isbin': 0L}
		ss = self.sess[vxid]
		spl   = cbd['data'].split(' ', 2)
		ss.append(int(spl[1]))
		return 1
		
	def fVCLCall(self, ttag, vxid, cbd):
		self.appendEvent(vxid,'call',cbd['data'])
		
		vd = self.vxid[vxid]
		vd['actstat'] = 'work'
		vd['actcur']  = cbd['data']
		
		return 1
		
	def fVCLReturn(self, ttag, vxid, cbd):
		self.appendEvent(vxid,'return',cbd['data'])

		vd = self.vxid[vxid]
		vd['act'][vd['actcur']] = copy.deepcopy(vd['act']['temp'])
		vd['act']['temp'] = {'init':{'var':{},'event':[]},'work':{'var':{},'event':[]},'fini':{'var':{},'event':[]}}
		vd['actidx'].append(vd['actcur'])
		vd['actcur']  = None
		vd['actstat'] = 'init'
		return 1
		
	def fRequest(self, ttag, vxid, cbd):
		#{'level': 2L, 'type': 'c', 'reason': 2, 'vxid_parent': 1, 'length': 37L, 'tag': 27L, 'vxid': 2, 'data': 'X-Powered-By: PHP/5.3.10-1ubuntu3.13\x00', 'isbin': 0L}

		var  = self.vap.vut.tag2Var(ttag,cbd['data'])
		vkey = var['vkey']
		spl   = var['key'].split(' ')
		vn    = spl[-1]
		if spl[0] != 'unset':
			self.appendVar(vxid,vn,var['val'])
		else:
			self.appendVar(vxid,vn,None)
		return 1

	def fEventStor(self, ttag, vxid, cbd):
		#default stor 
		self.appendEvent(vxid,ttag,cbd['data'])
		return 1

		
	


'''
       Timestamp - Timing information
              Contains timing information for the Varnish worker threads.

              Time stamps are issued by Varnish on certain events, and show the absolute time of the event, the time spent since the start of the work unit, and the time spent since the last timestamp was logged. See vsl(7)
              for information about the individual timestamps.

              The format is:

              %s: %f %f %f
              |   |  |  |
              |   |  |  +- Time since last timestamp
              |   |  +---- Time since start of work unit
              |   +------- Absolute time of event
              +----------- Event label


・貼られたrawログからsessionを復元するロジックは作る(raw2session)
・ヘッダはスタック格納

SessionOoen
 |+ http://xxx/xxx/
 ||+<<vcl_recv>>
 |||+req.url = hoge
 |||+req.url = hoge
 |||+req.url = hoge -> XXX -> CCC
 ||
 ||+<<vcl_recv>>
 |||+req.url = hoge
 |||+req.url = hoge
 |||+req.url = hoge
 ||
 ||+<<vcl_recv>>
 |||+req.url = hoge
 |||+req.url = hoge
 |||+req.url = hoge

'''
