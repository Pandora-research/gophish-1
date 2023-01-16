# gophish

GoPhish automation

Licensed under GNU GPLv3.

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

**Create new Landing page**

```python3
python import-landing-page.py -n 'Landing page 1' -p 'template.html'
```

**Create new user groups (create group per user)**

```python3
python import-users.py -c 'users-template.csv' -t -g
```

**Create one new user group (all users in the same group)**

```python3
python import-users.py -c 'users-template.csv' -n 'User Group 1' -t
```

**Export User Groups to CSV file (To create user_groups - email_templates matches)**

```python3
python export-groups.py -c users_groups-email_templates.csv
```

---
