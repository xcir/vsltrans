# coding: utf-8
import varnishapi

import threading,time,signal,copy,sys,re,os,time,binascii


class log2vsl:
	def __init__(self):
		self.raw  = []
		self.data = {}
		self.parse = None

	def chkFmt(self):
		re_session = re.compile(r"^\* +<< +Session +>>")
		re_request = re.compile(r"^--")
		re_raw     = re.compile(r"^ *\d+ [A-Z]")
		
		haslv = 0
		for line in self.raw:
			if  re_raw.match(line):
				self.parse = self.parseRaw
				return
			elif '<<' in line:
				if re_session.match(line) and haslv:
					self.parse = self.parseSession
					return
			elif re_request.match(line):
				haslv = 1
		if haslv:
			self.parse = self.parseRequest
			return
		self.parse = self.parseVXID
		return
		'''
		RAW
		    100070 Begin          c sess 0 HTTP/1
		SESSION
		*   << Session  >> 34477     
		-   Begin          sess 0 HTTP/1
		REQUEST(has lv2 line)
		*   << Request  >> 100078    
		-   Begin          req 100077 rxreq
		VXID
		other
		'''
		#Debug  {'level': 1L, 'type': 'c', 'reason': 2, 'vxid_parent': 0, 'length': 12L, 'tag': 1L, 'vxid': 34485, 'data': 'RES_MODE 18\x00', 'isbin': 2L}
	def parseSession(self):
		r  = re.compile(r"^[-0-9]+ +([^ ]+) +(.*)$")
		rh = re.compile(r"^[\*0-9]+ +<< +([^ ]+) +>> +(\d+) *$")
		vxid  = 0
		pvxid = 0
		for line in self.raw:
			m = r.match(line)
			if not m:
				m = rh.match(line)
				if not m:
					continue
				vxid = int(m.group(2))
				continue
			ttag = m.group(1)
			data = m.group(2)
			if ttag == 'Begin':
				pvxid = int(data.split(' ',3)[1])
			if vxid not in self.data:
				self.data[vxid] = []
			self.data[vxid].append({'ttag':ttag,'pvxid':pvxid,'cbd':{'level':1,'type':None,'reason':None,'vxid_parent':pvxid,'length':len(data),'tag':None,'vxid':vxid,'data':data,'isbin':0}})
			
	def parseRequest(self):
		r  = re.compile(r"^[-0-9]+ +([^ ]+) +(.*)$")
		rh = re.compile(r"^[\*0-9]+ +<< +([^ ]+) +>> +(\d+) *$")
		vxid  = 0
		pvxid = 0
		for line in self.raw:
			m = r.match(line)
			if not m:
				m = rh.match(line)
				if not m:
					continue
				vxid = int(m.group(2))
				continue
			ttag = m.group(1)
			data = m.group(2)
			if ttag == 'Begin':
				spl = data.split(' ',3)
				if spl[0]=='req' and spl[2]=='rxreq':
					pvxid = 0
				else:
					pvxid = int(spl[1])
			if vxid not in self.data:
				self.data[vxid] = []
			self.data[vxid].append({'ttag':ttag,'pvxid':pvxid,'cbd':{'level':1,'type':None,'reason':None,'vxid_parent':pvxid,'length':len(data),'tag':None,'vxid':vxid,'data':data,'isbin':0}})

	def parseVXID(self):
		r  = re.compile(r"^- +([^ ]+) +(.*)$")
		rh = re.compile(r"^\* +<< +([^ ]+) +>> +(\d+) *$")
		vxid  = 0
		pvxid = 0
		for line in self.raw:
			m = r.match(line)
			if not m:
				m = rh.match(line)
				if not m:
					continue
				vxid = int(m.group(2))
				continue
			ttag = m.group(1)
			data = m.group(2)
			if ttag == 'Begin':
				pvxid = int(data.split(' ',3)[1])
			if vxid not in self.data:
				self.data[vxid] = []
			self.data[vxid].append({'ttag':ttag,'pvxid':pvxid,'cbd':{'level':1,'type':None,'reason':None,'vxid_parent':pvxid,'length':len(data),'tag':None,'vxid':vxid,'data':data,'isbin':0}})
			
	def parseRaw(self):
		#    100073 Timestamp      c Process: 1435425931.782784 1.000796 0.000036
		r = re.compile(r"^ *(\d+) ([^ ]+) +([^ ]) (.*)$")
		pvxid=0
		for line in self.raw:
			m = r.match(line)
			if not m:
				continue
			vxid = int(m.group(1))
			if vxid==0:
				#CLI
				continue
			ttag = m.group(2)
			type = m.group(3)
			data = m.group(4)
			if ttag == 'Begin':
				pvxid = int(data.split(' ',3)[1])
			
			if vxid not in self.data:
				self.data[vxid] = []
			self.data[vxid].append({'ttag':ttag,'pvxid':pvxid,'cbd':{'level':1,'type':type,'reason':None,'vxid_parent':pvxid,'length':len(data),'tag':None,'vxid':vxid,'data':data,'isbin':0}})
			
	def read(self,file):
		self.raw   = []
		self.parse = None
		self.data  = {}
		if not os.path.exists(file):
			return 0
		f = open(file)
		for line in f.readlines():
			self.raw.append(line)
		f.close()
		self.chkFmt()
		self.parse()

class vslTrans4:
	def dataClear(self):
		self.sess  = {}
		self.vxid  = {}
		

	def __init__(self, opts):
		
		#self.debug = 1
		self.debug = 0
		self.mode = 'request'
		#self.mode = 'session'
		
		self.source = 'vsl'
		
		#一旦requestで、sessionも対応する
		vops = ['-g',self.mode]
		if isinstance(opts, list):
			for o,a in opts:
				if   o == '-q':
					vops.append(o)
					vops.append(a)
				elif o == '-f':
					self.source = 'file'
					self.file   = log2vsl()
					self.file.read(a)
		self.vap     = varnishapi.VarnishLog(vops)
		if self.vap.error:
			print self.vap.error
			exit(1)
		self.vslutil = varnishapi.VSLUtil()
		self.dataClear()
		self.__transWrd = {
			'init':'Before vcl funciton',
			'work':'In vcl function',
			'fini':'After vcl function',
		}
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
			'SessClose':	[self.fExistVXID, self.fVCLReturn],

			'Timestamp':	[self.fExistVXID, self.fTimestamp],
			'__default':	[self.fExistVXID, self.fEventStor],

		}
		
	
	def execute(self):
		if self.source == 'vsl':
			while 1:
				#dispatch
				#self.state = 0
				ret = self.vap.Dispatch(self.vapCallBack)
				if 0 == ret:
					time.sleep(0.1)
		else:
			for v in self.file.data.values():
				for data in v:
					self.filter(data['ttag'],data['cbd'])
				
	def vapCallBack(self, vap, cbd, priv):
		if not cbd['isbin']:
			cbd['length'] = cbd['length'] -1;
			cbd['data']   = cbd['data'][:-1]
			
		ttag = vap.VSL_tags[cbd['tag']]
		self.filter(ttag,cbd)
	
	def filter(self,ttag,cbd):
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
		rv = self.rebuildVar(vdi,19)
		if len(rv['val']) ==0:
			return ''
		tmp =  '+-' +('-'* rv['keysz']) + '-+-'
		sar = ['init','work','fini']
		for step in sar:
			tmp = tmp + ('-'* rv['size'][step]) + '-+-'
		line = prefix + tmp[:-1]
		ret = ret + line + "\n"
		
		tmp =  '| ' +("%" + str(rv['keysz']) + "s | ")  % 'key'
		for step in sar:
			wrd = self.__transWrd[step]
			tmp = tmp + self.printCenter(rv['size'][step],wrd) + " | "
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
	
	def printEvent(self,prefix,sp,max,k,v):
		return prefix + sp + (("%"+str(max)+"s | %s") % (k,v)) + "\n"
	
	def flushActEvent(self,vdi,prefix,lv,mode,prnDone):
		sk = ['init','work','fini']
		ret = ''
		sp  = ' '*3+'| '
		
		max = 15
		if mode == 'event':
			for step in sk:
				for v in vdi[step]['event']:
					l = len(v['k'])
					if l > max:
						max = l
		
		for step in sk:
			for v in vdi[step]['event']:
				if v['k'] == 'Link':
					ret = ret + self.printEvent(prefix,sp,max,'','')
					if mode == 'event':
						ret = ret + self.printEvent(prefix,sp,max,v['k'],v['v'])
					spl = v['v'].split(' ', 2)
					lvxid = int(spl[1])
					prnDone[lvxid]=lvxid
					if spl[2] == 'restart':
						ret = ret + self.printBox(prefix,'#',"RESTART",1)
						ret = ret + self.flushAct(lvxid, '' ,lv,mode,prnDone)
					if spl[2] == 'esi':
						ret = ret + self.printBox(prefix+sp+' '*max + " > ",'#',"ESI",1)
						ret = ret + self.flushAct(lvxid, prefix+sp+' '*max + " > " ,lv+1,mode,prnDone)
					else:
						ret = ret + self.flushAct(lvxid, prefix+sp+' '*max + " > " ,lv+1,mode,prnDone)
				elif v['k'] == 'call':
					#if mode == 'event':
					#	ret = ret + self.printEvent(prefix,sp,max,v['k'],v['v'])
					ret = ret + prefix + sp + "\n"
					ret = ret + self.printBox(prefix,'>',"vcl_%s" % (v['v'].lower()))
				elif v['k'] == 'return':
					if   mode == 'var':
						ret = ret + prefix + sp + "\n"
						ret = ret + self.printVar(vdi,prefix + sp)
					else:
						ret = ret + self.printEvent(prefix,sp,max,'','')
						ret = ret + self.printEvent(prefix,sp,max,v['k'],v['v'])
						ret = ret + prefix + sp + "\n"
					#	ret = ret + self.printBox(prefix + ' '*3,'<',"return(%s)" % (v['v'].lower()))
					#	ret = ret + prefix + sp + "\n"
				elif mode == 'event':
					ret = ret + self.printEvent(prefix,sp,max,v['k'],v['v'])

		return ret
			
	def printBox(self,prefix,wrd,txt,rmode=0,sz=40):
		ret = prefix + wrd*sz+"\n"
		ret = ret + prefix + wrd + self.printCenter(sz-2,txt)+wrd+"\n"
		if not rmode:
			ret = ret + prefix + wrd*sz+"\n"
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
			
	def printCenter(self,num,str):
		l  = len(str)
		ll = (num - l)/2
		rr = num - l - ll
		
		return (' '*ll + str + ' '*rr)
		
	def flush(self,vxid):
		#val
		prnDone = {}
		print self.printBox('','*','Variable',0,60)

		print self.printBox('','#','Start',1),
		self.flushSess(self.getRootVXID(vxid),1,'var',prnDone)
		#event
		print "\n"
		prnDone = {}
		print self.printBox('','*','Event',0,60)
		print self.printBox('','#','Start',1),
		self.flushSess(self.getRootVXID(vxid),1,'event',prnDone)
		print '-'*100
		print "\n"
		#flush
		self.rmData(prnDone)
	
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
	def fTimestamp(self, ttag, vxid, cbd):
		vd = self.vxid[vxid]
		spl  = cbd['data'].split(':',1);
		spl2 = spl[1].split(' ',3)
		vd['timestamp'].append({'k':spl[0],'abs':spl2[1],'offset':spl2[3]})
		spl3 = vd['timestamp'][-1]['abs'].split('.',2)
		
		val = spl[0] + ': '+time.strftime('%Y/%m/%d %H:%M:%S.', time.gmtime(int(spl3[0]))) + spl3[1] + ' GMT (last +' + vd['timestamp'][-1]['offset']+'s)'
		self.appendEvent(vxid,ttag,val)
		return 1
	
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
		self.vxid[vxid] = {'actidx':[], 'act':{},'actcur':'initial','actstat':'init','timestamp':[]}
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
		#todo:わざわざ名前変えるか再検討(vcl_returnに戻す？VCL表記に合わす？）
		if ttag == 'VCL_return':
			ttag = 'return'
		self.appendEvent(vxid,ttag,cbd['data'])


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
		if cbd['isbin']:
			self.appendEvent(vxid,ttag,"(0x%s) %s" % (binascii.hexlify(cbd['data']),cbd['data']))
		else:
			self.appendEvent(vxid,ttag,cbd['data'])
		return 1

		
	
'''
todo:
サマリ表示をいれるかどうか考えとく
----------------------------------------
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
          timestamp:[
            {'k':'Process','abs':1435412407.697665,'offset':0.000042}
          ]
      },
  }


self.vxid[vxid] = {'actidx':[], 'act':{},'actcur':'initial','actnxt':None,'actstat':'init','timestamp':[]}
actcur = 現在のアクション
actnxt = 次のアクション(vcl_callで変更）
actstat= 初期状態なのかwork状態なのか

'''


