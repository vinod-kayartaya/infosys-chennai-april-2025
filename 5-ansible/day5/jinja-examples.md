# Real-World Examples

## Example 1: Apache Virtual Host Configuration

```jinja2
<VirtualHost *:80>
    ServerName {{ ansible_fqdn }}
    {% if server_aliases is defined %}
    {% for alias in server_aliases %}
    ServerAlias {{ alias }}
    {% endfor %}
    {% endif %}

    DocumentRoot /var/www/html

    <Directory /var/www/html>
        Options Indexes FollowSymLinks
        AllowOverride All
        {% if ansible_distribution_major_version | int >= 8 %}
        Require all granted
        {% else %}
        Order allow,deny
        Allow from all
        {% endif %}
    </Directory>

    # Logging
    ErrorLog /var/log/httpd/{{ ansible_hostname }}_error.log
    CustomLog /var/log/httpd/{{ ansible_hostname }}_access.log combined

    # Security headers
    {% if ssl_enabled | default(false) %}
    Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
    {% endif %}
    Header always set X-Content-Type-Options nosniff
    Header always set X-Frame-Options DENY
</VirtualHost>

{% if ssl_enabled | default(false) %}
<VirtualHost *:443>
    ServerName {{ ansible_fqdn }}
    {% if server_aliases is defined %}
    {% for alias in server_aliases %}
    ServerAlias {{ alias }}
    {% endfor %}
    {% endif %}

    DocumentRoot /var/www/html

    SSLEngine on
    SSLCertificateFile {{ ssl_cert_path | default('/etc/ssl/certs/server.crt') }}
    SSLCertificateKeyFile {{ ssl_key_path | default('/etc/ssl/private/server.key') }}

    # Modern SSL configuration
    SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384
    SSLHonorCipherOrder off
    SSLSessionTickets off
</VirtualHost>
{% endif %}
```

## Example 2: System Monitoring Configuration

```jinja2
# System Monitoring Configuration for {{ ansible_hostname }}
# Generated on {{ ansible_date_time.iso8601 }}

[system]
hostname = {{ ansible_hostname }}
fqdn = {{ ansible_fqdn }}
os_family = {{ ansible_os_family }}
distribution = {{ ansible_distribution }} {{ ansible_distribution_version }}
architecture = {{ ansible_architecture }}

[hardware]
cpu_cores = {{ ansible_processor_cores }}
cpu_threads = {{ ansible_processor_count }}
memory_mb = {{ ansible_memtotal_mb }}
memory_gb = {{ (ansible_memtotal_mb / 1024) | round(1) }}

{% if ansible_processor_cores >= 4 and ansible_memtotal_mb >= 8192 %}
performance_class = high
monitoring_interval = 30
{% elif ansible_processor_cores >= 2 and ansible_memtotal_mb >= 4096 %}
performance_class = medium
monitoring_interval = 60
{% else %}
performance_class = low
monitoring_interval = 120
{% endif %}

[network]
{% for interface in ansible_interfaces %}
{% if interface != 'lo' and ansible_facts[interface]['active'] | default(false) %}
[network.{{ interface }}]
ip_address = {{ ansible_facts[interface]['ipv4']['address'] | default('N/A') }}
mac_address = {{ ansible_facts[interface]['macaddress'] | default('N/A') }}
{% if ansible_facts[interface]['ipv4'] is defined %}
monitor_connectivity = true
ping_target = {{ ansible_facts[interface]['ipv4']['gateway'] | default(ansible_default_ipv4.gateway) }}
{% endif %}
{% endif %}
{% endfor %}

[storage]
{% for mount in ansible_mounts %}
{% if mount.mount != '/dev' and mount.mount != '/sys' and mount.mount != '/proc' %}
[storage.{{ mount.mount | replace('/', '_root') | replace('/', '_') }}]
mount_point = {{ mount.mount }}
device = {{ mount.device }}
filesystem = {{ mount.fstype }}
size_gb = {{ (mount.size_total / 1024**3) | round(1) }}
{% set usage_percent = ((mount.size_total - mount.size_available) / mount.size_total * 100) | round(1) %}
current_usage_percent = {{ usage_percent }}
{% if usage_percent > 90 %}
alert_level = critical
{% elif usage_percent > 80 %}
alert_level = warning
{% else %}
alert_level = normal
{% endif %}
{% endif %}
{% endfor %}

[services]
service_manager = {{ ansible_service_mgr }}
{% if ansible_os_family == "RedHat" %}
package_manager = {{ 'dnf' if ansible_distribution_major_version | int >= 8 else 'yum' }}
{% elif ansible_os_family == "Debian" %}
package_manager = apt
{% endif %}

[alerts]
{% if ansible_memtotal_mb < 2048 %}
low_memory_warning = true
{% endif %}
{% if ansible_processor_cores < 2 %}
low_cpu_warning = true
{% endif %}
{% set root_mount = ansible_mounts | selectattr('mount', 'equalto', '/') | first %}
{% if root_mount and ((root_mount.size_total - root_mount.size_available) / root_mount.size_total * 100) > 85 %}
disk_space_warning = true
{% endif %}
```

## Example 3: Nginx Load Balancer Configuration

```jinja2
# Nginx Load Balancer Configuration
# Server: {{ ansible_hostname }} ({{ ansible_default_ipv4.address }})
# Generated: {{ ansible_date_time.iso8601 }}

worker_processes {{ ansible_processor_cores }};
worker_connections {{ 1024 * ansible_processor_cores }};

upstream backend_servers {
    {% for server in backend_servers %}
    server {{ server.ip }}:{{ server.port | default(80) }} weight={{ server.weight | default(1) }}{% if server.backup | default(false) %} backup{% endif %};
    {% endfor %}

    # Health checks
    {% if ansible_memtotal_mb >= 4096 %}
    keepalive 32;
    {% else %}
    keepalive 16;
    {% endif %}
}

server {
    listen 80;
    server_name {{ ansible_fqdn }} {{ server_aliases | default([]) | join(' ') }};

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";

    # Logging
    access_log /var/log/nginx/{{ ansible_hostname }}_access.log;
    error_log /var/log/nginx/{{ ansible_hostname }}_error.log;

    # Rate limiting based on server capacity
    {% if ansible_memtotal_mb >= 8192 %}
    limit_req zone=api burst=20 nodelay;
    {% elif ansible_memtotal_mb >= 4096 %}
    limit_req zone=api burst=10 nodelay;
    {% else %}
    limit_req zone=api burst=5 nodelay;
    {% endif %}

    location / {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts based on system performance
        {% if ansible_processor_cores >= 4 %}
        proxy_connect_timeout 5s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
        {% else %}
        proxy_connect_timeout 10s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        {% endif %}
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }

    # Server status
    location /server-info {
        access_log off;
        return 200 '{"hostname":"{{ ansible_hostname }}","ip":"{{ ansible_default_ipv4.address }}","memory_gb":{{ (ansible_memtotal_mb/1024)|round(1) }},"cpu_cores":{{ ansible_processor_cores }}}';
        add_header Content-Type application/json;
    }
}

{% if ssl_enabled | default(false) %}
server {
    listen 443 ssl http2;
    server_name {{ ansible_fqdn }} {{ server_aliases | default([]) | join(' ') }};

    ssl_certificate {{ ssl_cert_path }};
    ssl_certificate_key {{ ssl_key_path }};

    # Modern SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    # HSTS
    add_header Strict-Transport-Security "max-age=63072000" always;

    # Same location blocks as HTTP with additional SSL headers
    location / {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }
}
{% endif %}
```

---
