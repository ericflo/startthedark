set(
    fab_hosts = ['startthedark.com'],
    fab_user = 'startthedark',
)

def unlink_nginx():
    'Un-link nginx rules for startthedark.'
    sudo('rm -f /etc/nginx/sites-enabled/startthedark.com')
    sudo('/etc/init.d/nginx reload')

def link_nginx():
    'Link nginx rules for startthedark'
    sudo('ln -s /etc/nginx/sites-available/startthedark.com /etc/nginx/sites-enabled/startthedark.com')
    sudo('/etc/init.d/nginx reload')

def deploy():
    'Deploy startthedark.'
    local('bash make_prod_css.sh')
    local('git commit -a -m "Rebuilt Prod CSS For Commit"')
    local('git push')
    run('cd /var/www/startthedark.com/startthedark; git pull;')
    run('cd /var/www/startthedark.com/startthedark; /usr/bin/python manage.py syncdb')
    sudo('/etc/init.d/apache2 reload')
