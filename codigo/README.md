# Curso Flask CodigoFacilito

EL siguiente proyecto fue hecho del tutorial de Codigo Facilito.  
Aunque el proyecto carece de la parte de los mails, aun asi se le han añadido  
las siguiente acciones: 

- Menu de navegacion
- <strong>helper/featurepagination:</strong> Solo obtiene el numero de paginas totales
- <strong>helper/extract_text:</strong> Para mostrar una determinada cantidad de palabras de una cadena.
- <strong>helper/delete_spacewith:</strong> lo utiliza para realizar eliminar los espacios en un estring por ejemplo en el titulo de un post, donde es necesario mandar el titulo por parametro
- <strong>models/Post:</strong> se añadio el modelo de post, y en la base de datos y se enlazo a user y un campo en comment
- <strong>forms/new_post:</strong> se creo un nuevo formulario
- <strong>main/index:</strong> se muestran los post publicados
- <strong>main/post:</strong> se muestra el post con los comentarios que se pueden hacer
- <strong>main/new_post:</strong> se puede postear 
- <strong>main/upload_file:</strong> para subir imagenes pero sin hacerlo en el post y sin guardarlo en la bd

## Dependencias
En lubuntu 16.04.03 al momento de instalar flask no se instalaron algunos paquetes

- pip install Flask-SQLAlchemy
- pip install wtForm
- pip install flask_wtf

## Estado:
En mi equipo windows 10, no se pudo instalar mysqldb, por lo que da error
