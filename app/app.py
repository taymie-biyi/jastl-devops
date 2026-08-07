from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>JASTL DevOps Platform</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                text-align: center;
                padding: 50px;
            }

            .container {
                background: white;
                width: 700px;
                margin: auto;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(0,0,0,0.2);
            }

            h1 {
                color: #1565C0;
            }

            ul {
                text-align: left;
                display: inline-block;
            }

            li {
                margin: 10px 0;
                font-size: 18px;
            }
        </style>
    </head>

    <body>

        <div class="container">

            <h1>JASTL DevOps Platform</h1>

            <h3>Value Added Project</h3>

            <ul>
                <li>GitHub Repository</li>
                <li>Jenkins CI/CD</li>
                <li>Docker Containerization</li>
                <li>Kubernetes Cluster</li>
                <li>Ansible Automation</li>
                <li>Prometheus Monitoring</li>
                <li>Grafana Dashboard</li>
                <li>MSP Integration</li>
                <li>ClearRoots Integration</li>
            </ul>

        </div>

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
