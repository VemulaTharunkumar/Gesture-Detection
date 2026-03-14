from flask import Flask, render_template, Response, request, jsonify
from core.engine import GestureEngine

app = Flask(__name__)
engine = GestureEngine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(engine.generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start', methods=['POST'])
def start():
    engine.start()
    return jsonify(ok=True, status="started")

@app.route('/stop', methods=['POST'])
def stop():
    engine.stop()
    return jsonify(ok=True, status="stopped")

@app.route('/exit', methods=['POST'])
def exit_app():
    engine.stop()
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()
    return jsonify(ok=True, status="exiting")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True, threaded=True)
