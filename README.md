# gophish

GoPhish automation

* Send different email to different recipients.
* Track if user clicked the link when an external phishing page is being deployed (track user unique code in the web server logs).

Licensed under GNU GPLv3.

---

### Office 365 SMTP settings

* SMTP From (put email address only): myname@mydomain.com
* SMTP Host: smtp.office365.com:587
* SMTP Username: myname@mydomain.com

---

### Usage

#### Import new Sending Profile

```python3
python import-sending-profile.py -n "SMTP Test Profile" -x "smtp.office365.com" -p 587 -f "myname@gmail.com"
```

#### Import new Landing page

```python3
python import-landing-page.py -n "Landing page 1" -p "template.html" -r "https://google.com"
```

#### Import new user groups (create group per user)

```python3
python import-users.py -c "users-template.csv" -t -g
```

#### Import one new user group (all users in the same group)

```python3
python import-users.py -c "users-template.csv" -n "User Group 1" -t
```

#### Export User Groups to CSV file (To create user_groups - email_templates matches)

```python3
python export-groups.py -c "users_groups-email_templates.csv"
```

#### Edit users_groups-email_templates.csv file and fill in the email templates for each user group.

#### Generate final Email templates for each group of users

```python3
python create-templates.py -c "users_groups-email_templates.csv" -t "email-templates" -d "final-templates"
```

#### Import new templates

```python3
python import-templates.py -t "final-templates" -s "Microsoft 365 security: You have messages in quarantine"
```

#### Import new campaigns - Send emails

```python3
python import-campaigns.py -c "campaigns.csv"
```

#### Export Users

```python3
python export-users.py -c "users-exported.csv"
```

#### Export Groups

```python3
python export-groups.py -c "groups-exported.csv"
```

#### Export Statistics

```python3
python export-stats.py -c "stats-exported.csv"
```

#### Delete all Groups

```python3
python delete-groups.py
```

---
