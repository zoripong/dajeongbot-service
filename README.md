# 다정봇 서버 [![Build Status](https://travis-ci.org/zoripong/DajeongBot-server.svg?branch=master)](https://travis-ci.org/zoripong/DajeongBot-server)

다정봇은 당신의 하루를 챗봇과의 대화 중 자연스럽게 기록해줄 챗봇 다이어리입니다.  서비스에 대한 자세한 내용은 [android 레포지토리](https://github.com/zoripong/DajeongBot)를 참고해주세요.

## List of API

다정봇 서버에서는 다음과 같은 api들을 제공합니다.

> Event

사용자의 일정에 관련된 CRUD api 를 제공합니다.

> User
 
로그인, 회원가입 등 회원을 관리합니다.
  
> Me
 
사용자의 모든 정보들에 대해 관리합니다.
  
> Message
 
 메세지를 주고 받을 수 있는 api입니다.
  
## Software Stack
 - Chatbot Engine
     - [Danbee](https://www.danbee.ai/)
 
 - Main Requirements  
     - [flask](http://flask.pocoo.org/)
     - [Celery](http://docs.celeryproject.org/en/latest/index.html)
     - [Celery-Beat](http://docs.celeryproject.org/en/latest/reference/celery.beat.html)
     - [PyFCM](https://github.com/olucurious/PyFCM)
     - [Flask SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)
 
 - Environment
     - [python 3.5.2](https://www.python.org/downloads/release/python-352/)
     - nginx
     - MySQL
     - Ubuntu 16.04
     - [virtualenv](https://virtualenv.pypa.io/en/stable/#)

 
## Server Structure
![server structure](https://scontent-icn1-1.xx.fbcdn.net/v/t1.15752-9/42575664_477819682722181_6619681210396311552_n.png?_nc_cat=105&oh=6421c36c3de3c5978bd059088c3075b0&oe=5C51C40E)
 
## Extras
 - 지속적으로 보완 중에 있습니다. (사용자 의도 파악이 가능한 문장 추가)
 - author [zoripong](https://github.com/zoripong/)
 - CONTACT ME : <mailto:devuri404@gmail.com>
