#About Deals API
[![Generic badge](https://img.shields.io/badge/Django-blue.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/DjangoRestFramework-orange.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Postgres-grey.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Celery-gree.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Redis-red.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Docker-black.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/Gunicorn-green.svg)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/nginx-black.svg)](https://shields.io/)


Deals Api is a service on django rest framework by which you can upload csv file with deals to database.

<img src="https://vk.com/doc102586510_584476038"/>

You can also get by 'GET' request top five deals by customers with:
- _username of customer._
- _sum of money which was spent._
- _name of gems that were bought by at least two of the top five list 
  and this customer is one of these buyers._
  
<img src="https://vk.com/doc102586510_584475896"/>

___

## Usage with Docker
The first you need to install docker and docker-compose on your host:<br>
https://losst.ru/ustanovka-docker-na-ubuntu-16-04

Then you need to clone deals-drf repo on your host.<br> 
So, in your terminal you have to make:

```bash
git clone https://github.com/kirillmaiboroda1996/deals-drf.git
```

###Development
If you want to get project for development, from docker-compose.yml directory make:

```bash
docker-compose up --build -d
```
- `--build` means you are building the docker-compose file
- `-d` means background mode

Now you can open service in your browser:<br>
http://127.0.0.1:8000/api/deals/


###Production
If you want to get project for production, from docker-compose.prod.yml directory make:
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```
- use `docker-compose logs -f` for watching logs if something wrong, <br>
  or you can remove `-d` from docker-compose command.
  
- use `docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput` <br>
if you need migrations
  
- use `docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear`<br>
to collect static for nginx.

Now you can open service in your browser:<br>
http://localhost:1337/api/deals/

##About urls

- monitoring workers by a flower:<br>
http://localhost:5555
  
- api documentation:<br>
http://localhost:8000/swagger/
  
- get result of task:<br>
http://localhost:8000/get-request-status/{task_id}/