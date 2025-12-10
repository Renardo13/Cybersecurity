FROM ubuntu:22.04

# Installer nginx, tor et openssh
RUN apt-get update && \
    apt-get install -y nginx tor openssh-server && \
    mkdir -p /var/run/sshd

# Configurer SSH pour le port 4242
RUN sed -i 's/#Port 22/Port 4242/' /etc/ssh/sshd_config && \
    echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config

# Copier fichiers statiques
COPY index.html /usr/share/nginx/html/index.html
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY torrc /etc/tor/torrc

# Exposer ports pour SSH et Nginx
EXPOSE 4242 80

# Lancer les services au démarrage
CMD service ssh start && service nginx start && tor -f /etc/tor/torrc && tail -f /dev/null
