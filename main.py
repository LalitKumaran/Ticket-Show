from web import createapp

app=createapp()

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=12345)

