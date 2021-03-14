FROM fedora:latest
ADD install-pkgs.sh /
RUN  echo "nameserver 8.8.8.8" > /etc/resolv.conf \
     && /install-pkgs.sh
