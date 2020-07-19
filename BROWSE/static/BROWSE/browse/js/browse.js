// ----------- input parameter -------------
function infoHover(userID){
    var infodata_url="/master_project/master_media/uploadfile/"+userID+"/info_para.txt";
    $("#input_para").qtip({
        content: {
            text: function(event, api) {
                $.ajax({ url: infodata_url })
                    .done(function(html) {
                        api.set('content.text', html)
                    })
                    .fail(function(xhr, status, error) {
                        api.set('content.text', status + ': ' + error)
                    })

                return 'Loading...';
            }
        },
        show: {
            effect: function(offset) {
                $(this).slideDown(50); 
            }},
        hide: {
            fixed:true,
            },
        position: {
            //target: $('#show_site'),
            my:'top right',
            at:'bottom center'
        },
        style: {
              classes: 'qtip-dark'
              //classes: 'qtip-dark qtip-jtools'
        }
    })  
    $("input_para").hover(function(){
        $(this).css("opacity",0.2)
    },function(){
        $(this).css("opacity",1)
    });

}

function addHoverTip(name,info_table){

    $(name).qtip({
        content: {
            text:info_table,
        },
        show: {
            effect: function(offset) {
                $(this).slideDown(100); 
            }},
        hide: {
            fixed:true,
            },
		position: {
			//target: $('#show_site'),
            my:'bottom right',
            at:'top center'
		},
        style: {
              classes: 'qtip-dark'
              //classes: 'qtip-dark qtip-jtools'
        }
    })  
    $(name).hover(function(){
        $(this).css("opacity",0.2)
    },function(){
        $(this).css("opacity",1)
    });
}


function uploadfile() {

    $('.ui.dimmer').dimmer('show');
    $("#input_para,#browse_result").css("display","block");

    var data_url;
    var mtyep;

    var files_data = new FormData();

    $("input[type='text']").each(function(){
        files_data.append($(this).attr("id"),$(this).val());
    });
    //$("select").each(function(){
        //files_data.append($(this).attr("id"),$(this).val());
    //})
    if ($(".ui.dropdown .text").text() === "Regulatory RNA Name"){
        files_data.append("browse","regulator");
        mtype="regulator"

    }else{
        files_data.append("browse","transcript");
        mtype="transcript"
    }
    //mtype=$("#browse").val();



	$.ajax({
		type: "POST",//方法类型
		//dataType: "json",//预期服务器返回的数据类型
		url: upload_url ,//url
		data: files_data,
        cache:false,
        processData:false,
        contentType:false,
		success: function (result) {
            //var way=$("#way").val();
            var way=result.way;
			console.log(result);
            var col = 0;
            if(result.data.length > 3){col=1};

            if (mtype==="regulator"){
                data_url="/master_project/master_media/uploadfile/"+result.userID+"/"+way+"/step6_regulator_transcript.json";
            }else{
                data_url="/master_project/master_media/uploadfile/"+result.userID+"/"+way+"/step6_transcript_regulator.json";
            };

            //$('#example').dataTable().fnClearTable(); // clear dataTable !!!!
            $('#example').dataTable().fnDestroy(); // destroy dataTable !!!!
            $('#example').html("");
            
            $('#example').DataTable({
                "ajax": data_url,
                "destroy":true,
                "columns":result.data,
                "aoColumnDefs":[
                    {
                        "aTargets":[-1],
                        "mData": function ( source, type, val  ) {return source},
                        "mRender" : function(data,type,full){
                            var value;
                            if(data[col+1]==="0")
                                value = "show details"
                            else
                                value = '<a target="_blank" href="'+site_link+"?name="+data[col]+"&mtype="+mtype+"&userID="+result.userID +"&way="+way+"&count="+data[col+1]+'">show details</a>';
                            return value
                        }
                    }
                ],
                "order": [[ col+1, 'desc'  ]],
                "initComplete": function() {
                    $('.ui.dimmer').dimmer('hide');
                    $("#downloadList a").attr("href",downloadList_url+"?id="+result.userID+"&way="+way);
                    $(".option").css("display","block");
                    //infoHover(result.userID);
                }
            });
                    },
		error : function() {
            $('.ui.dimmer').dimmer('hide');
            Swal.fire({
                  icon: 'error',
                  title: 'Oops...',
                  text: 'please check your ID is correrct or not',
                
            })
                //.then((result) => {
                //if (result.value){
                    //$('#example').dataTable().fnDestroy(); // destroy dataTable !!!!
                    //$('#example').html("");
                //}
            //})
		}
	});

}



var btn = document.getElementById("search");  
btn.addEventListener('click',uploadfile);



// folder_id is from Django
if(folder_id != ""){
    $('#folder_id').val(folder_id);
}
if(RNAup_score != ""){
    $('#RNAup_score').val(RNAup_score);
}
if(RNAfold_MFE != ""){
    $('#RNAfold_MFE').val(RNAfold_MFE);
}
if(readCount != ""){
    $('#readCount').val(readCount);
}



// add Hover Info
var d_rc="<span class='info'><span class='stress_red'>The more the better</span></span>";
//var d_rm="<span class='info'>Use \"RNAfold\" (from ViennaRNA package) to calculate \"minimum free energy\" (mfe) of CLASH reads.<br><br>This o 
//ption selects the \"RNAfold_MFE\" column (less equal).<br><br>You can use None to not select</span>";
//var d_rs="<span class='info'>Use \"RNAup\" (from ViennaRNA package) to calculate the \"thermodynamics\" of regulatory RNA and target RNA ,and find the binding site.<br><br>This option selects the \"RNAup_score\" column (less equal).<br><br>You can use None to not select</span>";
var d_rs="<span class='info'>The \"thermodynamics\" of regulatory RNA and target RNA. <br> <span class='stress_red'>The less the better.</span><br> Recommand from -5 to -10. </span>";

var d_ji="<span class='info'>To recognize your analysis result</span>";

//addHoverTip("#d_rs",d_rs);
//addHoverTip("#d_rm",d_rm);
//addHoverTip("#d_rc",d_rc);


// semanticUI dropdown
$('.ui.dropdown').dropdown();

// filter parameter popup
function popFocus(name,content,action){
    $(name).attr("data-html",content)
    $(name)
        .popup({
                on: action
              
        })
    ;
}

popFocus("#folder_id",d_ji,"focus")
popFocus("#readCount",d_rc,"focus")
popFocus("#RNAup_score",d_rs,"focus")
