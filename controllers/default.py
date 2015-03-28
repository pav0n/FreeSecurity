def index():
    imagenes = db().select(db.imagen.ALL, orderby=db.imagen.titulo)
    return dict(imagenes=imagenes)

@auth.requires_login()
def mostrar():
    imagen = db.imagen(request.args(0, cast=int)) or redirect(URL('index'))
    db.publicacion.imagen_id.default = imagen.id
    formulario = SQLFORM(db.publicacion)
    if formulario.process().accepted:
        response.flash = 'tu comentario se ha publicado'
    comentarios = db(db.publicacion.imagen_id==imagen.id).select()
    return dict(imagen=imagen, comentarios=comentarios, formulario=formulario)

def download():
    return response.download(request, db)

def user():
    return dict(form=auth())

@auth.requires_membership('administrador')
def administrar():
    grid = SQLFORM.smartgrid(db.imagen, linked_tables=['comentario'])
    return dict(grid=grid)
