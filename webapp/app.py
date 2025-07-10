from flask import Flask, render_template, request, abort
import os

app = Flask(__name__)

# Directory that contains generated playlists
PLAYLIST_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'iptv', 'output')


def parse_m3u(path):
    channels = []
    name = None
    with open(path, 'r', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#EXTINF'):
                parts = line.split(',', 1)
                if len(parts) > 1:
                    name = parts[1].strip()
            elif line.startswith('#'):
                continue
            else:
                url = line
                channels.append({'name': name or url, 'url': url})
                name = None
    return channels


@app.route('/')
def index():
    if not os.path.isdir(PLAYLIST_DIR):
        playlists = []
    else:
        playlists = [f for f in os.listdir(PLAYLIST_DIR) if f.endswith('.m3u') or f.endswith('.m3u8')]
    return render_template('index.html', playlists=playlists)


@app.route('/playlist/<path:filename>')
def playlist(filename):
    path = os.path.join(PLAYLIST_DIR, filename)
    if not os.path.isfile(path):
        abort(404)
    channels = parse_m3u(path)
    return render_template('playlist.html', playlist=filename, channels=channels)


@app.route('/play')
def play():
    url = request.args.get('url')
    if not url:
        abort(404)
    return render_template('player.html', url=url)


if __name__ == '__main__':
    app.run(debug=True)
