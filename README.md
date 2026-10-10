# Gestor de Cursos actualizado

Proyecto actualizado tomando como referencia el contenido de `django-gestion-proyectos.zip` entregado por el profesor. Se conserva la temática de cursos y lecciones, los formularios ModelForm, las rutas existentes y el CSS local.

## Qué se incorporó

| Avance del proyecto de clase | Adaptación al gestor de cursos |
| --- | --- |
| Aplicación accounts y LoginView/LogoutView | Inicio de sesión en `/login/` y cierre de sesión mediante POST |
| login_required | Todas las vistas de cursos y lecciones requieren sesión |
| Página de inicio y acerca de | `/inicio/` y `/acerca-de/` |
| Plantilla base compartida | `templates/layouts/base.html`, navegación y botón de cerrar sesión |
| Edición de proyectos | Edición de título, descripción, nivel e imagen del curso |
| ImageField y archivos multimedia | Portada opcional de los cursos, visible en el listado y detalle |
| Prioridad de tareas | Prioridad Baja, Media o Alta de las lecciones |
| Avance del estado por POST | Borrador → En revisión → Publicado |
| Configuración regional | Español y zona horaria America/Bogota |
| requirements.txt | Dependencias de la versión de clase: Django 5.2.17 |

El estado “En revisión” representa la preparación editorial de una lección. Los estados existentes Borrador y Publicado mantienen sus valores originales. Las lecciones anteriores reciben prioridad Media; los cursos anteriores quedan sin portada hasta que se agregue una.

La portada es opcional y no requiere conexión a un CDN. Al editar un curso sin subir otra imagen, se conserva la portada actual. El formulario permite quitarla.

Se mantienen la creación, edición y eliminación de lecciones. La eliminación de cursos y lecciones sigue mostrando una confirmación y solo se ejecuta al enviar POST. Los identificadores inexistentes devuelven 404.

## Ejecutar en Windows con Visual Studio Code

1. Extrae `gestor_cursos_actualizado.zip` en una carpeta nueva. Abre la carpeta `gestor_cursos_final` en VS Code: es la que contiene `manage.py`.
2. Abre **Terminal > Nueva terminal**. Los comandos siguientes se ejecutan dentro de esa carpeta.
3. Crea el entorno virtual con tu instalación de Python (Python 3.10 o superior):

   ```powershell
   python -m venv entorno
   ```

4. Activa el entorno en PowerShell:

   ```powershell
   .\entorno\Scripts\Activate.ps1
   ```

   Si usas CMD, ejecuta:

   ```cmd
   entorno\Scripts\activate.bat
   ```

   Si PowerShell bloquea la activación, puedes usar el intérprete del entorno directamente, sin cambiar ninguna política del equipo:

   ```powershell
   .\entorno\Scripts\python.exe -m pip install -r requirements.txt
   .\entorno\Scripts\python.exe manage.py migrate
   .\entorno\Scripts\python.exe manage.py createsuperuser
   .\entorno\Scripts\python.exe manage.py runserver
   ```

5. Con el entorno activado, instala las dependencias:

   ```powershell
   python -m pip install -r requirements.txt
   ```

6. Aplica las migraciones:

   ```powershell
   python manage.py migrate
   ```

7. Crea tu usuario para iniciar sesión:

   ```powershell
   python manage.py createsuperuser
   ```

   Ingresa el nombre de usuario y la contraseña que quieras usar. La contraseña no se muestra mientras la escribes. La base de datos recibida no contenía usuarios, cursos ni lecciones; no se agregó una cuenta ni contraseña predeterminada.

8. Ejecuta el servidor:

   ```powershell
   python manage.py runserver
   ```

9. Abre http://127.0.0.1:8000/ e inicia sesión con el usuario creado. En VS Code, usa **Ctrl + Shift + P > Python: Select Interpreter** y selecciona `entorno\Scripts\python.exe`.

El ZIP incluye la base de datos original con la nueva migración aplicada. El comando `migrate` también permite preparar una base de datos nueva o actualizar una copia anterior. No necesitas ejecutar `makemigrations` para usar esta actualización.

## Si tienes datos más recientes en tu computadora

Antes de reemplazar tu proyecto, conserva una copia completa de su carpeta. Puedes usar tu `db.sqlite3` más reciente dentro de la carpeta actualizada y ejecutar `python manage.py migrate`: la migración `0002` agrega los campos sin eliminar los registros existentes. Si ya tenías imágenes, conserva también la carpeta `media`.

El entorno virtual del ZIP original era de Windows y no se incluye en este ZIP: crea uno nuevo para esta carpeta e instala sus dependencias. No reutilices el entorno anterior con otra versión de Django.

## Rutas

| Ruta | Función |
| --- | --- |
| `/login/` | Iniciar sesión |
| `/logout/` | Cerrar sesión mediante el botón, con POST |
| `/inicio/` | Bienvenida |
| `/acerca-de/` | Información del gestor |
| `/` o `/cursos/` | Listado de cursos |
| `/curso/nuevo/` | Crear curso |
| `/curso/<pk>/` | Detalle y lecciones |
| `/curso/<pk>/editar/` | Editar curso y portada |
| `/curso/<pk>/eliminar/` | Confirmar eliminación |
| `/curso/<pk>/leccion/nueva/` | Crear lección |
| `/leccion/<pk>/editar/` | Editar lección |
| `/leccion/<pk>/eliminar/` | Confirmar eliminación |
| `/leccion/<pk>/avanzar/` | Avanzar estado, solo POST |
| `/admin/` | Panel de administración |

Como en el ejercicio de clase, los usuarios autenticados administran el mismo catálogo. No se agregó registro público ni separación de cursos por propietario.

## Archivos principales modificados

- `cursos/models.py`: imagen del curso, prioridad de la lección y estado de revisión.
- `cursos/forms.py`: campos nuevos en los formularios.
- `cursos/views.py`: protección de acceso, edición del curso, archivos subidos y avance de estado.
- `cursos/urls.py`: rutas nuevas, manteniendo las anteriores.
- `cursos/migrations/0002_curso_imagen_leccion_prioridad_alter_leccion_estado.py`: actualización de la base de datos.
- `accounts/`: aplicación de autenticación.
- `config/settings.py` y `config/urls.py`: autenticación, idioma y multimedia.
- `templates/`: plantilla base, login, inicio, acerca de y formularios actualizados.
- `static/css/styles.css`: estilos compartidos complementarios.
- `requirements.txt`, `.gitignore` y `cursos/tests.py`.

## Comprobación

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test cursos
```

La actualización pasó seis pruebas automatizadas con Django 5.2.17: protección de todas las vistas; login, destino de regreso y logout; renderizado de páginas y errores 404; creación/edición con validación de imágenes; prioridad, avance de estado, restricción POST y CSRF; confirmación de eliminación y borrado de lecciones en cascada.

Esta configuración está preparada para ejecución local durante las clases.
