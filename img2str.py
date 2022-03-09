import base64

def img2str(filename, file):
    img = open(file, 'rb')
    content = 'image_bytes = {}\n'.format(base64.b64encode(img.read()))
    img.close()
    with open(f'img2str_{filename}.py', 'a') as f:
        f.write(content)

if __name__ == '__main__':
    img2str('catan_logo', 'C:\\Users\\wjrm5\\Documents\\Personal projects\\Catan\\frontend\\assets\\catan_logo.png')
    img2str('celebration', 'C:\\Users\\wjrm5\\Documents\\Personal projects\\Catan\\frontend\\assets\\celebration.png')