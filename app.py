# from flask import Flask, request, jsonify, render_template, send_file
# from ultralytics import YOLO
# import os
# import tempfile

# app = Flask(__name__)

# # Load the YOLO model
# model = YOLO("best.pt")


# @app.route('/')
# def home():
#     # Renders the index.html file from the templates folder
#     return render_template('index.html')


# @app.route('/track', methods=['POST'])
# def track_fire():
#     # First, print all files in the request to debug
#     print("Files in request:", request.files)
#     print("Form data:", request.form)
    
#     # Try different possible field names
#     if 'video' in request.files:
#         video_file = request.files['video']
#     elif 'video_file' in request.files:
#         video_file = request.files['video_file']
#     elif 'file' in request.files:
#         video_file = request.files['file']
#     else:
#         # If no file found, check if a default file path was provided instead
#         default_path = request.form.get('video_file')
#         if default_path and os.path.exists(default_path):
#             # Use the provided path
#             confidence = float(request.form.get('conf', 0.01))
#             iou_threshold = float(request.form.get('iou', 0.3))
            
#             try:
#                 results = model.track(source=default_path, save=True, conf=confidence, iou=iou_threshold)
#                 result_path = str(results[0].save_dir)
#                 result_file = os.path.join(result_path, os.path.basename(default_path))
                
#                 return send_file(result_file, as_attachment=True, 
#                                 download_name=f"processed_{os.path.basename(default_path)}", 
#                                 mimetype='video/mp4')
#             except Exception as e:
#                 print(f"Error processing default file: {e}")
#                 return jsonify({"status": "error", "message": str(e)}), 500
        
#         # No file found in the request
#         return jsonify({"status": "error", "message": "No video file provided. Files in request: " + str(list(request.files.keys()))}), 400
    
#     # Check if the file is empty
#     if video_file.filename == '':
#         return jsonify({"status": "error", "message": "Empty filename"}), 400

#     print(f"Processing file: {video_file.filename}")
    
#     confidence = float(request.form.get('conf', 0.01))
#     iou_threshold = float(request.form.get('iou', 0.3))

#     try:
#         # Create a temporary file to save the uploaded video
#         temp_dir = tempfile.mkdtemp()
#         temp_path = os.path.join(temp_dir, video_file.filename)
#         video_file.save(temp_path)
        
#         print(f"File saved to: {temp_path}")
        
#         # Process the video file from the saved path
#         results = model.track(source=temp_path, save=True, conf=confidence, iou=iou_threshold)
        
#         # Get the result file path
#         result_dir = results[0].save_dir
#         print(f"Result directory: {result_dir}")
        
#         # Look for the processed file
#         processed_files = [f for f in os.listdir(result_dir) if f.endswith(os.path.splitext(video_file.filename)[1])]
#         if processed_files:
#             result_file = os.path.join(result_dir, processed_files[0])
#             print(f"Sending file: {result_file}")
            
#             return send_file(result_file, as_attachment=True, 
#                             download_name=f"processed_{video_file.filename}", 
#                             mimetype='video/mp4')
#         else:
#             return jsonify({"status": "error", "message": f"Processed file not found in {result_dir}"}), 500
    
#     except Exception as e:
#         print(f"Error: {e}")
#         return jsonify({"status": "error", "message": str(e)}), 500


# if __name__ == '__main__':
#     app.run(debug=True)



# from flask import Flask, request, jsonify
# from ultralytics import YOLO
# import cv2

# app = Flask(__name__)

# # Load the YOLO model
# model = YOLO("best.pt")

# @app.route('/')
# def home():
#     return "Welcome to the Fire Detection API! Use the /track endpoint to run the model."

# @app.route('/track', methods=['POST'])  # Corrected: Route starts with a slash
# def track_fire():
#     video_file = request.form.get('video_file', 'input.mp4')
#     confidence = float(request.form.get('conf', 0.01))
#     iou_threshold = float(request.form.get('iou', 0.3))

#     try:
#         results = model.track(source=video_file, save=True, conf=confidence, iou=iou_threshold)
#         result_image_path = str(results[0].save_dir)
#         return jsonify({"status": "success", "result_image_path": result_image_path})
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)})
    
# def generate_frames():
#     cap = cv2.VideoCapture(0)  # Open webcam only when requested

#     while True:
#         success, frame = cap.read()
#         if not success:
#             break

#         # Perform inference
#         results = model(frame)
#         for result in results:
#             for box in result.boxes:
#                 x1, y1, x2, y2 = map(int, box.xyxy[0])
#                 confidence = float(box.conf[0])

#                 # Draw bounding box
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
#                 cv2.putText(frame, f"Fire {confidence:.2f}", (x1, y1 - 10),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

#         # Encode frame
#         _, buffer = cv2.imencode('.jpg', frame)
#         frame_bytes = buffer.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

#     cap.release()  # Release webcam when the loop ends

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, request, jsonify
from ultralytics import YOLO
import cv2
import os

app = Flask(__name__)

# Load the YOLO model
model = YOLO("best.pt")

@app.route('/track', methods=['POST'])
def track_fire():
    if 'video_file' not in request.files:
        return jsonify({"status": "error", "message": "No video file provided"}), 400
    
    video_file = request.files['video_file']
    if video_file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"}), 400

    # Save uploaded file temporarily
    video_path = os.path.join("uploads", video_file.filename)
    os.makedirs("uploads", exist_ok=True)  # Ensure the directory exists
    video_file.save(video_path)

    confidence = float(request.form.get('conf', 0.01))
    iou_threshold = float(request.form.get('iou', 0.3))

    try:
        results = model.track(source=video_path, save=True, conf=confidence, iou=iou_threshold)
        result_image_path = str(results[0].save_dir)
        return jsonify({"status": "success", "result_image_path": result_image_path})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
