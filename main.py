from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
import json


app = Flask("VideoAPI")
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument("title", required=True)
parser.add_argument("uploadDate", type=int, required=True)

videos = {
    'video1': {
        'title': 'Hello world in python flask',
        'uploadDate': 20210917
    },
    'video2': {
        'title': 'Introduction to JavaScript',
        'uploadDate': 20210918
    }
}

with open('videos.json', 'r') as f:
    videos = json.load(f)


def write_changes_to_file():
    global videos
    videos = {k: v for k, v in sorted(
        videos.items(), key=lambda video: video[1]['uploadDate'])}
    with open("videos.json", 'w') as f:
        json.dump(videos, f)


class Video(Resource):
    def get(self, video_id):
        if video_id == "all":
            return videos
        # elif video_id not in videos and video_id != "all":
        #     abort(404, message=f"Video {video_id} not found!")
        return videos[video_id]

    def put(self, video_id):
        args = parser.parse_args()
        new_video = {"title": args["title"]}
        videos[video_id] = new_video
        write_changes_to_file()
        return videos, 200

    def delete(self, video_id):
        if video_id not in videos:
            abort(400, message=f"Video {video_id} not found!")
        else:
            del videos[video_id]
            write_changes_to_file()
            return videos, 200


class VideoSchedule(Resource):
    def get(self):
        return videos

    def post(self):
        args = parser.parse_args()
        new_video = {"title": args["title"]}
        video_id = max(int(v.lstrip("video")) for v in videos.keys()) + 1
        videos[video_id] = new_video
        write_changes_to_file()
        return videos, 201


api.add_resource(Video, "/<video_id>")
api.add_resource(VideoSchedule, "/videos")

if __name__ == "__main__":
    app.run(debug=True)
