if not request.env.web2py_runtime_gae:
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    db = DAL('google:datastore+ndb')
    session.connect(request, response, db=db)

response.generic_patterns = ['*'] if request.is_local else []

from gluon.tools import Auth

auth = Auth(db)
auth.define_tables(username=False, signature=False)
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

db.define_table('imagen',
                Field('titulo', unique=True),
                Field('archivo', 'upload'),
                format = '%(titulo)s')

db.define_table('publicacion',
                Field('imagen_id', 'reference imagen'),
                Field('autor'),
                Field('email'),
                Field('cuerpo', 'text'))

db.imagen.titulo.requires = IS_NOT_IN_DB(db, db.imagen.titulo)
db.publicacion.imagen_id.requires = IS_IN_DB(db, db.imagen.id, '%(titulo)s')
db.publicacion.autor.requires = IS_NOT_EMPTY()
db.publicacion.email.requires = IS_EMAIL()
db.publicacion.cuerpo.requires = IS_NOT_EMPTY()
db.publicacion.imagen_id.writable = db.publicacion.imagen_id.readable = False
