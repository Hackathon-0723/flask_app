
jQuery(document).ready(function($){
    init();
    startVideo();

    $(".start_btn").on("click", function() {
        $('.start').animate({ height: 'hide' }, 'slow');   // 左に非表示
        $('.timer').animate({ height: 'show' }, 'slow');   // 右に表示
        count = 20;  //60のカウントダウン
        $('.sec').text(count);
        countDown = setInterval(function(){ //1秒おきにカウントマイナス
            count--;
            /*
            if(count <= 10){
                var selected_eff = $('puff').val();
                $('.timer').hide(selected_eff, get_options(selected_eff), 200);
	            $('.timer').show(selected_eff, get_options(selected_eff), 500);
            }else */
            if(count <= 0){//0になったら停止する
                clearInterval(countDown);
            }
            $('.sec').text(count);
        },1000);
    });
});



/*
var startBtn = document.getElementById('start-btn');

var multiBtn = document.getElementById('multi-btn');

var startPage = document.getElementById('start');

var multiPage = document.getElementById('multi-page');

var contentSec = document.getElementById('sec');
*/



const localVideo = document.getElementById('video');

function startVideo() {
    navigator.mediaDevices.getUserMedia({video: true, audio: false})
    .then(function (stream) {
        localVideo.srcObject = stream;
    }).catch(function (error) {
        console.error('mediaDevice.getUserMedia() error: ', error);
        return;
    });
}



/*
var count = 60;  // 制限時間60秒
var interval = 1000;

function countdown() {
    contentSec.innerHTML = count;
    count--;
}

startBtn.addEventListener('click', () => {
    startPage.classList.add('no-display');
    timerID = setInterval("countdown()", 1000);
});
*/


function init() {
    /*
    $(".biography-details").hide();
    $(".skill-details").hide();
    $(".publications-details").hide();
    $(".hobbies-details").hide();
    */
   $(".timer").hide();
}