# Unprivileged nginx: runs as a non-root user and listens on 8080
FROM nginxinc/nginx-unprivileged:alpine
COPY index.html /usr/share/nginx/html/
USER 101
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget -q --spider http://127.0.0.1:8080/ || exit 1
