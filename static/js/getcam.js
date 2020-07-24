//カメラ画像の取得
$(function(){
  const constraints = window.constraints = {
    audio: false,
    video: {
      facingMode: "environment"
      // facingMode:デフォルトで使用されるカメラの指定、"environment"でフロントカメラ、"user"でインカメラ
    }
  };

  async function init() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      const video = document.querySelector('#myvideo');
      const videoTracks = stream.getVideoTracks();
      window.stream = stream; 
      video.srcObject = stream;
      e.target.disabled = true;
    } catch{
      $('#errorMsg').text('カメラの使用を許可してください');
    }
  }

  $('#start').click(init);
});