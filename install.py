import os

def copy_file(source, dest, buffer_size=1024*1024):
    while True:
        copy_buffer = source.read(buffer_size)
        if not copy_buffer:
            break
        dest.write(copy_buffer)

def install_app(app, db):
    print ''
    print 'Simple note prepareing install'
    print '-' * 20

    print 'Creating database boilerplate'

    db.create_all()

    print 'Database created successfully'
    print '-' * 20

    print 'Make template directory'

    # prepare tmp directory
    if not os.path.isdir(app.config['TMP_DIR']):
        os.mkdir(app.config['TMP_DIR'])

    print 'Template directory made successfully'
    print '-' * 20

    print 'Creating configuration files'

    basedir = os.path.abspath(os.path.dirname(__file__))
    config_dir = os.path.join(basedir, 'config')
    development_config = os.path.join(config_dir, 'development.py')
    production_config = os.path.join(config_dir, 'production.py')


    with open(development_config, 'rb') as src, open(production_config, 'wb') as dest:
        copy_file(src, dest)

    print 'Production config file created,'
    print 'Please set the SECRET_KEY and SQLALCHEMY_DATABASE_URI'
    print 'and other important fields.'
