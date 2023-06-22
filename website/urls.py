import io
import random
import string
from .models import URL,User
from flask_login import login_required
from flask import Blueprint, render_template, redirect, send_file, url_for,request, flash, jsonify
from .utils import db
from flask_login import current_user
from flask_caching import Cache
from . import cache




urls = Blueprint("urls", __name__)

@urls.route("/shorten", methods=['GET', 'POST'])
@login_required
def shorten_url():
  if request.method == "POST":
     username = current_user.email
     auth_user = User.query.filter_by(email=username).first()
     print(auth_user)
     print(username)
     long_url = request.form.get("original_url")
     url_name = request.form.get("name")
     custom_url = request.form.get("custom_url")

     if custom_url:
      found_url = URL.query.filter_by(custom_url=custom_url).first()
      
      if found_url:
                return jsonify ({"error":"Custom name already exists, go back and choose another "})
                
      else:
            short_url = custom_url
            print(short_url)
            new_url = URL(long_url, short_url, custom_url, auth_user.id, url_name)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("urls.dashboard"))
     else:
        short_url = generate_short_url()
        print(short_url)
        new_url = URL(original_url=long_url, short_url=short_url, custom_url=custom_url, users=auth_user.id, name=url_name)
        db.session.add(new_url)
        db.session.commit()
        return redirect(url_for("urls.dashboard"))

        
     
  else:
     return render_template('url.html', user=current_user)
  

@urls.route('/<short_url>')

def redirection(short_url):
    long_url = URL.query.filter_by(short_url=short_url).first()
    if long_url:
        long_url.visitors +=1

        db.session.commit()
        return redirect(long_url.original_url)
    else:
        return f'<h1>Url doesnt exist</h1>'
    


  
@urls.route('/all_urls')
@login_required

def display_all():
    active_user = current_user.email
    auth_user = User.query.filter_by(email=active_user).first()
    active_url = URL.query.filter_by(users=auth_user.id).all()
    return render_template('all_urls.html', vals=active_url)


      
def generate_short_url():
    characters = string.ascii_letters + string.digits
    random_url = ''.join(random.choice(characters) for _ in range(6))
    brief_url = URL.query.filter_by(short_url=random_url).first()
    if not brief_url:
      return random_url
    

import qrcode
from io import BytesIO
from base64 import b64encode



@urls.route('/generate-qrcode', methods=['GET','POST'])
def generateQR():
    
    data = request.form.get('link')
    """

    memory = BytesIO()
    img = qrcode.make(data)
    img.save(memory)
    memory.seek(0)

    base64_img = "data:image/png;base64," + b64encode(memory.getvalue()).decode('ascii')
    """
   

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill='black', back_color='white')
    img_io = io.BytesIO()
    qr_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(
         img_io, mimetype='image/png', 
         as_attachment=True, 
         download_name='qrcode.png'
      )

@urls.route('/delete/<int:id>')
@login_required
def delete(id):
    url = URL.query.get_or_404(id)
    if url:
        db.session.delete(url)
        db.session.commit()
        return redirect(url_for('urls.dashboard'))
    return 'URL not found.'

@urls.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_url(id):
    url = URL.query.get_or_404(id)
    if url:
        if request.method == 'POST':
            custom_url = request.form['custom_url']
            if custom_url:
                existing_url = URL.query.filter_by(custom_url=custom_url).first()
                if existing_url:
                    flash ('That custom URL already exists. Please try another one.')
                    return redirect(url_for('urls.edit_url', id=id))
                url.custom_url = custom_url
                url.short_url = custom_url
            db.session.commit()
            return redirect(url_for('urls.dashboard'))
        return render_template('edit.html', url=url)
    return 'URL not found.'

@urls.route("/dashboard")
@login_required
def dashboard():
    urls = URL.query.filter_by(users=current_user.id).order_by(URL.created_at.desc()).all()
    host = request.host_url
    return render_template('dashboard.html', urls=urls, host=host)