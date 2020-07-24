$(function() {
  //h1要素を変数に代入する
  var h1 = $('h1');

  //h1要素の中の文字を一文字ずつ分割して配列(txt_array)に入れる
  var txt_array = h1.text().split('');

  //h1要素の中身を空にする
  $('h1').html('');

  //配列に入っている文字数分だけ処理を繰り返す
  $.each(txt_array, function(index, element) {

    //<span style="opacity: 0">配列に入っている1文字</span>という要素を作成する
    var new_element = $("").text(element).css({ opacity: 0 });

    //作成した要素をh1要素の末尾に追加していく。
    h1.append(new_element);

    //indexの数値 * ミリ秒だけ処理を遅延させる。
    //indexの数値は後方の文字にいくほど大きくなるので
    //それにミリ秒を乗じる事で後ろの文字ほど処理が遅延し文字が遅れて現れる
    new_element.delay(index * 100);

    //animateを使って3000ミリ秒（3秒）の時間をかけて
    //opacityを1（不透明）にしてジワッと文字を出現させる
    new_element.animate({opacity: 1}, 3000);

  });
});