const localVideo = document.getElementById('video')
startVideo();

function startVideo() {
    navigator.mediaDevices.getUserMedia({video: true, audio: false})
    .then(function (stream) {
        localVideo.srcObject = stream;
    }).catch(function (error) {
        console.error('mediaDevice.getUserMedia() error: ', error);
        return;
    });
}