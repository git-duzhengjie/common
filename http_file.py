import urllib2
import urllib


def simple_http_down(url):
    file_name = urllib.unquote(url).decode('utf-8').split('/')[:-1]
    urllib.urlretrieve(url, file_name)


def big_http_down(url):
    file_name = urllib.unquote(url).decode('utf-8').split('/')[:-1]
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer_ = u.read(block_sz)
        if not buffer_:
            break
        file_size_dl += len(buffer_)
        f.write(buffer_)
    f.close()


def http_up():
    # test_client.py
    from poster.encode import multipart_encode
    from poster.streaminghttp import register_openers
    import urllib2

    # Register the streaming http handlers with urllib2
    register_openers()

    # Start the multipart/form-data encoding of the file "DSC0001.jpg"
    # "image1" is the name of the parameter, which is normally set
    # via the "name" parameter of the HTML <input> tag.

    # headers contains the necessary Content-Type and Content-Length
    # data_gen is a generator object that yields the encoded parameters
    data_gen, headers = multipart_encode({"image1": open("DSC0001.jpg")})

    # Create the Request object
    request = urllib2.Request("http://localhost:5000/upload_image", data_gen, headers)
    # Actually do the request, and get the response
    print urllib2.urlopen(request).read()