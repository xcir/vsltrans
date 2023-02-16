# coding: utf-8
import varnishapi

import threading,time,copy,sys,re,os,time,binascii,json,hashlib


class v4filter:
    def dataClear(self):
        self.sess  = {}
        self.vxid  = {}

    def __init__(self, opts, vut,outcb):
        self.vut = vut
        self.outcb = outcb
        self.debug = 0
        self.dataClear()

        if isinstance(opts, list):
            for o,a in opts:
                if o == '--debug':
                    self.debug = 1
        self.__filter = {
            'ReqURL':        [self.fExistVXID, self.fRequest],
            'ReqStart':        [self.fExistVXID, self.fRequest],
            'ReqMethod':    [self.fExistVXID, self.fRequest],
            'ReqProtocol':    [self.fExistVXID, self.fRequest],
            'ReqHeader':    [self.fExistVXID, self.fRequest],
            'ReqUnset':        [self.fExistVXID, self.fRequest],

            'BereqURL':            [self.fExistVXID, self.fRequest],
            'BereqMethod':        [self.fExistVXID, self.fRequest],
            'BereqProtocol':    [self.fExistVXID, self.fRequest],
            'BereqHeader':        [self.fExistVXID, self.fRequest],
            'BereqUnset':        [self.fExistVXID, self.fRequest],

            'BerespHeader':        [self.fExistVXID, self.fRequest],
            'BerespUnset':        [self.fExistVXID, self.fRequest],
            'BerespProtocol':    [self.fExistVXID, self.fRequest],
            'BerespStatus':        [self.fExistVXID, self.fRequest],
            'BerespReason':        [self.fExistVXID, self.fRequest],

            'RespHeader':    [self.fExistVXID, self.fRequest],
            'RespUnset':    [self.fExistVXID, self.fRequest],
            'RespProtocol':    [self.fExistVXID, self.fRequest],
            'RespStatus':    [self.fExistVXID, self.fRequest],
            'RespReason':    [self.fExistVXID, self.fRequest],

            'ObjHeader':    [self.fExistVXID, self.fRequest],
            'ObjUnset':        [self.fExistVXID, self.fRequest],
            'ObjProtocol':    [self.fExistVXID, self.fRequest],
            'ObjStatus':    [self.fExistVXID, self.fRequest],
            'ObjReason':    [self.fExistVXID, self.fRequest],


            'Begin':        self.fBegin,
            'End':            [self.fExistVXID, self.fEnd],
            'Link':            [self.fExistVXID, self.fLink],
            'VCL_call':        [self.fExistVXID, self.fVCLCall],
            'VCL_return':    [self.fExistVXID, self.fVCLReturn],
            'SessClose':    [self.fExistVXID, self.fVCLReturn],

            'Timestamp':    [self.fExistVXID, self.fTimestamp],
            '__default':    [self.fExistVXID, self.fEventStor],
        }
    def filter(self,ttag,cbd):
        vxid = cbd['vxid']
        key = ttag

        if key not in self.__filter:
            key = '__default'
            if self.debug:
                print("%15s " % ttag,)
                print(cbd)

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


    def rmData(self,prnDone):
        for vxid in prnDone.values():
            del self.sess[vxid]
            del self.vxid[vxid]


    ########################################################################
    def fExistVXID(self, ttag, vxid, cbd):
        if vxid in self.sess:
            return 1
        return 0
    
    def getRootVXID(self,vxid):
        if vxid not in self.sess:
            return None
        if self.sess[vxid][0] is None:
            return vxid
        return self.getRootVXID(self.sess[vxid][0])
    
    def __chkEndSess(self,vxid):
        if not vxid in self.sess:
            return 0
        sesslen = len(self.sess[vxid])
        if sesslen == 1 or self.sess[vxid][-1] is not None:
            return 0
        elif sesslen == 2:
            return 1
        
        for v in self.sess[vxid][1:-1]:
            if self.__chkEndSess(v) == 0:
                return 0
        return 1

    def chkEndSess(self,vxid):
        vxidr = self.getRootVXID(vxid)
        if vxid is None:
            #incomplete data
            return 1
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
        if len(vd['actidx']) == 0:
            #強制フラッシュ
            self._fVCLReturn(ttag, vxid, cbd)

        ak = vd['actidx'][-1]
        vd['act'][ak]['fini'] = copy.deepcopy(vd['act']['temp']['init'])
        vd['act']['temp']['fini'] = {'var':{},'event':[]}
        
        
        ss = self.sess[vxid]
        ss.append(None)
        if self.chkEndSess(vxid):
            #Flush Data
            self.rmData(self.outcb(self.sess,self.vxid,vxid,self.getRootVXID(vxid)))
            
            #self.flush(vxid)
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
        self.appendEvent(vxid,ttag,cbd['data'])
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

    def _fVCLReturn(self, ttag, vxid, cbd):
        vd = self.vxid[vxid]
        vd['act'][vd['actcur']] = copy.deepcopy(vd['act']['temp'])
        vd['act']['temp'] = {'init':{'var':{},'event':[]},'work':{'var':{},'event':[]},'fini':{'var':{},'event':[]}}
        vd['actidx'].append(vd['actcur'])
        vd['actcur']  = None
        vd['actstat'] = 'init'

    def fVCLReturn(self, ttag, vxid, cbd):
        #todo:わざわざ名前変えるか再検討(vcl_returnに戻す？VCL表記に合わす？）
        if ttag == 'VCL_return':
            ttag = 'return'
        self.appendEvent(vxid,ttag,cbd['data'])
        self._fVCLReturn(ttag, vxid, cbd)

        return 1

    def fRequest(self, ttag, vxid, cbd):
        #{'level': 2L, 'type': 'c', 'reason': 2, 'vxid_parent': 1, 'length': 37L, 'tag': 27L, 'vxid': 2, 'data': 'X-Powered-By: PHP/5.3.10-1ubuntu3.13\x00', 'isbin': 0L}

        var  = self.vut.tag2Var(ttag,cbd['data'])
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

class im2DOT():
    def __init__(self):
        self.kx = ['init', 'work', 'fini']
    def getAllSess(self, ret, vxid):
        for v in self.sess[vxid]:
            if v is not None and v != vxid and v not in ret:
                 ret[v] = v
                 self.getAllSess(ret,v)
    def prnHeader(self):
        ret = \
'''
digraph graph_%d {
  node [
    shape = record,
    fontsize = 9,
  ];
  graph [
    rankdir = TB,
  ];
%s
}
''' % (self.rootVxid,self.dot)
       
        return ret.replace("\n"," ")
    def add(self,txt,ind=1):
        self.dot += '  ' * ind + txt
    def getHash(self,txt):
        return hashlib.sha256(txt).hexdigest()
    def __genDOT(self):
        #client ip
        clip = ''
        if 'RECV' in self.vxid[self.rootVxid]['act']:
            clip = self.vxid[self.rootVxid]['act']['RECV']['init']['var']['client.ip'][0];
        elif 'initial' in self.vxid[self.rootVxid]['act']:
            #session data. check to next vxid
            clip = self.vxid[self.sess[self.rootVxid][1]]['act']['RECV']['init']['var']['client.ip'][0];
        self.add("Client%d [shape = oval, label = \"client\l%s\"];\n" % (self.rootVxid, clip))
        self.add("Client%d -> VCL_start_%d\n" %(self.rootVxid, self.rootVxid))
        
        #external link(ex:Storage, Backend Link)
        ext    = {'storage':{},'backend':{}}
        extlnk = {'storage':[],'backend':[]}
        for vxid in self.sr.keys():
            v = self.vxid[vxid]
            act = ''
            curact = 0
            actidx = v['actidx']
            retidx = {}
            lnk    = []
            session = 1
            host = ''
            url  = ''
            begin= ['','','']
            if 'temp' in v['act']:
                del v['act']['temp']
            if 'RECV' in v['act']:
                if 'req.http.Host' in v['act']['RECV']['init']['var']:
                    host = v['act']['RECV']['init']['var']['req.http.Host'][0]
                if 'req.url' in v['act']['RECV']['init']['var']:
                    url = "%s %s %s" % (
                        v['act']['RECV']['init']['var']['req.method'][0],
                        v['act']['RECV']['init']['var']['req.url'][0],
                        v['act']['RECV']['init']['var']['req.proto'][0]
                        )
                if v['act']['RECV']['init']['event'][0]['k'] == 'Begin':
                    begin = v['act']['RECV']['init']['event'][0]['v'].split(' ')
                session = 0
            elif 'BACKEND_FETCH' in v['act']:
                if 'bereq.http.Host' in v['act']['BACKEND_FETCH']['init']['var']:
                    host = v['act']['BACKEND_FETCH']['init']['var']['bereq.http.Host'][0]
                if 'bereq.url' in v['act']['BACKEND_FETCH']['init']['var']:
                    url = "%s %s %s" % (
                        v['act']['BACKEND_FETCH']['init']['var']['bereq.method'][0],
                        v['act']['BACKEND_FETCH']['init']['var']['bereq.url'][0],
                        v['act']['BACKEND_FETCH']['init']['var']['bereq.proto'][0]
                        )
                if v['act']['BACKEND_FETCH']['init']['event'][0]['k'] == 'Begin':
                    begin = v['act']['BACKEND_FETCH']['init']['event'][0]['v'].split(' ')
                session = 0
            elif 'PIPE' in v['act']:
                if 'bereq.http.Host' in v['act']['PIPE']['init']['var']:
                    host = v['act']['PIPE']['init']['var']['bereq.http.Host'][0]
                if 'bereq.url' in v['act']['PIPE']['init']['var']:
                    url = "%s %s %s" % (
                        v['act']['BACKEND_FETCH']['init']['var']['bereq.method'][0],
                        v['act']['BACKEND_FETCH']['init']['var']['bereq.url'][0],
                        v['act']['BACKEND_FETCH']['init']['var']['bereq.proto'][0]
                        )
                if v['act']['PIPE']['init']['event'][0]['k'] == 'Begin':
                    begin = v['act']['PIPE']['init']['event'][0]['v'].split(' ')
                session = 0
            else:
                if v['act']['initial']['init']['event'][0]['k'] == 'Begin':
                    begin = v['act']['initial']['init']['event'][0]['v'].split(' ')
            sg = \
"""subgraph cluster_vxid_%d {
    label = "VXID: %d TYPE:%s\\nPARENT: %s REASON:%s";
labelloc = "t";
""" % (vxid, vxid,begin[0],begin[1],begin[2])
            for action,vv in v['act'].items():
                i = 0
                tmp = "  VCL_%s_%d [shape = none; label = <<table border=\"0\" cellspacing=\"0\">" % (action, vxid)
                tmp += "<tr><td port=\"head\" border=\"1\" bgcolor=\"#bbbbff\">%s</td></tr>" % (action)
                #search for init,work,fini
                skipret = 0
                for key in self.kx:
                    for vvv in vv[key]['event']:
                        i+=1
                        vkey = vvv['k']
                        vval = vvv['v']
                        color = "";
                        if vkey == 'return':
                            color = " bgcolor=\"#eeeeff\""
                            if vval == 'restart' or vval == 'retry':
                                skipret = 1
                        elif vkey == 'Link':
                            color = " bgcolor=\"#eeffee\""
                            lnk.append([action, i, int(vval.split(' ')[1])])
                        elif vkey == 'call':
                            color = " bgcolor=\"#eeeeff\""
                            vkey = 'Execute'
                            vval = "vcl_" + vval.lower()
                        elif vkey == 'Storage':
                            ext['storage'][self.getHash(vval)] = vval
                            extlnk['storage'].append([action, vxid, i, vval])
                        elif vkey == 'BackendOpen':
                            spl = vval.split(' ', 3)
                            del spl[-2:]
                            vt = ' '.join(spl)
                            ext['backend'][self.getHash(vval)] = vt
                            extlnk['backend'].append([action, vxid, i, vt])
                        elif vkey == 'Backend':
                            spl = vval.split(' ')
                            del spl[1]
                            vt = ' '.join(spl)
                            if len(extlnk['backend']) >0:
                                el=extlnk['backend'][-1]
                                if not(
                                   el[0] == action and
                                   el[1] == vxid and
                                   el[3] == vt):
                                    ext['backend'][self.getHash(vval)] = vt
                                    extlnk['backend'].append([action, vxid, i, vt])
                                
                            else:
                                ext['backend'][self.getHash(vval)] = vt
                                extlnk['backend'].append([action, vxid, i, vt])
                        elif vkey == 'Error' or vkey == 'FetchError':
                            color = " bgcolor=\"#ffaaaa\""
                        tmp+="<tr><td %s port=\"%d\" border=\"1\">%s:<br/>%s</td></tr>" % (color, i, vkey, vval.replace('&','&amp;').replace('"','&quot;').replace('<','&lt;').replace('>','&gt;'))
                if not skipret:
                    retidx[action] = i
                tmp += "</table>> ]"
                sg += tmp
                
            act += "VCL_start_%d -> VCL_%s_%d:head\n" % (vxid, actidx[0], vxid)
            #if actidx[-1] != 'start':
            #    actidx.append('start')
            if retidx:
                for i in range(0, len(actidx) -1):
                    action = actidx[i]
                    if action not in retidx:
                        continue
                    ri = retidx[action]
                    port = ''
                    if actidx[i+1] != 'start':
                        port=':head'
                    act+="VCL_%s_%d:%d -> VCL_%s_%d%s\n" % (action, vxid, ri, actidx[i+1], vxid,port)
            lt = ''
            for l in lnk:
                lt += "VCL_%s_%d:%d -> VCL_start_%d \n" % (l[0], vxid, l[1], l[2])
            if session:
                self.add("VCL_start_%d [label=\"Session\", style=filled];\n" % (vxid))
            else:
                self.add("VCL_start_%d [label=\"%s\lhost: %s\l\", style=filled];\n" % (vxid, url, host))
            self.add(sg)
            self.add(act)
            self.add("};\n")
            self.add(lt)
        exs = ''
        for k,v in ext.items():
            if not v:
                continue
            exs += \
'''
subgraph cluster_%s {
    label = "%s";
    labeljust = "l";
''' % (k,k)
            for l in v.values():
                exs += "%s_%s [label = \"%s\"];\n" % (k,self.getHash(l),l)
            exs += "}\n"
            for l in extlnk[k]:
                exs += "VCL_%s_%d:%d -> %s_%s\n" % (l[0],l[1],l[2],k,self.getHash(l[3]))
        self.add(exs)
    def genDOT(self,sessar,vxidar,vxid,rootVxid):
        self.dot      = ''
        self.sess     = sessar
        self.vxid     = vxidar
        self.rootVxid = rootVxid
        self.sr       = {}
        self.getAllSess(self.sr, rootVxid)
        if len(self.sr) == 0:
            self.sr = {rootVxid:rootVxid}
        self.__genDOT()
        return self.prnHeader()
    
    def getData(self,sessar,vxidar,vxid,rootVxid):
        print(self.genDOT(sessar,vxidar,vxid,rootVxid))
        return self.sr

class im2JSON():
    def __init__(self):
        self.f_dot = 0
            
    def setDOT(self):
        self.f_dot  = 1
        self.im2dot = im2DOT()

    def getAllSess(self, ret, vxid):
        for v in self.sess[vxid]:
            if v is not None and v != vxid and v not in ret:
                 ret[v] = v
                 self.getAllSess(ret,v)
                 
    def getData(self,sessar,vxidar,vxid,rootVxid):
        self.sess = sessar
        self.vxid = vxidar
        sr = {}
        self.getAllSess(sr, rootVxid)
        if len(sr) == 0:
            sr = {rootVxid:rootVxid}
        ret = {"rootVxid": rootVxid,"sess":{},"vxid":{}}
        for v in sr:
            ret["sess"][v] = self.sess[v]
            ret["vxid"][v] = self.vxid[v]
            del ret["vxid"][v]['act']['temp']
        if self.f_dot:
            ret["dot"] = self.im2dot.genDOT(sessar,vxidar,vxid,rootVxid)
        print(json.dumps(ret))
        return sr
        
    
class im2CLI():
    def __init__(self):
        self.__transWrd = {
            'init':'Before vcl funciton',
            'work':'In vcl function',
            'fini':'After vcl function',
        }

    def getData(self,sessar,vxidar,vxid,rootVxid):
        self.sess = sessar
        self.vxid = vxidar
        return self.flush(vxid,rootVxid)
        #        self.rmData(prnDone)
        
    def flushSess(self,vxid,lv,mode,prnDone):
        ret = ''
        if vxid not in prnDone:
            ret += self.flushAct(vxid,'',lv,mode,prnDone)
            prnDone[vxid] = vxid
        for v in self.sess[vxid][1:-1]:
            ret += self.flushSess(v,lv+1,mode,prnDone)
        return ret
        
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
                    if vvv is None:
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
        ret += line + "\n"
        
        tmp =  '| ' +("%" + str(rv['keysz']) + "s | ")  % 'key'
        for step in sar:
            wrd = self.__transWrd[step]
            tmp = tmp + self.printCenter(rv['size'][step],wrd) + " | "
            #tmp = tmp + ("%" + str(rv['size'][step]) + "s | ")  % step
        ret += prefix + tmp + "\n"
        ret += line + "\n"
        
        
        for vk, vv in sorted(rv['val'].items()):
            tmp =  '| '+("%" + str(rv['keysz']) + "s | ")  % vk
            for step in sar:
                vvv = vv[step]
                tmp = tmp + ("%-" + str(rv['size'][step]) + "s | ")  % vvv
            ret += prefix + tmp + "\n"
        ret += line + "\n"
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
                    ret += self.printEvent(prefix,sp,max,'','')
                    if mode == 'event':
                        ret += self.printEvent(prefix,sp,max,v['k'],v['v'])
                    spl = v['v'].split(' ', 2)
                    lvxid = int(spl[1])
                    prnDone[lvxid]=lvxid
                    if spl[2] == 'restart':
                        ret += self.printBox(prefix,'#',"RESTART",1)
                        ret += self.flushAct(lvxid, '' ,lv,mode,prnDone)
                    if spl[2] == 'esi':
                        ret += self.printBox(prefix+sp+' '*max + " > ",'#',"ESI",1)
                        ret += self.flushAct(lvxid, prefix+sp+' '*max + " > " ,lv+1,mode,prnDone)
                    else:
                        ret += self.flushAct(lvxid, prefix+sp+' '*max + " > " ,lv+1,mode,prnDone)
                elif v['k'] == 'call':
                    #if mode == 'event':
                    #    ret += self.printEvent(prefix,sp,max,v['k'],v['v'])
                    ret += prefix + sp + "\n"
                    ret += self.printBox(prefix,'>',"vcl_%s" % (v['v'].lower()))
                elif v['k'] == 'return':
                    if   mode == 'var':
                        ret += prefix + sp + "\n"
                        ret += self.printVar(vdi,prefix + sp)
                    else:
                        ret += self.printEvent(prefix,sp,max,'','')
                        ret += self.printEvent(prefix,sp,max,v['k'],v['v'])
                        ret += prefix + sp + "\n"
                    #    ret += self.printBox(prefix + ' '*3,'<',"return(%s)" % (v['v'].lower()))
                    #    ret += prefix + sp + "\n"
                elif mode == 'event':
                    ret += self.printEvent(prefix,sp,max,v['k'],v['v'])

        return ret
            
    def printBox(self,prefix,wrd,txt,rmode=0,sz=40):
        ret = prefix + wrd*sz+"\n"
        ret += prefix + wrd + self.printCenter(sz-2,txt)+wrd+"\n"
        if not rmode:
            ret += prefix + wrd*sz+"\n"
        return ret
    
    def flushAct(self,vxid,prefix,lv,mode,prnDone):
        ret = self.printBox(prefix,'#',"VXID:%d" % vxid)
        #ret =  prefix + "<<VXID:%d>>\n" % vxid
        vd = self.vxid[vxid]
        for k in vd['actidx']:
            vdi = vd['act'][k]
            retval = self.searchKey('return',vdi['work']['event'])
            '''
            ret += prefix + '#'*60+"\n"
            ret += prefix + '#' + self.printCenter(58,"vcl_%s / return(%s)" % (k.lower(),retval))+"#\n"
            ret += prefix + '#'*60+"\n"
            '''
            ret += self.flushActEvent(vdi,prefix,lv,mode,prnDone)
            if   mode == 'var':
                #ret += prefix + '<<Variable>>' + "\n"
                #ret += self.printVar(vdi,prefix)
                pass
            #elif mode == 'event':
            #    ret += prefix + '<<Event>>' + "\n"
        return ret
    def printCenter(self,num,str):
        l  = len(str)
        ll = int((num - l)/2)
        rr = num - l - ll
        
        return (' '*ll + str + ' '*rr)
        
    def flush(self,vxid,rootVxid):
        #val
        prnDone = {}
        ret = ''
        ret += self.printBox('','*','Variable',0,60)

        ret += self.printBox('','#','Start',1)
        ret += self.flushSess(rootVxid,1,'var',prnDone)
        #event
        ret += "\n"
        prnDone = {}
        ret += self.printBox('','*','Event',0,60)
        ret += self.printBox('','#','Start',1)
        ret += self.flushSess(rootVxid,1,'event',prnDone)
        ret += '-'*100
        ret += "\n"
        print(ret)
        #flush
        return prnDone
    def searchKey(self,k,ar):
        for v in ar:
            if v['k'] == k:
                return v['v']
        return ''

class log2chunk(v4filter):
    def __init__(self,opts,outcb):
        self.__raw      = []
        self.data       = {}
        self.parse      = None
        self.fmtversion = 0
        self.fname      = ''
        if isinstance(opts, list):
            for o,a in opts:
                if o == '-f':
                    self.source = 'file'
                    self.fname  = a
        v4filter.__init__(self,opts, varnishapi.VSLUtil(),outcb)

    def chkFmt(self):
        re_session = re.compile(r"^\* +<< +Session +>>")
        re_request = re.compile(r"^--")
        re_raw     = re.compile(r"^ *\d+ [A-Z]")
        re_raw_v3  = re.compile(r"^ *\d+ (Rx|Tx)")
        haslv = 0

        # default version
        self.fmtversion = 4

        for line in self.__raw:
            if  re_raw.match(line):
                self.parse = self.parseRaw
                # version detect(3/4)
                for l in self.__raw:
                    if re_raw_v3.match(l):
                        self.fmtversion = 3
                        return
                return
            elif '<<' in line:
                if re_session.match(line):
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
        r2  = re.compile(r"^[-0-9]+ +([^ ]+)$")
        rh = re.compile(r"^[\*0-9]+ +<< +([^ ]+) +>> +(\d+) *$")
        vxid  = 0
        pvxid = 0
        for line in self.__raw:
            m = r.match(line)
            data = ''
            if not m:
                m = r2.match(line)
            else:
                data = m.group(2)
            if not m:
                m = rh.match(line)
                if not m:
                    continue
                vxid = int(m.group(2))
                continue
            ttag = m.group(1)
            if ttag == 'Begin':
                pvxid = int(data.split(' ',3)[1])
            if vxid not in self.data:
                self.data[vxid] = []
            self.data[vxid].append({'ttag':ttag,'pvxid':pvxid,'cbd':{'level':1,'type':None,'reason':None,'vxid_parent':pvxid,'length':len(data),'tag':None,'vxid':vxid,'data':data,'isbin':0}})
            
    def parseRequest(self):
        r  = re.compile(r"^[-0-9]+ +([^ ]+) +(.*)$")
        r2  = re.compile(r"^[-0-9]+ +([^ ]+)$")
        rh = re.compile(r"^[\*0-9]+ +<< +([^ ]+) +>> +(\d+) *$")
        vxid  = 0
        pvxid = 0
        for line in self.__raw:
            m = r.match(line)
            data = ''
            if not m:
                m = r2.match(line)
            else:
                data = m.group(2)
            if not m:
                m = rh.match(line)
                if not m:
                    continue
                vxid = int(m.group(2))
                continue
            ttag = m.group(1)
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
        r2  = re.compile(r"^- +([^ ]+)$")
        rh = re.compile(r"^\* +<< +([^ ]+) +>> +(\d+) *$")
        vxid  = 0
        pvxid = 0
        for line in self.__raw:
            m = r.match(line)
            data = ''
            if not m:
                m = r2.match(line)
            else:
                data = m.group(2)
            if not m:
                m = rh.match(line)
                if not m:
                    continue
                vxid = int(m.group(2))
                continue
            ttag = m.group(1)
            if ttag == 'Begin':
                pvxid = int(data.split(' ',3)[1])
            if vxid not in self.data:
                self.data[vxid] = []
            self.data[vxid].append({'ttag':ttag,'pvxid':pvxid,'cbd':{'level':1,'type':None,'reason':None,'vxid_parent':pvxid,'length':len(data),'tag':None,'vxid':vxid,'data':data,'isbin':0}})
            
    def parseRaw(self):
        #    100073 Timestamp      c Process: 1435425931.782784 1.000796 0.000036
        r = re.compile(r"^ *(\d+) ([^ ]+) +([^ ]) (.*)$")
        r2 = re.compile(r"^ *(\d+) ([^ ]+) +([^ ])$")
        pvxid=0
        for line in self.__raw:
            m = r.match(line)
            data = ''
            if not m:
                m = r2.match(line)
            else:
                data = m.group(4)
            if not m:
                continue
            vxid = int(m.group(1))
            if vxid==0:
                #CLI
                continue
            ttag = m.group(2)
            type = m.group(3)
            if ttag == 'Begin':
                pvxid = int(data.split(' ',3)[1])
            
            if vxid not in self.data:
                self.data[vxid] = []
            self.data[vxid].append({'ttag':ttag,'pvxid':pvxid,'cbd':{'level':1,'type':type,'reason':None,'vxid_parent':pvxid,'length':len(data),'tag':None,'vxid':vxid,'data':data,'isbin':0}})
            
    def execute(self):
        self.__raw   = []
        self.parse = None
        self.data  = {}
        if not os.path.exists(self.fname):
            return 0
        f = open(self.fname)
        for line in f.readlines():
            self.__raw.append(line.rstrip("\r\n"))
        f.close()
        self.chkFmt()
        self.parse()
        del self.__raw
        
        for v in self.data.values():
            for data in v:
                self.filter(data['ttag'],data['cbd'])
        
class vsl2chunk(v4filter):
    def __init__(self, opts, outcb):
        self.mode = 'request'
        #self.mode = 'session'
        
        self.source = 'vsl'

        #一旦requestで、sessionも対応する
        arg = {}
        vops = ['-g',self.mode]
        if isinstance(opts, list):
            for o,a in opts:
                if   o == '-q':
                    vops += ['-q', a]
                elif o == '--sopath':
                    arg["sopath"] = a
                elif o == '-n':
                    vops += ['-n', a]
        arg["opt"]   = vops
        self.vap     = varnishapi.VarnishLog(**arg)
        if self.vap.error:
            print(self.vap.error)
            exit(1)
        v4filter.__init__(self,opts,self.vap.vut,outcb)
    
    def execute(self):
        while 1:
            #dispatch
            ret = self.vap.Dispatch(self.vapCallBack)
            if 0 == ret:
                time.sleep(0.1)
            if ret < -3:
                print(self.vap.error)
                exit(1)

    def vapCallBack(self, vap, cbd, priv):
        ttag = vap.VSL_tags[cbd['tag']]
        self.filter(ttag,cbd)
    


class vslTrans4:
    def __init__(self, opts):
        self.source = 'vsl'
        self.odrv   = None
        f_dot       = 0
        if isinstance(opts, list):
            for o,a in opts:
                if o == '-f':
                    self.source = 'file'
                elif o == '-j':
                    self.odrv = im2JSON()
                elif o == '-d':
                    f_dot = 1
        if self.odrv is None:
            if f_dot:
                self.odrv = im2DOT()
            else:
                self.odrv = im2CLI()
        elif f_dot:
            self.odrv.setDOT()
        if self.source == 'vsl':
            self.idrv = vsl2chunk(opts,self.odrv.getData)
        else:
            self.idrv = log2chunk(opts,self.odrv.getData)
            
    def execute(self):
        self.idrv.execute()

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


