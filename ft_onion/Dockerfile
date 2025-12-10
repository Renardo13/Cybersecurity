FROM ubuntu:22.04

# Installer nginx, tor et openssh
RUN apt-get update && \
    apt-get install -y nginx tor openssh-server && \
    mkdir /var/run/sshd

# Configurer SSH pour le port 4242
RUN sed -i 's/#Port 22/Port 4242/' /etc/ssh/sshd_config && \
    echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config

# Copier fichiers
COPY index.html /usr/share/nginx/html/index.html
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY torrc /etc/tor/torrc

# Exposer ports
EXPOSE 4242 80

# Lancer services en parallèle
CMD /usr/sbin/sshd -D & nginx -g 'daemon off;' & tor -f /etc/tor/torrc