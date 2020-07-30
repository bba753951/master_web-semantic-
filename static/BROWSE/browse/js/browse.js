$("#nav_browse").addClass("active")

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

function infoGet(userID){
    var infodata_url="/master_project/master_media/uploadfile/"+userID+"/info_para.txt";
	$.ajax({
		url: infodata_url ,//url
		success: function (result) {
            $("#input_parameter").html(result)
        },
		error : function() {
            Swal.fire({
                  icon: 'error',
                  title: 'Oops...',
                  text: 'please check your ID is correrct or not (input parameter error)',
                
            })
		}
    })
}

function summaryGet(userID,way){
    var infodata_url="/master_project/master_media/uploadfile/"+userID+"/"+way+"/output_summary.html";
	$.ajax({
		url: infodata_url ,//url
		success: function (result) {
            $("#output_summary").html(result)
        },
		error : function() {
            Swal.fire({
                  icon: 'error',
                  title: 'Oops...',
                  text: 'please check your ID is correrct or not (output_summary error)',
                
            })
		}
    })
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

function addClickTip(name,info_table){

    $(name).qtip({
        content: {
            text:info_table,
            button:"close me"
        },
        show: {
            event: 'click',
            effect: function(offset) {
                $(this).slideDown(100); // "this" refers to the tooltip
            }},
        hide: {
            //target: $('#'+id_name+i,'*:not("[type=button]")'),
            target: $(name),
            event: 'click'
        },
		position: {
			//target: $('#show_site'),
            my:'bottom left',
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


    var data_url;
    var mtype;

    var files_data = new FormData();

    $("input[type='text']").each(function(){
        files_data.append($(this).attr("id"),$(this).val());
    });
    //$("select").each(function(){
        //files_data.append($(this).attr("id"),$(this).val());
    //})
    if ($(".ui.dropdown .text").text() === "Small RNA name"){
        files_data.append("browse","regulator");
        mtype="regulator"

    }else{
        files_data.append("browse","transcript");
        mtype="transcript"
    }
    //mtype=$("#browse").val();

    if ($("#folder_id").val()===""){
            Swal.fire({
                  icon: 'error',
                  title: 'Oops...',
                  html: 'You need to input a <span class="stress_red"> job ID </span>which can get from our result mail. <br><br> Or <span class="stress_red"> type \"example\" as job ID</span> to see example result.',
                
            })
        throw "empty job ID";

    }
    var show_a="show interactors"
    if (mtype === "transcript"){
        show_a="show interaction"
        
    }


    $('.ui.dimmer').dimmer('show');
	$.ajax({
		type: "POST",//方法类型
		//dataType: "json",//预期服务器返回的数据类型
		url: upload_url ,//url
		data: files_data,
        cache:false,
        processData:false,
        contentType:false,
		success: function (result) {
            if (result.jobState === "1"){
                $('.ui.dimmer').dimmer('hide');
                $("#all_para,#browse_result").css("display","none");
                //$("#input_para,#browse_result,#output_para").css("display","none");
                Swal.fire({
                      icon: 'error',
                      title: 'Oops...',
                      text: 'Your job state is queued, please wait for a while.',
                    
                })

            }else if(result.jobState === "2"){
                $('.ui.dimmer').dimmer('hide');
                $("#all_para,#browse_result").css("display","none");
                //$("#input_para,#browse_result,#output_para").css("display","none");
                Swal.fire({
                      icon: 'error',
                      title: 'Oops...',
                      text: 'Your job state is running, please wait for a while.',
                    
                })

            }else if(result.jobState === "0"){
                $('.ui.dimmer').dimmer('hide');
                $("#all_para,#browse_result").css("display","none");
                //$("#input_para,#browse_result,#output_para").css("display","none");
                Swal.fire({
                      icon: 'error',
                      title: 'Oops...',
                      text: 'Your job state do not start, please contact us for problem.',
                    
                })

            }else if(result.jobState === "3"){
                //$("#input_para,#browse_result,#output_para").css("display","block");
                $("#all_para,#browse_result").css("display","block");
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
                                    value = show_a
                                else
                                    value = '<a target="_blank" href="'+site_link+"?name="+data[col]+"&mtype="+mtype+"&userID="+result.userID +"&way="+way+"&count="+data[col+1]+'">'+show_a+'</a>';
                                return value
                            }
                        }
                    ],
                    "order": [[ col+1, 'desc'  ]],
                    "initComplete": function() {
                        $('.ui.dimmer').dimmer('hide');
                        //$("#downloadList").attr("href",downloadList_url+"?id="+result.userID+"&way="+way);
                        $("#load_result").addClass("active")
                        $("#load_result_bottom").addClass("active")
                        $.ajax({
                            type: "GET",
                            url: downloadList_url+"?id="+result.userID+"&way="+way,
                            success: function (result) {
                                $("#load_result").removeClass("active")
                                $("#load_result_bottom").removeClass("active")
                            }
                        })
                        
                        $("#downloadList").attr("href","/master_project/master_media/uploadfile/"+result.userID+"/"+way+"/download.zip");
                        $("#downloadList_b").attr("href","/master_project/master_media/uploadfile/"+result.userID+"/"+way+"/download.zip");
                        $(".option").css("display","block");
                        //infoHover(result.userID);
                        infoGet(result.userID)
                        summaryGet(result.userID,way)
                    }
                });
            }
        },
		error : function() {
            $('.ui.dimmer').dimmer('hide');
            //$("#input_para,#browse_result,#output_para").css("display","none");
            $("#all_para,#browse_result").css("display","none");
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
//var d_rm="<span class='info'>Use \"RNAfold\" (from ViennaRNA package) to calculate \"minimum free energy\" (mfe) of CLASH reads.<br><br>This o 
//ption selects the \"RNAfold_MFE\" column (less equal).<br><br>You can use None to not select</span>";
//var d_rs="<span class='info'>Use \"RNAup\" (from ViennaRNA package) to calculate the \"thermodynamics\" of regulatory RNA and target RNA ,and find the binding site.<br><br>This option selects the \"RNAup_score\" column (less equal).<br><br>You can use None to not select</span>";
var d_rc="<span class='info'>More reads could be indicative of more biologically relevant targeting events</span>";
var d_rs="<span class='info'>The \"thermodynamics\" of small RNA and target RNA. <br> <span class='stress_red'>The lower the score, the more likely to be a true pair.</span><br> Recommand from -5 to -10. </span>";
var d_ji="<span class='info'>To recognize your analysis result</span>";
addClickTip("#m_rc",d_rc)
addClickTip("#m_rs",d_rs)

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

//popFocus("#folder_id",d_ji,"focus")
//popFocus("#readCount",d_rc,"focus")
//popFocus("#RNAup_score",d_rs,"focus")


