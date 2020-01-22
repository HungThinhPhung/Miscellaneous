$("#suggestedItem").hide();
$("#suggestedItem2").hide();
clicked = false;
//clickedItemID = '';
//clickedItemWeight = 0;
//clickedItem = '';
//clickedValue ='';
$(document).ready(function(){
    $('#inputCompanyName').bind("enterKey",function(e){
       $("#suggestedItem").hide();
       $.ajax({
            type: 'GET',
            url: '/split?text=' + $("#inputCompanyName").val(),
            success: function(data){
                data = JSON.parse(data);
                $('#country').val(data.country)
                $('#province').val(data.province)
                $('#district').val(data.district)
                $('#ward').val(data.commune)
            }
       });
    });
    $('#inputCompanyName').keyup(function(e){
        if(e.keyCode == 13)
        {
            $(this).trigger("enterKey");
        }
    });
    $('#inputCompanyName').on('input',function(e){
        if($("#inputCompanyName").val().length >2 ){
            $("#suggestedItem").show()
            $.ajax({
                    type: 'GET',
                    url: '/myapi?text=' + $("#inputCompanyName").val(),
                    success: function(data){
                        data = JSON.parse(data);
                        console.log(data);
                        $("#suggestedItem").html("");
                        number = 0;
                        $.each(data, function(index) {
                            item = data[index]._source;
                            output = '<tr class="table-item p-15 col-md-9 m-b-5 m-l-10 m-r-10" id="row'+number+'" fullTyping="'+ item.FullTyping +'" ><td><a class="item-name" fullTyping="' +  item.FullTyping +'">'+ item.FullAddress +'</a></td></tr>';
                            number++;
                            $("#suggestedItem").append(output);
                        });
                        initSelectItem();
                    }
            });
        }
        else{
            $("#suggestedItem").hide();
            $('#index-edit').attr('disabled', 'disabled');
        }
    });

    function initSelectItem(){
        var currentItem = $("#inputCompanyName").val();
        $( ".table-item" ).hover(function() {

            $( ".table-item" ).removeClass("selected");
            $( this ).addClass("selected") ;
        }, function(){

            $(this).removeClass('selected');
            $("#inputCompanyName").val(currentItem);
        });
        $( ".table-item" ).click(function() {
            $("#suggestedItem").hide();
            $('#index-edit').removeAttr('disabled');
            clickedValue = $("#inputCompanyName").val();
            currentItem = $(".selected .item-name").attr('fullTyping');
            clickedItem = currentItem;
            clickedFullText = $(".selected .item-name").text();
            valueArr = clickedFullText.split(',').reverse()
            clickedItemID = $(this).attr("item-id");
            clickedItemWeight = parseInt($(".selected .weight").text()) +1;
            var idArr = ['#country', '#province', '#district', '#ward']

            for(i=0;i<valueArr.length;i++){
                $(idArr[i]).val(valueArr[i])
            }
            $('#location-detail').val(clickedFullText)
            clicked = true;
    //        debugger;
    //        updateWeight($(this).attr("item-id"),currentItem,parseInt($(".selected .weight").text()));



            $( ".table-item" ).hide();
        });
    }


    $('#inputCompanyName2').on('input',function(e){
        if($("#inputCompanyName2").val().length >2 ){
            $("#suggestedItem2").show()

            $.ajax({
                    type: 'GET',
                    url: '/imap?text=' + $("#inputCompanyName2").val(),
                    success: function(data){
                    var proArr = ['name', 'housenumber', 'street', 'city', 'state', 'country']
                    data = JSON.parse(data);
                    console.log(data);
                       $("#suggestedItem2").html("");
                            number = 0;
                        $.each(data, function(index) {
                            item = data[index];
                            properties = item.properties;
                            fullName = ''
                            if(properties.hasOwnProperty('name')){
                                fullName = properties.name + ', '
                            }
                            if(properties.hasOwnProperty('housenumber')){
                                fullName += properties.housenumber + ' '
                            }
                            if(properties.hasOwnProperty('street')){
                                fullName += properties.street + ', '
                            }
                            if(properties.hasOwnProperty('city')){
                                fullName += properties.city + ', '
                            }
                            if(properties.hasOwnProperty('state')){
                                fullName += properties.state + ', '
                            }
                            if(properties.hasOwnProperty('country')){
                                fullName += properties.country
                            }

                            output = '<tr class="table-item2 p-15 col-md-9 m-b-5 m-l-10 m-r-10" id="row'+number+'" fullTyping="" ><td><a class="item-name2" fullTyping="">'+ fullName +'</a></td></tr>';
                            number++;
                            $("#suggestedItem2").append(output);
                        });
                        initSelectItem2();
                    }
            });
        }
        else{
            $("#suggestedItem2").hide();
            $('#index-edit2').attr('disabled', 'disabled');
        }
    });

    function initSelectItem2(){
        var currentItem = $("#inputCompanyName2").val();
        $( ".table-item2" ).hover(function() {
            $( ".table-item2" ).removeClass("selected");
            $( this ).addClass("selected") ;
        }, function(){

            $(this).removeClass('selected');
            $("#inputCompanyName2").val(currentItem);
        });
        $( ".table-item2" ).click(function() {
            $("#suggestedItem2").hide();
            $('#index-edit2').removeAttr('disabled');
            clickedValue = $("#inputCompanyName2").val();
            currentItem = $(".selected .item-name2").attr('fullTyping');
            clickedItem = currentItem;
            clickedFullText = $(".selected .item-name2").text();
            valueArr2 = clickedFullText.split(',').reverse();
            clickedItemID = $(this).attr("item-id");
            clickedItemWeight = parseInt($(".selected .weight").text()) +1;
            var idArr2 = ['#country2', '#province2', '#district2', '#ward2'];
            for(i=0;i<valueArr2.length;i++){
                $(idArr2[i]).val(valueArr2[i]);
            }
            $('#location-detail2').val(clickedFullText)
            clicked = true;
    //        debugger;
    //        updateWeight($(this).attr("item-id"),currentItem,parseInt($(".selected .weight").text()));



            $( ".table-item2" ).hide();
        });
    }
});