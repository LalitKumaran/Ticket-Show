from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from . import db
from .models import User,Show,Venue,Booking
import datetime
import base64
from uuid import uuid4

views=Blueprint('views',__name__)

alive=0

@views.route('/',methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@views.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(user_id=email).first()
        if user:
            if user.password == password:
                global alive
                alive = user
                flash('Logged in')
                if(user.user_type=="admin"):
                    return redirect(url_for('views.admin'))
                else:
                    return redirect(url_for('views.home'))
            else:
                flash('Incorrect password')
        else:
            flash('User does not exist.')
            return redirect(url_for('views.signup'))
    return render_template("./auth/login.html", user=alive)

@views.route('/logout',methods=['GET','POST'])
def logout():
    global alive
    alive = 0
    flash('Logged out successfully.')
    return redirect(url_for('views.login'))

@views.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        city = request.form.get('city')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(user_id=email).first()
        if user:
            flash('An account has already been created with this email.')
        elif password1 != password2:
            flash('Passwords don\'t match.')
        else:
            new_user = User(user_id=email, username=username, email=email,  password=password1, phone=phone, city=city, user_type="user")
            db.session.add(new_user)
            db.session.commit()
            flash('Successfully signed up.')
            return redirect(url_for('views.login'))

    return render_template("./auth/signup.html", user=alive)

@views.route('/admin',methods=['GET', 'POST'])
def admin():
    if(alive):
        show = Show.query.all()
        venue = Venue.query.all()
        if request.method=="POST":
            search = request.form.get("search")
            s = Show.query.filter_by(showname=search)
            v = Venue.query.filter_by(venuename=search)
            if(v):
                venue=v
            if(s):
                show=s
        return render_template("./admin/admin.html", user=alive,show=show,venue=venue)
    else:
        return render_template("./auth/login.html", user=alive)

@views.route('/admin/new',methods=['GET', 'POST'])
def newadmin():
    if(request.method=="POST"):
        if(alive):
            username = request.form.get('username')
            email = request.form.get('email')
            phone = request.form.get('phone')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')
            user = User.query.filter_by(user_id=email).first()
            if user:
                flash('An account has already been created with this email.')
            elif password1 != password2:
                flash('Passwords don\'t match.')
            else:
                new_user = User(user_id=email, username=username, email=email,  password=password1, phone=phone, user_type="admin")
                db.session.add(new_user)
                db.session.commit()
                flash('Successfully Created.')
                return redirect(url_for('views.admin'))
        else:
            return render_template("./admin/admin.html", user=alive)
    return render_template("./admin/newadmin.html")

@views.route('/home',methods=['GET', 'POST'])
def home():
    if(alive):
        show=Show.query.all()
        venue=Venue.query.all()
        if request.method=="POST":
            search = request.form.get("search")
            s = Show.query.filter_by(showname=search)
            v = Venue.query.filter_by(venuename=search)
            if(v):
                venue=v
            if(s):
                show=s
        if(alive.user_type=="admin"):
            return render_template('./admin/admin.html',show=show,venue=venue)
        else:
            return render_template('home.html',show=show,venue=venue)
    else:
        flash('Session Expired')
        return redirect(url_for('views.index'))

@views.route('/show',methods=['GET', 'POST'])
def show():
    if(alive):
        show = Show.query.all()
        if request.method=="POST":
            search = request.form.get("search")
            s = Show.query.filter_by(showname=search)
            if(s):
                show=s
        return render_template("shows.html",show=show)
    else:
        return redirect(url_for('views.index'))

@views.route('/venue',methods=['GET', 'POST'])
def venue():
    if(alive):
        venue = Venue.query.all()
        if request.method=="POST":
            search = request.form.get("search")
            v = Venue.query.filter_by(venuename=search)
            if(v):
                venue=v
        return render_template("venues.html",venue=venue)
    else:
        return redirect(url_for('views.index'))

@views.route('/newshow',methods=['GET', 'POST'])
def newshow():
    if alive != 0:
        if alive.user_type=="admin":
            show = Show.query.all()
            venue = Venue.query.all()
            if request.method == 'POST':
                #date = str(datetime.date.today())
                show_id = 'S'+str(uuid4())
                showname = request.form.get('showname')
                rating  = request.form.get('rating')
                date = request.form.get('date')
                time = request.form.get('time')
                tag = request.form.get('tag')
                price = request.form.get('price')
                venue = request.form.get('venue')
                category = request.form.get('category')
                cast = request.form.get("cast")
                lang = request.form.get("lang")
                duration = request.form.get("duration")
                file = request.files['poster']
                data = file.read()
                poster = base64.b64encode(data).decode('ascii') 
                seats = Venue.query.filter_by(venuename=venue).first().capacity
                s=Show.query.filter_by(showname=showname,date=date,time=time,venue=venue).first()
                if(s):
                    flash('Show exists')
                else:
                    new_show = Show(show_id=show_id, showname=showname, rating=rating, date=date, time=time, tag=tag, price=price, venue=venue, category=category, cast=cast, poster=poster,seats=seats, lang=lang)
                    db.session.add(new_show)
                    db.session.commit()
                    flash('Successfully added the show.')
                    return redirect(url_for('views.show')) 

            return render_template("./admin/addshow.html", user=alive, show=show, venue=venue)
        else:
            flash('Admin Only')
            return redirect(url_for('views.login'))
    else:
        flash('Session Expired')
        return redirect(url_for('views.login'))

@views.route('/newvenue',methods=['GET', 'POST'])
def newvenue():
    if alive != 0:
        if alive.user_type=="admin":
            venue = Venue.query.all()
            if request.method == 'POST':
                #date = str(datetime.date.today())
                venue_id = 'V'+str(uuid4())
                venuename = request.form.get('venuename')
                capacity  = request.form.get('capacity')
                location = request.form.get('location')
                type = request.form.get('type')
                file = request.files['image']
                data = file.read()
                image= base64.b64encode(data).decode('ascii') 
                new_venue= Venue(venue_id=venue_id, venuename=venuename, capacity=capacity, location=location, type=type, image=image)
                v = Venue.query.filter_by(venuename=venuename,location=location,type=type).first()
                if(v):
                    flash("Venue exists")
                else:
                    db.session.add(new_venue)
                    db.session.commit()
                    flash('Successfully added the Venue.')
                    return redirect(url_for('views.venue')) 
            return render_template("./admin/addvenue.html", user=alive, venue=venue)
        else:
            flash('Admin Only')
            return redirect(url_for('views.login'))
    else:
        flash('Session Expired')
        return redirect(url_for('views.login'))

@views.route('/profile',methods=['GET', 'POST'])
def profile():
    if alive != 0:
        book = Booking.query.all()
        show = Show.query.all()
        venue = Venue.query.all()
        if(request.method=="POST"):
            search = request.form.get("search")
            v = Show.query.filter_by(venue=search).first()
            s = Show.query.filter_by(showname=search).first()
            if(v):
                book=Booking.query.filter_by(show_id=v.show_id)
            elif(s):
                book=Booking.query.filter_by(show_id=s.show_id)
        return render_template("profile.html",user=alive,booking=book,show=show,venue=venue)
    else:
        return redirect(url_for('views.login'))

@views.route('/show/<show_id>', methods=['GET', 'POST'])
def viewshow(show_id):
    if alive != 0:
        show = Show.query.get(show_id)
        #book = Booking.query.all()
        venue = Venue.query.filter_by(venuename=show.venue).first()
        seatcount=1
        if(request.method=="POST"):
            seatcount=int(request.form.get("seatcount"))
        return render_template("viewshow.html",show=show,user=alive,venue=venue,seatcount=seatcount)
    else:
        return redirect(url_for('views.login'))

@views.route('/book/<show_id>,<seatcount>', methods=['GET', 'POST'])
def book(show_id,seatcount):
    seatcount=(int(seatcount))
    if alive != 0:
        show = Show.query.filter_by(show_id=show_id).first()
        venue = Venue.query.filter_by(venuename=show.venue).first()
        amount=seatcount*show.price
        return render_template('pay.html',show=show,user=alive,venue=venue,seatcount=seatcount,amount=amount)
    else:
        return redirect(url_for('views.login'))

@views.route('/pay/<show_id>,<seatcount>', methods=['GET', 'POST'])
def pay(show_id,seatcount):
    if alive != 0:
        show = Show.query.filter_by(show_id=show_id).first()
        '''subject="Ticket confirmed"
        msg="You booked "+str(count) + "for" + str(show.showname) + "on" + str(show.date) + "at" + str(show.time) +"from account"+ str(alive.username) + ""
        message=Message(subject,sender="22f2001140@ds.study.iitm.ac.in",recipients=[alive.email])
        message.body=msg
        mail.send(message)'''
        seatcount=int(seatcount)
        if(show.seats>=seatcount):
            book_id = "B"+str(uuid4())
            amount= show.price*seatcount
            new_book = Booking(booking_id=book_id,show_id=show.show_id, user_id=alive.user_id, seatcount=seatcount,amount=amount)
            #b = Booking.query.filter_by(show_id=show.show_id,user_id=alive.user_id)
            db.session.add(new_book)
            show.seats-=seatcount
            db.session.commit()
            flash('Tickets Booked')
        else:
            flash('Tickets Not avilable')
        return render_template('home.html',show=Show.query.all(),user=alive,venue=Venue.query.all())
    else:
        return redirect(url_for('views.login'))

@views.route('/venue/<venue_id>',methods=['GET','POST'])
def viewvenue(venue_id):
    if(alive!=0):
        venuename=Venue.query.filter_by(venue_id=venue_id).first().venuename
        show=Show.query.filter_by(venue=venuename)
        return render_template("shows.html",show=show)
    else:
        return redirect(url_for('views.login'))

@views.route('/removevenue/<venue_id>', methods=['GET', 'POST'])
def removevenue(venue_id):
    if alive != 0:
        if(alive.user_type=="admin"):
            venue = Venue.query.get(venue_id)
            db.session.delete(venue)
            db.session.commit()
            flash("Venue Removed")
        else:
            flash('Access denied')
        return redirect(url_for('views.venue'))
    else:
        return redirect(url_for('views.login'))

@views.route('/removeshow/<show_id>', methods=['GET', 'POST'])
def removeshow(show_id):
    if alive != 0:
        if(alive.user_type=="admin"):
            show = Show.query.get(show_id)
            db.session.delete(show)
            db.session.commit()
            flash("Show Removed")
        else:
            flash('Access denied')
        return redirect(url_for('views.show'))
    else:
        return redirect(url_for('views.login'))

@views.route('/updatevenue/<venue_id>', methods=['GET', 'POST'])
def updatevenue(venue_id):
    if alive != 0:
        if(alive.user_type=="admin"):
            venue = Venue.query.filter_by(venue_id=venue_id).first()
            if request.method == 'POST':
                venue.venuename = request.form.get('venuename')
                venue.capacity  = request.form.get('capacity')
                venue.location = request.form.get('location')
                venue.type = request.form.get('type')
                file = request.files['image']
                data = file.read()
                if data:
                    venue.image= base64.b64encode(data).decode('ascii') 
                db.session.commit()
                flash("Venue Updated")
            else:
                return render_template('./admin/updatevenue.html',venue=venue)
        else:
            flash('Access denied')
        return redirect(url_for('views.venue'))
    else:
        return redirect(url_for('views.login'))

@views.route('/updateshow/<show_id>', methods=['GET', 'POST'])
def updateshow(show_id):
    if alive != 0:
        if(alive.user_type=="admin"):
            show = Show.query.filter_by(show_id=show_id).first()
            if request.method == 'POST':
                show.showname = request.form.get('showname')
                show.rating  = request.form.get('rating')
                show.date = request.form.get('date')
                show.time = request.form.get('time')
                show.tag = request.form.get('tag')
                show.price = request.form.get('price')
                v = request.form.get('venue')
                if(v!=show.venue):
                    show.venue=v
                    show.seats = Venue.query.filter_by(venuename=show.venue).first().capacity
                show.category = request.form.get('category')
                show.cast = request.form.get("cast")
                show.lang = request.form.get("lang")
                show.duration = request.form.get("duration")
                file = request.files['poster']
                data = file.read()
                if data:
                    show.poster = base64.b64encode(data).decode('ascii') 
                db.session.commit()
                flash("Show Updated")
            else:
                return render_template('./admin/updateshow.html',show=show)
        else:
            flash('Access denied')
        return redirect(url_for('views.show'))
    else:
        flash('Session Expired')
        return redirect(url_for('views.login'))