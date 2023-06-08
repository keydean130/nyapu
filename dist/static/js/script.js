//マップ
window.addEventListener("load" , function(){
    map_load();
});


//マップのデータをGET文で手に入れる
function map_load(){

    let form_elem   = "#form_area";

    let url     = $(form_elem).prop("action");
    let method  = "GET";

    $.ajax({
        url: url,
        type: method,
        processData: false,
        contentType: false,
        dataType: 'json'
    }).done( function(data, status, xhr ) {
        console.log(data.map_diaries);
        map_draw(data.map_diaries);
    }).fail( function(xhr, status, error) {
        console.log(status + ":" + error );
    });
}

// 現在地を取得して、地図を描画する
function getgeo() {
  map.on('locationerror', onLocationError);
  map.locate({
    setView: "true"
  });
}

function onLocationError(e) {
  alert('位置情報を取得できませんでした。\n'+ e.message);
}
