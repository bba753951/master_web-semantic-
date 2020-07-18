
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
            my:'bottom center',
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
    console.log("click");
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
    if (! /\s*@\s*/.test($("#mail").val())){
        Swal.fire({
              icon: 'error',
              title: 'Oops...',
              text: 'Wrong E-mail address',
            
        });
        throw "wrong mail";

    }


    $("input[type='file']").each(function(){
        console.log($(this).attr("name"))
        if ($(this).prev("span").text() === "no file"){
            Swal.fire({
                  icon: 'error',
                  title: 'Oops...',
                  text: 'Upload file can\'t be empty',
                
            });
            throw $(this).attr("name")+" file empty";

        }

        var file1=$(this).get(0).files[0];
        files_data.append($(this).attr("name"),file1);
    });


    $("input[type='text']").each(function(){
        console.log($(this).attr("id"))
        files_data.append($(this).attr("id"),$(this).val());
    });

    $("select").each(function(){
        files_data.append($(this).attr("id"),$(this).val());
    })


    $("#pbar").css("display","flex");

	$.ajax({
		type: "POST",
		url: analyse_url ,
		data: files_data,
        cache:false,
        processData:false,
        contentType:false,
		success: function (result) {
            console.log("ok");
                    },
		error : function() {
            Swal.fire({
                  icon: 'error',
                  title: 'Oops...',
                  text: 'Something went wrong!',
                
            })
		},
		xhr: function(){
        // get the native XmlHttpRequest object
        var xhr = $.ajaxSettings.xhr() ;
        // set the onprogress event handler
        $('#p').attr('max', 100);
        $('#p').attr('value', 0);

        xhr.upload.onprogress = function(evt){ 
            var width =  evt.loaded/evt.total*100;
            $("#myBar").css("width",width+"%");
            $("#Percentage").text(Math.floor(width) + '%');
            console.log('progress', width) 

        } ;
        // set the onload event handler
        xhr.upload.onload = function(){ 
            console.log('DONE!') 
            Swal.fire({
                  icon: 'success',
                  title: 'Check your E-amil',
                  html: 'You need to recive a mail from us and <span class="stress_red">click the link</span> to start analysis',
            })
        } ;

        //$("#pbar").css("display","none");
        // return the customized object
        return xhr ;
    }
	});
}

var btn = document.getElementById("search");  
btn.addEventListener('click',uploadfile);


//upload file hint
var m_crf="<span class='info'>A compressed file <span class='stress'>(.zip)</span> about CLASH Read in <span class='stress'>FASTQ</span> format.</span>";
var m_rrf="<span class='info'>A compressed file <span class='stress'>(.zip)</span> about regulatory RNA in <span class='stress'>FASTA </span>format.</span>";
var m_trf="<span class='info'>A compressed file <span class='stress'>(.zip)</span> about target RNA in <span class='stress'>FASTA</span> format.</span>";

addClickTip("#m_crf",m_crf);
addClickTip("#m_rrf",m_rrf);
addClickTip("#m_trf",m_trf);

// preprocess hint
var m_tt="<span class='info'>Select a program to trim 3\' adapter </span>";
var m_as="<span class='info'> Adapter sequence to be trimmed. <br><br> If not specified explicitly, Trim Galore will try to auto-detect whether the Illumina universal, Nextera transposase or Illumina small RNA adapter sequence was used. <br><br> Such as:<br>Illumina: AGATCGGAAGAGC<br>Small RNA: TGGAATTCTCGG<br>Nextera: CTGTCTCTTATA</span>";
var m_bs="<span class='info'> Trimming of 5' adapter sequences.<br><br> Depending on the experimental design, 5' linkers may contain a variable-length barcode for sample multiplexing and a random nucleotide prefix for monitoring of PCR amplification artefacts. </span>";
var m_crl_g="<span class='info'>After trimming adapter,select the CLASH length <span class='stress'>(greater than)</span> <br>You can\'t use 0 !!!</span>";
var m_crl_l="<span class='info'>After trimming adapter,select the CLASH length <span class='stress'>(less than)</span> <br>You can\'t use 0 !!!</span>";
var m_ps="<span class='info'>Trim low-quality ends from reads in addition to adapter removal</span>";

addClickTip("#m_tt",m_tt);
addClickTip("#m_as",m_as);
addClickTip("#m_bs",m_bs);
addClickTip("#m_crl_g",m_crl_g);
addClickTip("#m_crl_l",m_crl_l);
addClickTip("#m_ps",m_ps);

// quality
//var d_rc="<span class='info'>Select \"read count\" of CLASH read (greater equal)</span>";
//var d_rm="<span class='info'>Use \"RNAfold\" (from ViennaRNA package) to calculate \"minimum free energy\" (mfe) of CLASH reads.<br><br>This option selects the \"RNAfold_MFE\" column (less equal).<br><br>You can use None to not select</span>";

//addHoverTip("#d_rc",d_rc);
//addHoverTip("#d_rm",d_rm);
//
// Find Pairs
var m_a="<span class='info'> Select a algorithm to find RNA-RNA pair</span>"
addClickTip("#m_a",m_a);
// -------- pir ----------
var m_mar_p="<span class='info'>Use \"bowtie1\" to align regulatory RNA to CLASH reads.<br><br> You can choose the mismatch count between 0 to 2</span>";
var m_mat_p="<span class='info'>Use \"bowtie1\" to align remaining sequence to target RNA.<br><br>You can choose the mismatch count between 0 to 2</span>";
var m_rsl_p="<span class='info'>Select sequence length of remaining sequence which gets from CLASH read (greater than)</span>";
var m_hpr_p="<span class='info'>Max number of fragments mapping to reference on CLASH read.If same reference sequence has different position mapped,just count once</span>";
addClickTip("#m_mar_p",m_mar_p);
addClickTip("#m_mat_p",m_mat_p);
addClickTip("#m_rsl_p",m_rsl_p);
addClickTip("#m_hpr_p",m_hpr_p);

// -------- hyb ----------
var m_hst_h="<span class='info'>Select mapping score of framents (same as blast e-value).</span>";
var m_obf_h="<span class='info'>When identifying RNA-RNA pair,maximum gap/overlap allowed between fragments </span>";
var m_hpr_h="<span class='info'>Max number of fragments mapping to reference on CLASH read.If same reference sequence has different position mapped,repeatedly count</span>";
addClickTip("#m_hst_h",m_hst_h);
addClickTip("#m_obf_h",m_obf_h);
addClickTip("#m_hpr_h",m_hpr_h);

// -------- clan ----------
var m_fl_c="<span class='info'>Minimum length for each fragment </span>";
var m_obf_c="<span class='info'>When identifying RNA-RNA pair,maximum overlap allowed between fragments </span>";
var m_hpf_c="<span class='info'>Number of maximum hits for each maximal fragment</span>";
addClickTip("#m_fl_c",m_fl_c);
addClickTip("#m_obf_c",m_obf_c);
addClickTip("#m_hpf_c",m_hpf_c);

// analyse
//var d_rs="<span class='info'>Use \"RNAup\" (from ViennaRNA package) to calculate the \"thermodynamics\" of regulatory RNA and target RNA ,and find the binding site.<br><br>This option selects the \"RNAup_score\" column (less equal).<br><br>You can use None to not select</span>";

//addHoverTip("#d_rs",d_rs);

// mail
var m_em="<span class='info'>We use this mail address to inform you how to start the analysis and browse the result</span>";
addClickTip("#m_em",m_em);

//============= flow click ==============
var curr_index=0;
$(".lshow").eq(0).css("display","block");
$(".rshow").each(function(index){
    $(this).click(function(){
        $(".rshow").eq(curr_index).removeClass("rclick");
        $(".lshow").eq(curr_index).css("display","none");
        $(".lshow").eq(index).css("display","block");
        $(this).addClass("rclick");
        curr_index=index;
    })
})

$(".next_btn").click(function(){
        $(".rshow").eq(curr_index).removeClass("rclick");
        $(".lshow").eq(curr_index).css("display","none");
        curr_index++;
        $(".lshow").eq(curr_index).css("display","block");
        $(".rshow").eq(curr_index).addClass("rclick");
})



//===============upload file =================
function changefile(name,text){
  
  $('input[name='+name+']').bind('change', function () {
    var filename = $(this).val();
    console.log(filename);
    if (/\s*\.zip$/.test(filename)){
      $(this).prev('span').text(filename.replace("C:\\fakepath\\", ""));
    }else if (filename === ""){
      $(this).prev('span').text(text)
    }else{
      $(this).prev('span').text(text)
        Swal.fire({
              icon: 'error',
              title: 'Oops...',
              text: 'File must be zip format',
            
        })
    }

  })
  
}
changefile("zip_read","no file");
changefile("zip_regulator","no file");
changefile("zip_target","no file");

//===============find pair way =================
var current_way=$('#find_way').val()
$('#find_way').bind('change', function(){
    $('.find_'+current_way).css('display','none')
    current_way=$(this).val()
    $('.find_'+current_way).css('display','block')
})

//===============adapter option =================
$('#trimmed_tool').bind('change', function(){
    var tool=$(this).val()
    if(tool==="trim_galore"){
        $('#ada_opt').text("(optional)")
    }else{
        $('#ada_opt').text("(required)")
    }
})
