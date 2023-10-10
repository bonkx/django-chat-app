# Django chat app with Django Channel

With Redis, Celery, Celery-beat, Uvicorn

---

### Todo List

- [x] Auth
  - [x] Register
  - [x] Login
  - [x] Logout
- [x] Chat
  - [x] Add Contact
  - [x] Chat websocket
  - [x] Upload Image
- [x] Encrypt and Decrypt with RSA key

---

## How to Run

```bash
# clone the repo
$ git clone repo

# go into repo's directory
$ cd repo

# generate your RSA Private and Public Key
# copy and edit env file
$ cp .env.example .env

# build docker
$ make build

# start docker
$ make run
```

### Credit

[RSA Key Generator](https://cryptotools.net/rsagen)  
[django-chat-room](https://github.com/twtrubiks/django-chat-room)  
[github-actions](https://viandwi24.medium.com/github-actions-sederhana-untuk-testing-dan-deploy-ke-server-vps-a43976cd6f46)  
