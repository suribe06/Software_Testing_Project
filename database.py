from cassandra.cluster import Cluster
import datetime as dt

cluster = Cluster(contact_points=['127.0.0.1'], port=9042)
sessionDB = cluster.connect("bdis")

def inicio(usr,pasw):
	"""
	Esta funcion verifica los datos para permitir iniciar sesion a los usuarios
	"""
	tp = -1
	person = sessionDB.execute("SELECT password,tipo from usuarios WHERE username = '{0}'".format(usr))
	if person.one() == None or person.one().password != pasw: ans = False
	else:ans,tp = True, person.one().tipo
	return ans,tp

def registroC(usr,pasw,ndoc,ape,bar,cor,dep,dire,mun,nac,nom,sex,tdoc,tel):
	"""
	Esta funcion registra un civil en la base de datos
	"""
	person1 = sessionDB.execute("SELECT password,tipo from usuarios WHERE username = '{0}'".format(usr))
	person2 = sessionDB.execute("SELECT password from civil WHERE ndocumento = {0} and tdocumento = '{1}' allow filtering".format(ndoc,tdoc))
	ans = False
	if person1.one() == None and person2.one() == None:
		ans = True
		sessionDB.execute("INSERT INTO civil (username,ndocumento,apellidos,barrio,correo,departamento,direccion,municipio,nacimiento,nombres,password,sexo,tdocumento,telefono) VALUES('{0}',{1},'{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}',{13})".format(usr,ndoc,ape,bar,cor,dep,dire,mun,nac,nom,pasw,sex,tdoc,tel))
		sessionDB.execute("INSERT INTO usuarios (username,password,tipo) VALUES ('{0}','{1}',{2})".format(usr,pasw,1))
	return ans

def registroP(usr,n,bar,cat,cor,dep,dir,mun,pasw,rsol,tel):
	"""
	Esta funcion registra una entidad publica en la base de datos
	"""
	ent1 = sessionDB.execute("SELECT password,tipo from usuarios WHERE username = '{0}'".format(usr))
	ent2 = sessionDB.execute("SELECT username, Nit from publica WHERE Nit = {0} allow filtering".format(n))
	if ent1.one() == None and ent2.one() == None:
		sessionDB.execute("INSERT INTO usuarios (username,password,tipo) VALUES ('{0}','{1}',{2})".format(usr,pasw,3))
		if len(tel) == 3:
			sessionDB.execute("INSERT INTO publica (username,Nit,barrio,categoria,correo,departamento,direccion,municipio,password,rsocial,telefono1,telefono2,telefono3) VALUES ('{0}',{1},'{2}','{12}','{3}','{4}','{5}','{6}','{7}','{8}',{9},{10},{11})".format(usr,n,bar,cor,dep,dir,mun,pasw,rsol,tel[0],tel[1],tel[2],cat))
		elif len(tel) == 2:
			sessionDB.execute("INSERT INTO publica (username,Nit,barrio,categoria,correo,departamento,direccion,municipio,password,rsocial,telefono1,telefono2,telefono3) VALUES ('{0}',{1},'{2}','{11}','{3}','{4}','{5}','{6}','{7}','{8}',{9},{10},NULL)".format(usr,n,bar,cor,dep,dir,mun,pasw,rsol,tel[0],tel[1],cat))
		else:
			sessionDB.execute("INSERT INTO publica (username,Nit,barrio,categoria,correo,departamento,direccion,municipio,password,rsocial,telefono1,telefono2,telefono3) VALUES ('{0}',{1},'{2}','{10}','{3}','{4}','{5}','{6}','{7}','{8}',{9},NULL,NULL)".format(usr,n,bar,cor,dep,dir,mun,pasw,rsol,tel[0],cat))
	return

def getNd(usr):
	"""
	Esta funcion obtiene el numero de documento de un civil
	"""
	person = sessionDB.execute("SELECT ndocumento from civil where username = '{0}'".format(usr))
	return person.one().ndocumento

def getTd(usr):
	"""
	Esta funcion obtiene el tipo de documento de un civil
	"""
	person = sessionDB.execute("SELECT tdocumento from civil where username = '{0}'".format(usr))
	return person.one().tdocumento

def getTipo(usr):
	"""
	Esta funcion obtiene el tipo del usuario (civil o publica)
	"""
	person = sessionDB.execute("SELECT tipo from usuarios where username = '{0}'".format(usr))
	return person.one().tipo

def editC(usr,pasw,ndoc,ape,bar,cor,dep,dire,mun,nac,nom,sex,tdoc,tel):
	"""
	Esta funcion edita el perfil de un civil
	"""
	exe = "UPDATE civil SET "
	exe1 = " WHERE username = '{0}' and ndocumento = {1} and tdocumento = '{2}'".format(usr,ndoc,tdoc)
	if pasw != None:
		exe+= "password = '{0}',".format(pasw)
		sessionDB.execute("UPDATE usuarios SET password = '{1}' WHERE username = '{0}'".format(usr,pasw))
	if ape != None: exe+="apellidos = '{0}',".format(ape)
	if bar != None: exe+="barrio = '{0}',".format(bar)
	if cor != None: exe+= "correo = '{0}',".format(cor)
	if dep != None: exe+="departamento = '{0}',".format(dep)
	if dire != None: exe+="direccion = '{0}',".format(dire)
	if mun != None: exe+="municipio = '{0}',".format(mun)
	if nac != None: exe+="nacimiento = '{0}',".format(nac)
	if nom != None: exe+="nombres = '{0}',".format(nom)
	if sex != None: exe+="sexo = '{0}',".format(sex)
	if tel != None: exe+="telefono = {0},".format(tel)
	if len(exe) > 17:
		exe = exe[:len(exe)-1]
		exe+= exe1
		print(exe)
		sessionDB.execute(exe)
	return

def regVisita(ni,nd,td,nom,ape,tem,tap,rsol,cat):
	"""
	Esta funcion registra una visita (con qr) de un civil a un establecimienti publico
	"""
	person = sessionDB.execute("SELECT nombres,apellidos from civil WHERE ndocumento = {0} and tdocumento = '{1}'allow filtering".format(nd,td))
	if person.one() != None:
	    visi = sessionDB.execute("SELECT COUNT(*) from visitas WHERE ndocumento = {0} and nit = {2} and tdocumento = '{1}'allow filtering".format(nd,td,ni))
	    i = int(visi.one().count) + 1
	    dia = dt.datetime.now()
	    temperatura = tem <= 37
	    ans = tap and temperatura
	    if ans == True:
	        sessionDB.execute("INSERT INTO visitas (id,nit,ndocumento,apellidos,categoria,fent,hent,nombres,reason,rsocial,tapa,tdocumento,temp,veredict) VALUES({0},{1},{2},'{3}','{15}','{4}-{5}-{6}','{12}:{13}:{14}','{7}','NA','{11}',{8},'{9}',{10},True)".format(i,ni,nd,ape,dia.year,dia.strftime("%m"),dia.strftime("%d"),nom,tap,td,tem,rsol,dia.hour,dia.minute,dia.second,cat))
	    else:
	        razon = ''
	        if not(tap):
	            razon = razon + '- No porta tapabocas '
	        if not(temperatura):
	            razon = razon + '- Temperatura elevada '
	        sessionDB.execute("INSERT INTO visitas (id,nit,ndocumento,apellidos,categoria,fent,hent,nombres,reason,rsocial,tapa,tdocumento,temp,veredict) VALUES({0},{1},{2},'{3}','{16}','{4}-{5}-{6}','{13}:{14}:{15}','{7}','{8}','{12}',{9},'{10}',{11},False)".format(i,ni,nd,ape,dia.year,dia.strftime("%m"),dia.strftime("%d"),nom,razon,tap,td,tem,rsol,dia.hour,dia.minute,dia.second,cat))
	return

def hVisitas(nd,td):
	"""
	Esta funcion obtiene las visitas a establecimientos publicos realizadas por un civil
	"""
	v = sessionDB.execute("SELECT * from visitas WHERE ndocumento = {0} and tdocumento = '{1}' allow filtering".format(nd,td))
	visi = []
	for obj in v:
	    if obj.veredict == True: b = "Aceptado"
	    else: b = "Denegado"
	    a = str(obj.fent.date().year)+"-"+str(obj.fent.date().month)+"-"+str(obj.fent.date().day)
	    c = str(obj.hent.time().hour)+":"+str(obj.hent.time().minute)
	    pub = sessionDB.execute("SELECT rsocial from publica WHERE nit = {0} allow filtering".format(obj.nit))
	    pers = [pub.one().rsocial,obj.categoria,a,c,b,obj.reason]
	    visi.append(pers)
	return visi

def hVisitasP(n):
	"""
	Esta funcion obtiene las visitas que ha recibido un establecimiento publico
	"""
	v = sessionDB.execute("SELECT * from visitas WHERE nit = {0} allow filtering".format(n))
	visi = []
	for obj in v:
	    if obj.veredict == True: b = "Aceptado"
	    else: b = "Denegado"
	    a = str(obj.fent.date().year)+"-"+str(obj.fent.date().month)+"-"+str(obj.fent.date().day)
	    c = str(obj.hent.time().hour)+":"+str(obj.hent.time().minute)
	    pers = [obj.tdocumento,obj.ndocumento,a,c,b,obj.reason]
	    visi.append(pers)
	return visi

def getNitP(usr):
	"""
	Esta funcion obtiene el NIT de la entidad publica
	"""
	person = sessionDB.execute("SELECT Nit from Publica where username = '{0}'".format(usr))
	return person.one().nit

def getCatRsol(usr):
	"""
	Esta funcion me da la categoria y la razon social de un establecimiento publico
	"""
	person = sessionDB.execute("SELECT rsocial, categoria from publica where username = '{0}'".format(usr))
	return person.one().rsocial,person.one().categoria

def editP(usr,n,bar,cor,dep,dire,mun,pasw,rsol,tel1,tel2,tel3):
	"""
	Esta funcion edita el perfil de un establecimiento publico
	"""
	exe = "UPDATE publica SET "
	exe1 = " WHERE username = '{0}' and nit = {1}".format(usr,n)
	if bar != None: exe+= "barrio = '{0}',".format(bar)
	if cor != None: exe+= "correo = '{0}',".format(cor)
	if dep != None: exe+="departamento = '{0}',".format(dep)
	if dire != None: exe+="direccion = '{0}',".format(dire)
	if mun != None: exe+="municipio = '{0}',".format(mun)
	if pasw != None:
		sessionDB.execute("UPDATE usuarios SET password = '{1}' WHERE username = '{0}'".format(usr,pasw))
		exe+="password = '{0}',".format(pasw)
	if rsol != None: exe+="rsocial = '{0}',".format(rsol)
	if tel1 != None: exe+="telefono1 = {0},".format(tel1)
	if tel2 != None: exe+="telefono2 = {0},".format(tel2)
	if tel3 != None: exe+="telefono3 = {0},".format(tel3)
	if len(exe) > 19:
		exe = exe[:len(exe)-1]
		exe+= exe1
		sessionDB.execute(exe)
	return

def getCorC(usr):
	"""
	Esta funcion me obtiene el correo de un civil
	"""
	person = sessionDB.execute("SELECT correo from civil where username = '{0}'".format(usr))
	return person.one().correo

def getCorP(usr):
	"""
	Esta funcion me obtiene el correo de un establecimiento publico
	"""
	person = sessionDB.execute("SELECT correo from publica where username = '{0}'".format(usr))
	return person.one().correo

def getPass(usr):
	"""
	Esta funcion obtiene la contrasena de un usuario
	"""
	person = sessionDB.execute("SELECT password from usuarios where username = '{0}'".format(usr))
	return person.one().password

def fVisitasC(nd,td,cat,fi,ff):
	"""
	Esta funcion filtra las visitas realizadas por un civil
	"""
	exe = "SELECT * from visitas where ndocumento = {0} and tdocumento = '{1}' ".format(nd,td)
	exe1 = "allow filtering"
	if fi != None: exe += "and fent >= '{0}' ".format(fi)
	if ff != None: exe += "and fent <= '{0}' ".format(ff)
	if cat != None: exe += "and categoria = '{0}' ".format(cat)
	exe += exe1
	v = sessionDB.execute(exe)
	visi = []
	for obj in v:
	    if obj.veredict == True: b = "Aceptado"
	    else: b = "Denegado"
	    a = str(obj.fent.date().year)+"-"+str(obj.fent.date().month)+"-"+str(obj.fent.date().day)
	    c = str(obj.hent.time().hour)+":"+str(obj.hent.time().minute)
	    pers = [obj.rsocial,obj.categoria,a,c,b,obj.reason]
	    visi.append(pers)
	return visi

def regVDestiempo(ni,nd,td,nom,ape,tem,tap,rsol,cat,fecha,hora):
	"""
	Esta funcion registra una visita asincrona por parte de un civil a un establecimiento publico
	"""
	person = sessionDB.execute("SELECT nombres,apellidos from civil WHERE ndocumento = {0} and tdocumento = '{1}' allow filtering".format(nd,td))
	if person.one() != None:
	    visi = sessionDB.execute("SELECT COUNT(*) from visitas WHERE ndocumento = {0} and tdocumento = '{1}' and nit = {2} allow filtering".format(nd,td,ni))
	    i = int(visi.one().count)+1
	    temperatura = tem <= 37
	    ans = temperatura and tap
	    if ans:
	        sessionDB.execute("INSERT INTO visitas (id,nit,ndocumento,apellidos,categoria,fent,hent,nombres,reason,rsocial,tapa,tdocumento,temp,veredict) VALUES({0},{1},{2},'{3}','{11}','{4}','{10}:00','{5}','NA','{9}',{6},'{7}',{8},True)".format(i,ni,nd,ape,fecha,nom,tap,td,tem,rsol,hora,cat))
	    else:
	        razon = ''
	        if not(tap):
	            razon = razon + '- No porta tapabocas '
	        if not(temperatura):
	            razon = razon + '- Temperatura elevada '
	        sessionDB.execute("INSERT INTO visitas (id,nit,ndocumento,apellidos,categoria,fent,hent,nombres,reason,rsocial,tapa,tdocumento,temp,veredict) VALUES({0},{1},{2},'{3}','{11}','{4}','{10}:00','{5}','{12}','{9}',{6},'{7}',{8},False)".format(i,ni,nd,ape,fecha,nom,tap,td,tem,rsol,hora,cat,razon))
	return

def fVisitasP(ni,ver,fi,ff):
	"""
	Esta funcion filtra las visitas que recibio un establecimiento publico
	"""
	exe = "SELECT * from visitas where nit = {0} ".format(ni)
	exe1 = "allow filtering"
	if fi != None: exe += "and fent >= '{0}' ".format(fi)
	if ff != None: exe += "and fent <= '{0}' ".format(ff)
	if ver != None: exe += "and veredict = {0} ".format(ver)
	exe += exe1
	v = sessionDB.execute(exe)
	visi = []
	for obj in v:
	    if obj.veredict == True: b = "Aceptado"
	    else: b = "Denegado"
	    a = str(obj.fent.date().year)+"-"+str(obj.fent.date().month)+"-"+str(obj.fent.date().day)
	    c = str(obj.hent.time().hour)+":"+str(obj.hent.time().minute)
	    pers = [obj.ndocumento,obj.tdocumento,a,c,b,obj.reason]
	    visi.append(pers)
	return visi

def getEdad(usr):
	"""
	Esta funcion retorna la edad de un civil
	"""
	today_date = dt.datetime.now().date()
	person = sessionDB.execute("SELECT nacimiento from civil where username = '{0}'".format(usr))
	birth_date = person.one().nacimiento.date()
	age = today_date - birth_date
	return int((age.days)/365)

def getEstrato(usr):
	"""
	Esta funcion retorna el estrato de un civil
	"""
	person = sessionDB.execute("SELECT estrato from civil where username = '{0}'".format(usr))
	return person.one().estrato

def salidas_recientes(nd, td):
	"""
	Esta funcion retorna el numero de visitas de un usuario en el rango de un mes
	"""
	dia = dt.datetime.now()
	dia -= dt.timedelta(days = 31)
	v = sessionDB.execute("SELECT * from visitas WHERE ndocumento = {0} and tdocumento = '{1}' and fent >= '{2}-{3}-{4}' allow filtering".format(nd,td,dia.year,dia.strftime("%m"),dia.strftime("%d")))
	ans = 0
	for obj in v:
		ans += 1
	return ans
