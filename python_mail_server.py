from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import cgi
import app
import settings
import webapi

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 8000

class TopHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text:plain; charset=utf-8')
        self.end_headers()
        parsed_path = urlparse(self.path)
        parsed_query = parse_qs(parsed_path.query)

        print(parsed_path)

        router = webapi.router()
        result = router.handle('GET', parsed_path.path, **parsed_query)
        self.wfile.write(result.encode())

    def do_POST(self):
        content_len  = int(self.headers.get("content-length"))
        req_body = self.rfile.read(content_len).decode("utf-8")
        mailpartsloader = app.MailPartsLoaderFactory.create(app.LoadType.CSV_LINE, **dict(
            mailfrom_idx = 0,
            mailto_idx = 1,
            subject_idx = 2,
            contents_idx = 3,
        ))
        csv_lines = req_body.splitlines(keepends=True)
        mailserver = mailsettings.SettingsToMailServer.load('./settings.json')
        mailpartslist = mailpartsloader.load(csv_lines).group_by_address_and_subject()
        for mailparts in mailpartslist:
            mailserver.send(mailparts)
            

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = (SERVER_ADDRESS, SERVER_PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run(handler_class=TopHandler)