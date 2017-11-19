FROM httpd:alpine
EXPOSE 80

RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    pip3 install --upgrade pip setuptools pyyaml && \
    rm -r /root/.cache

COPY authenticator /usr/local/apache2/htdocs
COPY config/httpd.conf /usr/local/apache2/conf.d/authenticator.conf
RUN echo "Include /usr/local/apache2/conf.d/authenticator.conf" >> /usr/local/apache2/conf/httpd.conf;

COPY config/entrypoint.sh /entrypoint.sh
RUN chmod 750 /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
