# Note For Kalle:
- I Hardcorded My Default Credentials For Cloud Backup So You Can Test That

- Option 10 Allow To Copy Password On Clipboard If Present In Database When You Visit A Website. You Can Only Run This 10 Min In One Go

- Only Windows Tested For Now. So Prefered OS To Run Is Windows 10

- I Used Unicode For Fun. So You Want Them To Visiable Then Run `_pw_manager.py` After Installation In **VsCode** Or **Windows Terminal**

- This Project Still Contains Bugs Because I'm Still Working On It. But I Tried To Resolve All Issues Related To Password Security

# Installation

1. Run ```python _install.py```
2. To Open iThACK PassMag Run ```python _pw_manager.py```

# Warnings

1. Default Password ```don't use weak master password```
2. Change Default Password First

# Features
- AES-256 Bit Encryption With Salting (Rainbow Table Secure)

- Hash Verification For Master Password And Created With Key-Derivation Function (Brute Force Secure)

- Local And Cloud Backup

- Import And Export Passwords Into CSV

- Auto Clipboard Password Copier *(Option 10)*

- Configuration Checkup After Installation *(Under Dev.)*

- Check Is Your Passwords Are Shown In Data Breaches And On Dark Web

- Passwords Are Never Exposed To Variable For Long Time. Accomplished By Only Using Variables In Block Scope (No Memory Leak. This Measure Has Taken For Binary Exploitition Pentesters)