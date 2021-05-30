from cassandra.cluster import Cluster
from flask import *
import requests, csv, sys, os
from database import inicio, registroC, registroP, getNd, getTd, getTipo, editC, regVisita, hVisitas, hVisitasP, getNitP, getCatRsol
from database import editP, getCorC, getCorP, getPass, fVisitasC, regVDestiempo, fVisitasP, getEdad, getEstrato, salidas_recientes
from download_files import download_csv, download_pdf
from QR import makeQR, readQR
from cryption import encriptar, decriptar
from correo import enviar_correo
from extra_functions import calcular_riesgo

#Configuramos la app de flask
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/set/')
def set():
    session['key'] = 'value'
    return 'ok'

#VISTA DE LOGIN
@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form["b1"]=="Iniciar sesion":
            u = request.form['user']
            p = encriptar(request.form['pass'])
            ans, tp = inicio(u, p)
            if ans:
                session['user'] = request.form['user']
                if tp == 1:
                    return redirect(url_for('main_civil'))
                if tp == 3:
                    return redirect(url_for('main_publico'))
            else:
                flash("Usuario o contraseña incorrecta")
        elif request.form["b1"]=="Registrarse":
            return redirect(url_for('register_select'))
        elif request.form["b1"]=="Recordar Contraseña":
            return redirect(url_for('recuperar_contra'))
    return render_template('login.html')

#VISTA SELECCIONAR TIPO DE REGISTRO
@app.route('/register_select', methods=['GET','POST'])
def register_select():
    if request.method == 'POST':
        select_tipo = str(request.form.get('tipoR'))
        if select_tipo == "C":
            return redirect(url_for('register_civil'))
        elif select_tipo == "EP":
            return redirect(url_for('register_publico'))
    return render_template('register_select.html')

#VISTA REGISTRO DEL CIVIL
@app.route('/register_civil', methods=['GET','POST'])
def register_civil():
    if request.method == 'POST':
        nombres_ = request.form['nombres']
        apellidos_ = request.form['apellidos']
        fecha_ = request.form['fecha']
        tipoDoc = request.form['tipoDocumento']
        numDoc = request.form['numeroDocumento']
        dept = request.form['departamento']
        mun = request.form['municipio']
        barrio_ = request.form['barrio']
        dire = request.form['direccion']
        genero_ = request.form['genero']
        tel = request.form['telefono']
        email = request.form['correo']
        u = request.form['username']
        p = encriptar(request.form['password'])
        #Registro del civil en la base de datos
        ans = registroC(u, p, int(numDoc), apellidos_, barrio_, email, dept, dire, mun, fecha_, nombres_, genero_, tipoDoc, int(tel))
        if ans == True:
            data = {}
            data["Nombre"] = nombres_
            data["Apellido"] = apellidos_
            data["Tipo Documento"] = tipoDoc
            data["Numero Documento"] = numDoc
            #Se crea el codigo qr del civil
            makeQR(data)
        return redirect(url_for('login'))
    return render_template('register_civil.html')

#VISTA REGISTRO DE ENTIDAD PUBLICA
@app.route('/register_publico', methods=['GET','POST'])
def register_publico():
    if request.method == 'POST':
        nit_ = request.form['NIT']
        cat = str(request.form.get('categoria'))
        razon_ = request.form['razon']
        dept_ = str(request.form.get('departamento'))
        mun_ = str(request.form.get('municipio'))
        barrio_ = str(request.form.get('barrio'))
        dir_ = request.form['direccion']
        tels = []
        t1 = request.form['T1']
        tels.append(int(t1))
        t2 = request.form['T2']
        if len(t2) != 0: tels.append(int(t2))
        t3 = request.form['T3']
        if len(t3) != 0: tels.append(int(t3))
        email = request.form['correo']
        u = request.form['username']
        p = encriptar(request.form['password'])
        #Registro de la entidad publica en la base de datos
        registroP(u, int(nit_), barrio_, cat, email, dept_, dir_, mun_, p, razon_, tels)
        m = ""
        m += "La entidad publica identificada con el NIT " + nit_ + " se acaba de registrar en el sistema"
        enviar_correo("gerentebbgm@gmail.com", "Registro entidad publica", m)
        return redirect(url_for('login'))
    return render_template('register_publico.html')

#VISTA MAIN CIVIL
@app.route('/main_civil', methods=['GET','POST'])
def main_civil():
    usuario = None
    if 'user' in session:
        usuario = session['user']
        if request.method == 'POST':
            if request.form["btn"] == "Cerrar Sesión":
                session.pop('user', None)
                return redirect(url_for('login'))
            elif request.form["btn"] == "Código QR":
                return redirect(url_for('vista_qr'))
            elif request.form["btn"] == "Historial de visitas":
                return redirect(url_for('vista_historiales'))
            elif request.form["btn"] == "Contáctanos":
                return redirect(url_for('contacto'))
            elif request.form["btn"] == "Editar Perfil":
                return redirect(url_for('editar_perfil_civil'))
            elif request.form["btn"] == "Calcular Riesgo":
                return redirect(url_for('vista_riesgo'))
    return render_template('main_civil2.html', usuario=usuario)

#VISTA MAIN ENTIDAD PUBLICA
@app.route('/main_publico', methods=['GET','POST'])
def main_publico():
    usuario = None
    if 'user' in session:
        usuario = session['user']
        if request.method == 'POST':
            if request.form["btn"] == "Cerrar Sesión":
                session.pop('user', None)
                return redirect(url_for('login'))
            elif request.form["btn"] == "Registro Asíncrono":
                return redirect(url_for('registro_falla'))
            elif request.form["btn"] == "Registro Visita":
                return redirect(url_for('registro_visita'))
            elif request.form["btn"] == "Historial de visitas":
                return redirect(url_for('vista_historiales_visitas'))
            elif request.form["btn"] == "Contáctanos":
                return redirect(url_for('contacto_publico'))
            elif request.form["btn"] == "Editar Perfil":
                return redirect(url_for('editar_perfil_publico'))
    return render_template('main_publico.html', usuario=usuario)

#VISTA PARA CALCULAR RIESGO PARA CIVIL
@app.route('/riesgo', methods=['GET','POST'])
def vista_riesgo():
    usuario = session['user']
    mensaje_riesgo = ''
    if request.method == 'POST':
        if request.form["btn"] == "Calcular Riesgo":
            estrato = 6 #getEstrato(usuario)
            ndu = getNd(usuario)
            tdu = getTd(usuario)
            num_salidas_recientes = salidas_recientes(ndu, tdu)
            edad = getEdad(usuario)
            riesgo = calcular_riesgo(edad, estrato, num_salidas_recientes)
            mensaje_riesgo = "{0}, tu factor de riesgo de infección es: {1}".format(usuario, riesgo)
        elif request.form["btn"] == "Volver":
            return redirect(url_for('main_civil'))

    return render_template('vista_riesgo.html', usuario=usuario, mensaje_riesgo=mensaje_riesgo)

#VISTA DEL CODIGO QR PARA EL CIVIL
@app.route('/qr', methods=['GET','POST'])
def vista_qr():
    usuario = session['user']
    ndu = getNd(usuario)
    qr = "QR_{0}.png".format(str(ndu))
    return render_template('vista_qr.html', usuario=usuario, qr=qr)

#VISTA HISTORIALES DE VISITAS PARA EL CIVIL
@app.route('/historiales', methods=['GET','POST'])
def vista_historiales():
    fields = ['Establecimiento Publico', 'Categoria', 'Fecha Entrada', 'Hora Entrada', 'Veredicto', 'Razón']
    usuario = session['user']
    ndu = getNd(usuario)
    tdu = getTd(usuario)
    hist_completo = hVisitas(ndu, tdu)
    if request.method == 'POST':
        if request.form["btn"] == "Filtrar":
            if len(request.form['fi']) != 0: fi_ = request.form['fi']
            else: fi_ = None
            if len(request.form['ff']) != 0: ff_ = request.form['ff']
            else: ff_ = None
            if request.form.get('categoria') != None: cat_ = str(request.form.get('categoria'))
            else: cat_ = None
            nd_ = getNd(usuario)
            td_ = getTd(usuario)
            hist_completo = fVisitasC(nd_,td_,cat_,fi_,ff_)
        elif request.form["btn"] == "Descargar":
            if str(request.form.get('formato')) == "CSV":
                download_csv(fields, hist_completo, 1)
            elif str(request.form.get('formato')) == "PDF":
                download_pdf(fields, hist_completo, 1)
    return render_template('vista_historiales.html', usuario=usuario, hist_completo=hist_completo)

#VISTA CONTACTO PARA EL CIVIL
@app.route('/contacto_civil', methods=['GET','POST'])
def contacto():
    usuario = session['user']
    if 'user' in session:
        if request.method == 'POST':
            if request.form["btn"] == "Enviar":
                td_ = str(request.form.get('TD'))
                nd_ = request.form['ND']
                nombres_ = request.form['nombres']
                apellidos_ = request.form['apellidos']
                email = request.form['correo']
                comentarios_ = request.form['comentarios']
                m1 = ""
                m1 += nombres_ + " " + apellidos_ + " identificado con " + td_ + " " + nd_ + " te envio los siguientes comentarios " + comentarios_ + ". Responder al correo " + email
                enviar_correo("gerentebbgm@gmail.com", "Solicitud de contacto", m1)
                m2 = "Tus comentarios fueron enviados con exito. Pronto te responderemos."
                enviar_correo(email, "Envio Solicitud de Contacto", m2)
            elif request.form["btn"] == "Volver":
                return redirect(url_for('main_civil'))
    return render_template('contacto_civil.html', usuario=usuario)

#VISTA CONTACTO PARA ENTIDAD PUBLICA
@app.route('/contacto_publico', methods=['GET','POST'])
def contacto_publico():
    usuario = session['user']
    if 'user' in session:
        if request.method == 'POST':
            if request.form["btn"] == "Enviar":
                nit_ = request.form['NIT']
                email = request.form['correo']
                comentarios_ = request.form['comentarios']
                m1 = ""
                m1 += "La entidad publica identificada con el NIT " + nit_ + " te envio los siguientes comentarios " + comentarios_ + ". Responder al correo " + email
                enviar_correo("gerentebbgm@gmail.com", "Solicitud de contacto", m1)
                m2 = "Tus comentarios fueron enviados con exito. Pronto te responderemos."
                enviar_correo(email, "Envio Solicitud de Contacto", m2)
            elif request.form["btn"] == "Volver":
                return redirect(url_for('main_publico'))
    return render_template('contacto_publica.html', usuario=usuario)

#VISTA EDITAR PERFIL PARA EL CIVIL
@app.route('/edit_perfil', methods=['GET','POST'])
def editar_perfil_civil():
    usuario = session['user']
    td = getTd(usuario)
    nd = getNd(usuario)
    if 'user' in session:
        if request.method == 'POST':
            if request.form["btn"] == "Guardar":
                if len(request.form['nombres']) != 0: nombres_ = request.form['nombres']
                else: nombres_ = None
                if len(request.form['apellidos']) != 0: apellidos_ = request.form['apellidos']
                else: apellidos_ = None
                if request.form.get('genero') != None: genero_ = str(request.form.get('genero'))
                else: genero_ = None
                if len(request.form['T']) != 0: tel_ = int(request.form['T'])
                else: tel_ = None
                if len(request.form['fecha']) != 0: fecha_ = request.form['fecha']
                else: fecha_ = None
                if len(request.form['correo']) != 0: email = request.form['correo']
                else: email = None
                if request.form.get('departamento') != None: dept_ = str(request.form.get('departamento'))
                else: dept_ = None
                if request.form.get('municipio') != None: mun_ = str(request.form.get('municipio'))
                else: mun_ = None
                if request.form.get('barrio') != None: barrio_ = str(request.form.get('barrio'))
                else: barrio_ = None
                if len(request.form['direccion']) != 0: dir_ = request.form['direccion']
                else: dir_ = None
                if len(request.form['contraseña']) != 0: p = encriptar(request.form['contraseña'])
                else: p = None
                editC(usuario, p, int(nd), apellidos_, barrio_, email, dept_, dir_, mun_, fecha_, nombres_, genero_, td, tel_)
            elif request.form["btn"] == "Volver":
                return redirect(url_for('main_civil'))
    return render_template('editar_perfil_civil.html', usuario=usuario)

#VISTA EDITAR PERFIL PARA ENTIDAD PUBLICA
@app.route('/edit_perfil_publico', methods=['GET','POST'])
def editar_perfil_publico():
    usuario = session['user']
    if 'user' in session:
        if request.method == 'POST':
            if request.form["btn"] == "Guardar":
                if len(request.form['razon']) != 0: razon_ = request.form['razon']
                else: razon_ = None
                if len(request.form['T1']) != 0: tel1_ = int(request.form['T1'])
                else: tel1_ = None
                if len(request.form['T2']) != 0: tel2_ = int(request.form['T2'])
                else: tel2_ = None
                if len(request.form['T3']) != 0: tel3_ = int(request.form['T3'])
                else: tel3_ = None
                if request.form.get('departamento') != None: dept_ = str(request.form.get('departamento'))
                else: dept_ = None
                if request.form.get('municipio') != None: mun_ = str(request.form.get('municipio'))
                else: mun_ = None
                if request.form.get('barrio') != None: barrio_ = str(request.form.get('barrio'))
                else: barrio_ = None
                nit_ = getNitP(usuario)
                editP(usuario, nit_, barrio_, None, dept_, None, mun_, None, razon_, tel1_, tel2_, tel3_)
            elif request.form["btn"] == "Volver":
                return redirect(url_for('main_publico'))
    return render_template('editar_perfil_publico.html', usuario=usuario)

#VISTA REGISTRO VISITA CON QR PARA ENTIDAD PUBLICA
@app.route('/registro_visita', methods=['GET','POST'])
def registro_visita():
    scriptPath = sys.path[0]
    UPLOAD_PATH = os.path.join(scriptPath, 'static/images/uploads/')
    usuario = session['user']
    data =  None
    if 'user' in session:
        if request.method == 'POST':
            if request.form["btn"] == "Registrar":
                tapabocas_ = str(request.form.get('tapabocas'))
                temperatura = request.form['temp']
                filename = None
                if 'file' not in request.files:
                    flash('No file part')
                    return redirect(request.url)
                file = request.files['file']
                if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)
                if file and allowed_file(file.filename):
                    filename = file.filename
                    file.save('{0}{1}'.format(UPLOAD_PATH, filename))
                    data = readQR(filename)
                nitus = getNitP(usuario)
                rsol, cat = getCatRsol(usuario)
                tap = None
                if tapabocas_ == "Si": tap = True
                else: tap = False
                regVisita(nitus, int(data[3]), data[2], data[0], data[1], int(temperatura), tap, rsol, cat)
                os.remove('{0}{1}'.format(UPLOAD_PATH, filename))
                return redirect(url_for('registro_visita'))
    return render_template('vista_registro_visita.html', usuario=usuario)

#VISTA REGISTRO VISITA POST FALLA ENTIDAD PUBLICA
@app.route('/registro_falla', methods=['GET','POST'])
def registro_falla():
    usuario = session['user']
    if request.method == 'POST':
        if request.form["btn"] == "Registrar":
            nombres_ = request.form['nombres']
            apellidos_ = request.form['apellidos']
            td_ = str(request.form.get('TD'))
            nd_ = request.form['ND']
            temp_ = request.form['temp']
            if str(request.form.get('tapabocas')) == "Si": tap_= True
            else: tap_ = False
            fecha_ = request.form['fecha']
            hora_ = request.form['hora']
            nit_ = getNitP(usuario)
            rsol, cat = getCatRsol(usuario)
            regVDestiempo(nit_,int(nd_),td_,nombres_,apellidos_,int(temp_),tap_,rsol,cat,fecha_,hora_)
    return render_template('vista_registro_visita_NE.html', usuario=usuario)

#VISTA HISTORIALES DE VISITA ENTIDAD PUBLICA
@app.route('/historiales_visitas', methods=['GET','POST'])
def vista_historiales_visitas():
    fields = ["Tipo Documento", "Numero Documento", "Fecha Entrada", "Hora Entrada", "Veredicto", "Razón"]
    usuario = session['user']
    nitus = getNitP(usuario)
    hist_completo = hVisitasP(nitus)
    if request.method == 'POST':
        if request.form["btn"] == "Descargar":
            if str(request.form.get('formato')) == "CSV":
                download_csv(fields, hist_completo, 1)
            elif str(request.form.get('formato')) == "PDF":
                download_pdf(fields, hist_completo, 1)
        elif request.form["btn"] == "Filtrar":
            if len(request.form['fi']) != 0: fi_ = request.form['fi']
            else: fi_ = None
            if len(request.form['ff']) != 0: ff_ = request.form['ff']
            else: ff_ = None
            if request.form.get('categoria') != None: cat_ = str(request.form.get('categoria'))
            else: cat_ = None
            if cat_ == "Denegado": c = False
            else: c = True
            nit_ = getNitP(usuario)
            hist_completo = fVisitasP(nit_, c, fi_, ff_)
    return render_template('vista_historial_visitas.html', usuario=usuario, hist_completo=hist_completo)

#VISTA RECUPERAR CONTRASEÑA
@app.route('/recuperar', methods=['GET','POST'])
def recuperar_contra():
    mensaje = ""
    if request.method == 'POST':
        if request.form["btn"] == "Recuperar":
            usr = request.form['usuario']
            email = request.form['correo']
            usr_email = None
            t = getTipo(usr)
            if t == 1: usr_email = getCorC(usr)
            elif t == 3: usr_email = getCorP(usr)
            if usr_email == email:
                p = getPass(usr)
                m = "Tu contrasena es {0}".format(decriptar(p))
                enviar_correo(usr_email, "Recuperacion contrasena", m)
                mensaje = "Tu contrasena ha sido enviada a tu correo"
            else:
                mensaje = "El correo que ingresaste no esta asociado al usuario ingresado"
    return render_template('recuperar_contrasena.html', mensaje=mensaje)

if __name__ == "__main__":
    app.debug = True
    app.run()
