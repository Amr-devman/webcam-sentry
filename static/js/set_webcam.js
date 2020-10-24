
Webcam.set({
// live preview size
width: 640,
height: 640,

// device capture size
dest_width: 640,
dest_height: 640,

// final cropped size
crop_width: 640,
crop_height: 640,

// format and quality
image_format: 'jpeg',
jpeg_quality: 90,

// flip horizontal (mirror mode)
flip_horiz: true
});
Webcam.attach( '#my_camera' );
