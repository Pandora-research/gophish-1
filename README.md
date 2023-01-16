# gophish
Tools and scripts for GoPhish automation

---

### Office 365 SMTP settings

* SMTP From (put email address only): myname@mydomain.com
* SMTP Host: smtp.office365.com:587
* SMTP Username: myname@mydomain.com

---

### Usage

**Create new Sending Profile**

```python3
python import-sending-profile.py -n 'SMTP Test Profile' -x 'smtp.office365.com' -p 587 -f myname@gmail.com
```

---
