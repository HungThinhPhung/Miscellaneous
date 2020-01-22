var serverUrl = window.location.origin + '/' + window.location.pathname.split('/')[0];

var locationUrl = 'https://testrdapi.misa.com.vn/location/';
var locationUrl = 'http://localhost:2000/location/';
var suggestData;
$("#suggested-item").hide();
$(document).ready(function () {
    $('#create').click(function() {
        send('insert')
    });

    $('#update').click(function() {
        send('update')
    });
    $('#input-location').on('input', function(e){
        inputText = $('#input-location').val();
        if(inputText.length > 2){
            suggest(inputText)
        }
    });
    $('body').click(function() {
        $('#suggested-item').hide();
    });
});

function packForm() {
    var fields = $('#in-out input');
    var result = {'id': $('#id').val()};
    for(var j = 0; j < fields.length; j++){
        result[rename(fields[j].id)] = fields[j].value;
    };
    return result;
};

function unpackForm(data){
    $('#id').val(data._id);
    var fields = $('#in-out input');
    for(var k = 0; k < fields.length; k++){
        fields[k].value = data._source[rename(fields[k].id)]
    };
}

function rename(name) {
    
    name = name.split('-');
    var result = '';
    for (var i = 0; i < name.length; i++) {
        var text = name[i];
        if (text == 'zip' || text == 'id') {
            text = text.toUpperCase();
        }
        else {
            text = text[0].toUpperCase() + text.slice(1);
        }
        result += text;
    }
    return result;
};

function send(mode){
    data = packForm();
    $.ajax({
        type: 'POST',
        url : locationUrl + mode,
        contentType: 'application/json; charset=utf-8',
        crossDomain: true,
        dataType: 'json',
        data: JSON.stringify(data),
        success: function ( data ) {
            console.log(data);
        }
    });
};

function suggest(text){
    $('#suggested-item').show()
    $.ajax({
        type: 'GET',
        url: locationUrl + 'suggestion?text=' + text,
        success: function(data){
            if(data.length == 0){
                $('#suggested-item').html('<i>Không tìm thấy địa chỉ <b>' + $('#input-location').val() + '<\i>')
                return null;
            }
            suggestData = data
            $("#suggested-item").html("");
            number = 0;
            $.each(data, function(index) {
                item = data[index]._source;
                output = '<tr class="table-item p-15 col-md-9 m-b-5 m-l-10 m-r-10" row-id="row'+number+'" fullTyping="'+ item.FullTyping +'" ><td><a class="item-name" fullTyping="' +  item.FullTyping +'" id="' +number+'">'+ item.FullAddress +'</a></td></tr>';
                number++;
                $("#suggested-item").append(output);
            });
            initSelectItem();
        }
});
}

function initSelectItem(){
    var currentItem = $("#input-location").val();
    $( ".table-item" ).hover(function() {

        $( ".table-item" ).removeClass("selected");
        $( this ).addClass("selected") ;
    }, function(){

        $(this).removeClass('selected');
        $("#input-location").val(currentItem);
    });
    $( ".table-item" ).click(function() {
        $("#suggested-item").hide();
        $('#index-edit').removeAttr('disabled');
        
        var clickedID = parseInt($(".selected .item-name").attr('id'));
        var clickedItem = suggestData[clickedID]
        unpackForm(clickedItem)
        
        $( ".table-item" ).hide();
    });
}