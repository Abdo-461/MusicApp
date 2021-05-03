from flask import Flask, render_template, request, flash , redirect , url_for , json , session
import boto3
import re
from boto3.dynamodb.conditions import Key

#create dynamo object with access and secret keys
dynamodb = boto3.resource('dynamodb',aws_access_key_id='',
                                     aws_secret_access_key='',
                                     region_name='us-east-1')

#s3 object to define s3 bucket
s3 = boto3.resource('s3', aws_access_key_id='',
                          aws_secret_access_key='',
                          region_name='us-east-1')
bucket = s3.Bucket('musicimages6969')

app = Flask(__name__)

global username

#logout function
@app.route('/logout')
def logout():
    return render_template('login.html')

#first page to load when app is launched
@app.route('/',methods=['POST','GET'])
def login():
    if request.method=='POST':
        #get user information from form
        email = request.form['email']
        password = request.form['password']
        #get table
        table = dynamodb.Table('login')
        #query table and comapre email
        response = table.query(
                KeyConditionExpression=Key('email').eq(email)
        )
        #put results in items
        items = response['Items']
        session['user_name'] = items[0]['user_name']
        #comapre password
        if password == items[0]['password']:
            return redirect(url_for('dashboard'))

        flash("Email or Password Invalid")
    return render_template('login.html')


#register page
@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        #get user information from form
        email=request.form['email']
        username=request.form['username']
        password=request.form['password']
        #get table
        table=dynamodb.Table('login')
        #query table and comapre email
        response = table.query(
                KeyConditionExpression=Key('email').eq(email)
        )
        #put results in items
        items = response['Items']
        if not items:
            #put user information into database table
            table.put_item(
                Item={
                    'email':email,
                    'user_name':username,
                    'password':password
                }
            )
            #redirect user to login page after signup
            flash('You are signed up! Please login!')
            return render_template('login.html')

        flash("Email already Exists")
    return render_template('register.html')

#create a url reference for dashboard for refreshing purposes
@app.route('/dashboard')
def dashboard():
    #reference table
    table=dynamodb.Table('Subscription')
    #query table
    response = table.query(
            KeyConditionExpression=Key('user_name').eq(session['user_name'])
        )
    #put results in items
    global subscription
    subscription = response['Items']
    return render_template('dashboard.html' ,subscriptions=subscription, username=session['user_name'])
    
global artistImage
#retrive music information based on title, artist, year
@app.route('/query',methods=["POST","GET"])
def query():
    #fetch user information from form
    title=request.form['title']
    artist=request.form['artist']
    year=request.form['year']
    #get table
    table=dynamodb.Table('Music')
    #query table with given information
    response = table.query(
        KeyConditionExpression=Key('title').eq(title)
    )
    #get image
    pattern = re.compile(artist+".jpg")
    for file in bucket.objects.all():
        if pattern.match(file.key):
             artistImage=file.key
    #put response result in items
    global songs
    songs = response['Items']
    #validate list
    if not songs:
        flash("No results is retrieved,Please query again")
        return redirect(url_for('dashboard'))
    #refresh page with the items in the items list
    return render_template('dashboard.html', music=songs,image=artistImage,username=session['user_name'])

#function for a user to subscribe to different music artist
@app.route('/subscription',methods=["POST"])
def subscriptions():
    #reference table
    table=dynamodb.Table('Subscription')
    #get music information
    title = request.form['titleSub']
    artist = request.form['artistSub']
    year = request.form['yearSub']
    image = request.form['imageSub']
    #upload items to subscription table
    table.put_item(Item = {
        'user_name':session['user_name'],
        'title':title,
        'artist':artist,
        'year':year,
        'image':image
})
    return redirect(url_for('dashboard'))

#function for a user to remove a music subscription
@app.route('/remove',methods=["POST"])
def remove():
    #fetch the title of the entry we want to delete
    titleid = request.form['titleid']
    #get table
    table=dynamodb.Table('Subscription')
    #query table
    response = table.query(
            KeyConditionExpression=Key('user_name').eq(session['user_name'])
        )
    for item in response['Items']:
        #delete item off database
        table.delete_item(Key = {
            'user_name':item['user_name'],
            'title': titleid
            }
        )
    return redirect(url_for('dashboard'))

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

if __name__ == '__main__':

    app.run(host='127.0.0.1', port=4242, debug=True)
