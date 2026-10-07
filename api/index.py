from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Supermarket Product Analyzer</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 900px;
                    margin: 60px auto;
                    padding: 20px;
                }
                h1 {
                    margin-bottom: 10px;
                }
                .box {
                    padding: 20px;
                    border: 1px solid #ddd;
                    border-radius: 10px;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>Supermarket Product Analyzer</h1>
            <p>Data Warehousing and Data Mining Mini Project</p>

            <div class="box">
                <h2>Project Features</h2>
                <ul>
                    <li>Sales data analysis</li>
                    <li>Product and category analysis</li>
                    <li>Customer and date dimensions</li>
                    <li>Association rule mining</li>
                    <li>Revenue analysis</li>
                    <li>Top product analysis</li>
                </ul>
            </div>

            <div class="box">
                <h2>Deployment Status</h2>
                <p>Project successfully deployed on Vercel.</p>
            </div>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))