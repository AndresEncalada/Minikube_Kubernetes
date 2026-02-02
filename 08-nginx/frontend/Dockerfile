FROM nginx:alpine

# Borramos la config por defecto de Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copiamos NUESTRA configuración
COPY default.conf /etc/nginx/conf.d/

# Copiamos NUESTRO html
COPY index.html /usr/share/nginx/html/