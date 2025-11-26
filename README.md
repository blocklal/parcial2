Proyecto de parcial número 2.
Comandos para la instalación:

git close python https://github.com/blocklal/parcial2.git
cd parcial2
python -m venv venv
venv\Scripts\activate o source venv/bin/activate
      # Windows              # Linux/Mac

pip install -r requirements.txt

python manage.py migrate

python manage.py createsuperuser
Ingresar datos: Usuario, correo y contraseña
(Es necesario para manejar todo desde el panel de admin)

python manage.py runserver
