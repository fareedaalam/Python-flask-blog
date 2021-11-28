#linux hosting
	## https://youtu.be/GQcUYFFKUSA
	##nginx https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04
	##apache https://www.digitalocean.com/community/tutorials/how-to-install-linux-apache-mysql-php-lamp-stack-on-ubuntu-20-04
1.sudo apt-get update (up to date linux server)
2.sudo apt-get install apache2 (install apache hosting server)
3.sudo apache2ctl configtest (check config file is exists)
4. vim /etc/apache2/apache2.conf (edit config file to add server name )
    4.1 Press insert and write at the end of file
        ServerName <yourhostIP>
    4.2 Svae the file with Button Esc, :wq Enter
5. sudo ufw app list (Check exists app on server)
6. sudo ufw app info "Apache Full" (Allow web traffic)
7. run you ip on any browser to check apache server is installed or not
8. sudo apt-get install mysql-server
9. sudo apt-get install php
10. sudo apt-get install libapache2-mod-php php-mcrypt php-mysql (install all helper package)
11.  vim /etc/apache2/mods-enabled/dir.conf (Edit dir config file)
    11.1 Swap index.html to index.php vice versa
    Restart (sudo service apache2 restart)
12. sudo apt-get install phpmyadmin (install php my admin)
    12.1 Restart Again (sudo service apache2 restart)
	
	
#configure wsgi on apache2	
1.sudo apt-get install libapache2-mod-wsgi-py3
2.sudo a2enmod wsgi








#SQL-getRowCount
     posts = Posts.query.filter_by().all()[0:params['no_of_posts']]

#flask-the flash() method of the flask module passes the message to the next request
    #which is an HTML template
    #flash('No file part') on python end point
    {% with messages = get_flashed_messages() %}
         {% if messages %}
               {% for message in messages %}
                    <p>{{ message }}</p>
               {% endfor %}
         {% endif %}
      {% endwith %}

#flask- Send Email
    pip install flask-mail

    app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-pwd']
    )

    mail = Mail(app)

     # mail.send_message('New message from ' + email,
        #                   sender=email,
        #                   recipients=[params['gmail-user']],
        #                   body=message + "\n" + contact_no
        #                 )
        msg = Message('New message from ' + email,
                      recipients=[params['gmail-user']],
                      sender=email,
                      body=message + "\n" + contact_no
                      )
        mail.send(msg)
        #Note :- set low secure your gmail account form google setting

# config.json file
    {
  "params": {
    "local_uri": "mysql+pymysql://root:@localhost/codethunder",
    "gh_uri": "https://github.com/fareedaalam",
    "blog_name": "Coding Thunder 1",
    "tag_line": "A Blog To Show Your Skill"
  }
}
#flask- read config file
    with open('config.json', 'r') as c:
        params= json.load(c)["params"]
    print(params['local_uri'])

#flask- Send and object to template
  return render_template('index.html',params=params)

#flask- Read object in template
    {{params['blog_name']}}

