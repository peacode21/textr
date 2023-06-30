import os,random,string,requests

from flask import render_template,request,session,flash,redirect,url_for

import json

from sqlalchemy.sql import text,desc

from sqlalchemy import or_

from werkzeug.security import generate_password_hash,check_password_hash

from textr import app,db

from textr.models import User