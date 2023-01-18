### Get tracking codes from Plesk Logs

```
cat access_ssl_log |grep https://<domain.example>/?|cut -d$' ' -f11|sed 's@"https://<domain.example>/?@@'|sed 's@"@@'

cat access_ssl_log.processed |grep https://<domain.example>/?|cut -d$' ' -f11|sed 's@"https://<domain.example>/?@@'|sed 's@"@@'
```

### Get tracking codes from Plesk Logs remotely

```
ssh user@<ip_address> "cat /var/www/vhosts/<domain.example>/logs/access_ssl_log|grep https://<domain.example>/?|cut -d$' ' -f11|sed 's@""https://<domain.example>/?@@'|sed 's@""@@'"

ssh user@<ip_address> "cat /var/www/vhosts/<domain.example>/logs/access_ssl_log.processed|grep https://<domain.example>/?|cut -d$' ' -f11|sed 's@""https://<domain.example>/?@@'|sed 's@""@@'"

ssh user@<ip_address> "cat /var/www/vhosts/<domain.example>/logs/access_ssl_log|grep https://<domain.example>/?|cut -d$' ' -f11|sed 's@""https://<domain.example>/?@@'|sed 's@""@@' && cat /var/www/vhosts/<domain.example>/logs/access_ssl_log.processed|grep https://<domain.example>/?|cut -d$' ' -f11|sed 's@""https://<domain.example>/?@@'|sed 's@""@@'"
```

---
