from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask("VideoAPI")
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument("title", required=True)

videos = {
    'video1': {
        'title': 'Hello world in python flask',
    },
    'video2': {
        'title': 'Introduction to JavaScript'
    }
}


class Video(Resource):
    def get(self, video_id):
        if video_id == "all":
            return videos
        return videos[video_id]

    def put(self, video_id):
        args = parser.parse_args()
        new_video = {"title": args["title"]}
        videos[video_id] = new_video
        return videos, 200

    def delete(self, video_id): 
        if video_id not in videos : 
            return f"Video {video_id} not found", 200
        else:
            del videos[video_id]
            return videos, 200

api.add_resource(Video, "/<video_id>")

if __name__ == "__main__":
    app.run(debug=True)
