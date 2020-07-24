//Ajaxで非同期通信してるから遅いかも
var canvas = $('#videocanvas')[0];

    $('#myvideo').on('loadedmetadata', function(){
        // canvasのサイズ合わせ
        var video = $('#myvideo')[0];
        var width = canvas.width = video.videoWidth;
        var height = canvas.height = video.videoHeight;

        // 描画先の指定
        var ctx = canvas.getContext("2d");

        // 送信データの作成
        var fd = new FormData();
        fd.append('video', null);

        //毎フレーム処理
        setInterval(function(){
            ctx.drawImage(video, 0, 0, width, height);
            canvas.toBlob(function(blob){

                fd.set('video', blob);

                $.ajax({
                    url: "/img",
                    type : "POST",
                    processData: false,
                    contentType: false,
                    data : fd,
                    dataType: "text",
                })
                .done(function(data){
                    console.log(data);
                })
                .fail(function(data){
                    console.log(data);
                });
            }, 'image/jpeg');
        },1000);
    });