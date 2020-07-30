$("#nav_upload").addClass("active")

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
            my:'top right',
            at:'bottom center'
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
function checkFile(id){
    console.log($(id).attr("id"))
    if ($("#"+id).prev('label').children("span").text() === "No file"){
        Swal.fire({
              icon: 'error',
              title: 'Oops...',
              text: 'Upload file can\'t be empty',
            
        });
        throw $(name).attr("id")+" file empty";
    }

}
function checkSelectFile(name){
    if ($(name).val() === ""){
        Swal.fire({
              icon: 'error',
              title: 'Oops...',
              text: 'Small/Target RNA file can\'t be empty',
            
        });
        throw "Small/Target RNA file is empty";
    }

}

function uploadfile() {
    console.log("click");
	var upload_state=0;
    var userid="";
    //var file1=$("input[name='zip_file']").get(0).files[0];
    var files_data = new FormData();
    //files_data.append("zip_file",file1);
    if ($("#adaptor").val() === "" && $("#trimmed_tool").val() != "trim_galore" ){
        Swal.fire({
              icon: 'error',
              title: 'Oops...',
              text: 'If you don\'t input the adapter sequence,you only can choose "trim_galore"',
            
        });
        throw "wrong adapter";

    }
    if ($("#mail").val() != ""){
        if (! /\s*@\s*/.test($("#mail").val())){
            Swal.fire({
                  icon: 'error',
                  title: 'Oops...',
                  text: 'Wrong E-mail address',
                
            });
            throw "wrong mail";

        }
    }

    if ($("input[name='upload_check']").prop("checked")){
        if ($("#use_old_id").val() === ""){
            Swal.fire({
                  icon: 'error',
                  title: 'Oops...',
                  text: 'Job ID can not empty',
                
            });
            throw "empty job id";

        }

    }else{
        $("#zip_read").each(function(){
            checkFile($(this).attr("id"));
            var file1=$(this).get(0).files[0];
            files_data.append($(this).attr("id"),file1);
        });

        $("#zip_regulator").each(function(){
            checkSelectFile("input[name=reg_select]")
            if ($("input[name=reg_select]").val() === "0"){
                checkFile($(this).attr("id"));
                var file1=$(this).get(0).files[0];
                files_data.append($(this).attr("id"),file1);
            }
        });

        $("#zip_target").each(function(){
            checkSelectFile("input[name=target_select]")
            if ($("input[name=target_select]").val() === "0"){
                checkFile($(this).attr("id"));
                var file1=$(this).get(0).files[0];
                files_data.append($(this).attr("id"),file1);
            }
        });
    }


    $("input[type='text']").each(function(){
        console.log($(this).attr("id"))
        files_data.append($(this).attr("id"),$(this).val());
    });
    $("input[type='hidden']").each(function(){
        console.log($(this).attr("id"))
        files_data.append($(this).attr("name"),$(this).val());
    });

    $("select").each(function(){
        files_data.append($(this).attr("id"),$(this).val());
    })
	
	if ($("#prep_check input").prop("checked"))
        files_data.append("prep_check","0");
	else
        files_data.append("prep_check","1");


    $(".mybar .label").text("Upload file ...");
    $(".ui.progress").css("display","block");

	$.ajax({
		type: "POST",
		url: analyse_url ,
		data: files_data,
        cache:false,
        processData:false,
        contentType:false,
		success: function (result) {
            console.log("ok");
			upload_state=1;	
            userid=result.userID;
            console.log("try to start: "+userid);
            if (userid != ""){

                $.ajax({
                    type: "GET",
                    url: confirm_url+"?id="+userid ,
                    success: function (result) {
                        console.log("ok");
                    },
                    error : function() {
                        Swal.fire({
                              icon: 'error',
                              title: 'Oops...',
                              text: 'Analysis can not start',
                            
                        })
                    },
                });
                if ($("#mail").val() != ""){
                    Swal.fire({
                          icon: 'success',
                          title: 'Job ID: <span class="stress_red">'+userid+ '</span>',
                          html: 'It may take a few hours to a day before the analyses are completed.<br><br> We use <span class="stress_red">E-mail </span>to inform you when your results are ready.',
                    }).then((result) => {
                      if (result.value) {
                        $(".mybar").css("display","none");
                      }
                    })
                }else{
                    Swal.fire({
                          icon: 'success',
                          title: 'Job ID: <span class="stress_red">'+userid+ '</span>',
                          html: 'It may take a few hours to a day before the analyses are completed.<br><br> Please use the following <a href="/master_project/browse?id='+userid+'" target="_blank"><i class="linkify icon"></i>link</a> or job ID (<span class="stress_red">'+userid+ '</span>) to check the status of your analyses.',
                    }).then((result) => {
                      if (result.value) {
                        $(".mybar").css("display","none");
                      }
                    })

                }
            }

		},
		error : function() {
            Swal.fire({
                  icon: 'error',
                  title: 'Oops...',
                  text: 'Something went wrong!',
                
            })
			upload_state=0;	
		},
		
		xhr: function(){
	        // get the native XmlHttpRequest object
	        var xhr = $.ajaxSettings.xhr() ;

	        // set the onprogress event handler
	        xhr.upload.onprogress = function(evt){ 
	            var width =  evt.loaded/evt.total*100;
	            $(".mybar .bar").css("width",width+"%");
	            $(".mybar .progress").text(Math.floor(width) + '%');
	            console.log('progress', width) 

	        } ;
	        // set the onload event handler
	        xhr.upload.onload = function(){ 
	            console.log('DONE!') 

	            $(".mybar .label").text("Success");
	        } ;

	        return xhr ;
	    }
	});
}

var btn = document.getElementById("search");  
btn.addEventListener('click',uploadfile);


//upload file hint
var m_crf="<span class='info'>Please upload a compressed file <span class='stress'>(.zip)</span> of CLASH sequencing data in <span class='stress'>FASTQ</span> format here.</span>";
var m_rrf="<span class='info'>Please upload a compressed file <span class='stress'>(.zip)</span> of small RNA in <span class='stress'>FASTA </span>format here.</span>";
var m_trf="<span class='info'>Please upload a compressed file <span class='stress'>(.zip)</span> of target RNA in <span class='stress'>FASTA</span> format here.</span>";

addClickTip("#m_crf",m_crf);
addClickTip("#m_rrf",m_rrf);
addClickTip("#m_trf",m_trf);

// preprocess hint
var m_tt="<span class='info'>Select a program to trim 3\' adapter </span>";
var m_as="<span class='info'> 3 \' adapter sequence to be trimmed. <br><br> If not specified explicitly, Trim Galore will try to auto-detect whether the Illumina universal, Nextera transposase or Illumina small RNA adapter sequence was used. <br><br> Such as:<br>Illumina: AGATCGGAAGAGC<br>Small RNA: TGGAATTCTCGG<br>Nextera: CTGTCTCTTATA</span>";
var m_bs="<span class='info'> Trimming of 5' adapter sequences.<br><br> Depending on the experimental design, 5' linkers may contain a variable-length barcode for sample multiplexing and a random nucleotide prefix for monitoring of PCR amplification artefacts. </span>";
var m_crl_g="<span class='info'>After trimming adapter,select the read length <span class='stress'>(greater than)</span> <br>You can\'t use 0 !!!</span>";
var m_crl_l="<span class='info'>After trimming adapter,select the read length <span class='stress'>(less than)</span> <br>You can\'t use 0 !!!</span>";
var m_ps="<span class='info'>Trim low-quality ends from reads in addition to adapter removal. A higher Q score will require higher quality reads. <br><br>Q score over 30 is a common requirement</span>";

addClickTip("#m_tt",m_tt);
addClickTip("#m_as",m_as);
addClickTip("#m_bs",m_bs);
addClickTip("#m_crl_g",m_crl_g);
addClickTip("#m_crl_l",m_crl_l);
addClickTip("#m_ps",m_ps);

// Find Pairs
var m_a="<span class='info'> Select a algorithm to identify chimeras <br> <a href='https://europepmc.org/article/ppr/ppr21284' class='stress' target='_blank'><i class='linkify icon'></i>CLAN<a> <br><a href='https://pubmed.ncbi.nlm.nih.gov/24211736/' class='stress' target='_blank'><i class='linkify icon'></i>Hyb<a> <br> <a href='https://pubmed.ncbi.nlm.nih.gov/30357353/' class='stress' target='_blank'><i class='linkify icon'></i>piRTarBase<a></span>"
addClickTip("#m_a",m_a);
// -------- pir ----------
var m_mar_p="<span class='info'>Use \"bowtie1\" to align small RNA to CLASH reads.<br><br> You can choose the mismatch count between 0 to 2</span>";
var m_mat_p="<span class='info'>Use \"bowtie1\" to align remaining sequence to target RNA.<br><br>You can choose the mismatch count between 0 to 2</span>";
var m_rsl_p="<span class='info'>Select sequence length of remaining sequence which gets from CLASH read (greater than)</span>";
var m_hpr_p="<span class='info'>Number of target hits per chimera read allowed </span>";
addClickTip("#m_mar_p",m_mar_p);
addClickTip("#m_mat_p",m_mat_p);
addClickTip("#m_rsl_p",m_rsl_p);
addClickTip("#m_hpr_p",m_hpr_p);

// -------- hyb ----------
var m_hst_h="<span class='info'>Select mapping score of framents (same as blast e-value).</span>";
var m_obf_h="<span class='info'>When identifying RNA-RNA pair,maximum gap/overlap allowed between two fragments </span>";
var m_hpr_h="<span class='info'>Number of target hits per chimera read allowed </span>";
addClickTip("#m_hst_h",m_hst_h);
addClickTip("#m_obf_h",m_obf_h);
addClickTip("#m_hpr_h",m_hpr_h);

// -------- clan ----------
var m_fl_c="<span class='info'>Minimum length for each RNA species identified within a read </span>";
var m_obf_c="<span class='info'>When identifying RNA-RNA pair,maximum overlap allowed between two fragments </span>";
var m_hpf_c="<span class='info'>Number of unique RNA species allowed to be identified in the same read</span>";
addClickTip("#m_fl_c",m_fl_c);
addClickTip("#m_obf_c",m_obf_c);
addClickTip("#m_hpf_c",m_hpf_c);


// mail
var m_em="<span class='info'>E-mail address will only be used to notify the user when the results are ready and to provide a link to those results.</span>";
addClickTip("#m_em",m_em);

// job ID
var m_ji="<span class='info'>Allow users to reanalyze the same uploaded data with different setting.</span>";
addClickTip("#m_ji",m_ji);



//===============upload file =================
function changefile(name,text){
  
  $("#"+name).bind('change', function () {
    var filename = $(this).val();
    console.log(filename);
    if (/\s*\.zip$/.test(filename)){
      $(this).prev('label').children("span").text(filename.replace("C:\\fakepath\\", ""));
    }else if (filename === ""){
      $(this).prev('label').children("span").text(text)
    }else{
      $(this).prev('label').children("span").text(text)
        Swal.fire({
              icon: 'error',
              title: 'Oops...',
              text: 'File must be zip format',
            
        })
    }

  })
  
}
changefile("zip_read","No file");
changefile("zip_regulator","No file");
changefile("zip_target","No file");

//===============find pair way =================
var current_way=$('#findway').val()
$('#findway').bind('change', function(){
    $('.find_'+current_way).css('display','none')
    current_way=$(this).val()
    $('.find_'+current_way).css('display','block')
})

//===============adapter option =================
$('#trimmed_tool').bind('change', function(){
    var tool=$(this).val()
    if(tool==="trim_galore"){
        $('#adaptor').next("div").addClass("hidde")
        $(".optional_").css("display","inline")
    }else{
        $('#adaptor').next("div").removeClass("hidde")
        $(".optional_").css("display","none")
    }
})
//=============== select data option =================
$('.ui.dropdown').each(function(){
  $(this).dropdown({

    onChange: function(value, text, $selectedItem) {

      if (value === "0"){
        $(this).next("label").removeClass("hidde")
      }else{
        $(this).next("label").addClass("hidde")
      }

    }
  });
})   

//
//=============== preprocess checkbox  =================
$('#prep_check').checkbox({
  onUnchecked: function() {
   $(".prep .field").each(function(){$(this).removeClass("disabled")})
  },
  onChecked: function() {
    $(".prep .field").each(function(){$(this).addClass("disabled")})
  }
})

//=============== file checkbox  =================
$('#file_check').checkbox({
  onUnchecked: function() {
    $("#use_old").addClass("hidde");
    $("#self_upload").removeClass("hidde")
  },
  onChecked: function() {

    $("#use_old").removeClass("hidde");
    $("#self_upload").addClass("hidde")
  }
});


