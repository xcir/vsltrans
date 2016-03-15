#!/usr/bin/python

import vsltranscore,getopt,os,sys,syslog,traceback
#based on Jurgen Hermanns http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66012

def main(opts):
	try:
		vhs = vsltranscore.vslTrans4(opts)
		vhs.execute()
	except KeyboardInterrupt:
		pass
	except Exception as e:
		syslog.openlog(sys.argv[0], syslog.LOG_PID|syslog.LOG_PERROR, syslog.LOG_LOCAL0)
		syslog.syslog(syslog.LOG_ERR, traceback.format_exc())

if __name__ == '__main__':
	try:
		opts,args = getopt.getopt(sys.argv[1:],"VP:q:f:n:", ["sopath=","debug"])
	except getopt.GetoptError:
		print 'invalid option'
		print 'usage: vsltrans -f [logfile] -q [query] --sopath [libvarnishapi.so] -n [instance-name] -V'
		sys.exit(2)
	
	d_flag = False
	p_file = False
	for o,a in opts:
		if   o == '-D':
			d_flag = True
		elif o == '-P':
			p_file = a
		elif o == '-V':
			print 'vsltrans (v0.x)'
			sys.exit(0)
		elif o == '-n':
			print 'using instance %s' % a
	if d_flag:
		try:
			pid = os.fork()
			if pid > 0:
				sys.exit(0)
		except OSError, e:
			print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
			sys.exit(1)
		os.chdir("/")
		os.setsid()
		os.umask(0)
		try:
			pid = os.fork()
			if pid > 0:
				if p_file:
					open(p_file,'w').write("%d"%pid)
				sys.exit(0)
		except OSError, e:
			print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror)
			sys.exit(1)
	main(opts)


