from bottle import Bottle, request, response, static_file
import os
import magic,ngrok,threading,webview,webbrowser

ngrok.set_auth_token(open("tokun").read())

app = Bottle()

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','zi_','sb3','sprite3'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

@app.route("/")
def aaaaa():
    return """<style>chat{
  display:block;
  font-size:100%;
  margin:10% 20% 20% 20%;
}
chat>*{
  width: auto;
}
chat>form>textarea{
  font-size:75%;
　width: 50vh;
　height: 30vh;
  resize: none;
}
chat>form{
  width: 100%;
　height: 100%;
}
flex{
  display:flex;
}
flex>button{
  margin-top:8%;
  margin-left:3%;
  height: 30%;
  font-size:20%;
}
.botton{
  background:#dddddd;
  border:2px solid #777777;
  box-shadow: 2px 2px 4px;
  border-radius:5% 5% 5% 5%;
  margin:3%;
}
.botton:hover{
  background:#cccccc;
  border:2px solid #aaaaaa;
  box-shadow: 2px 2px 4px;
  border-radius:5%;
  margin:3%;
}
ul{
  list-style: none;
}
a{
  text-decoration: none;
  color:black;
}
red{
  color:red;
}</style>
<title>入力画面</title>
<chat>
<h1>投稿</h1>
<form action="/upload" method="POST" enctype="multipart/form-data">
  <input name="file" type="file"><br>
  <input type="submit">
</form>
"""
class Api:
    def __init__(self):
        self.window = None
    def openweb(self,url):
        webbrowser.open(url)

# ファイルをアップロードするエンドポイント
@app.post('/upload')
def upload_file():
    upload_folder = 'uploads'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    upload_file = request.files.get('file')
    if upload_file:
        # ファイルサイズのチェック
        if upload_file.content_length > MAX_FILE_SIZE:
            response.status = 400
            return {'status': 'error', 'message': 'File size exceeds the limit.'}

        # ファイルのマジックナンバーを取得
        file_magic = magic.Magic(mime=True)
        mime_type = file_magic.from_buffer(upload_file.file.read(1024))

        # ファイルのMIMEタイプから拡張子を取得
        ext = mime_type.split('/')[1]
        # アップロードされたファイルのファイル名を取得
        filename = upload_file.raw_filename

        # ファイルを保存
        file_path = os.path.join(upload_folder, filename)
        upload_file.file.seek(0)  # ファイルポインタを先頭に戻す
        upload_file.save(file_path)
        return {'status': 'success', 'message': 'File uploaded successfully.', 'file_path': file_path}
    else:
        response.status = 400
        return {'status': 'error', 'message': 'No file uploaded.'}

# ファイルをダウンロードするエンドポイント
@app.get('/uploads/<filename>')
def download_file(filename):
    file_path = os.path.join('uploads', filename)
    if os.path.exists(file_path):
        return static_file(filename, root='uploads')
    else:
        response.status = 404
        return {'status': 'error', 'message': 'File not found.'}

# ファイル一覧を取得するエンドポイント
@app.get('/upload')
def list_files():
    upload_folder = 'uploads'
    files = []
    for filename in os.listdir(upload_folder):
        if os.path.isfile(os.path.join(upload_folder, filename)):
            files.append(filename)
    return {'files': files}
import time
def run():
    app.run(host='0.0.0.0', port=25256)
listener = ngrok.forward(25256, authtoken_from_env=True)
if True:
    aaa=threading.Thread(target=run)
    aaa.start()
    time.sleep(0.05)
    window=webview.create_window('公開しました!',js_api = Api(),html=f'<a href="javascript:pywebview.api.openweb(\'{listener.url()}\')">{listener.url()}</a>')
    webview.start() # QTを利用

