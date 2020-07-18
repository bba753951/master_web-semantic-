
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

function uploadfile() {
    $("#pbar").css("display","flex");
    console.log("click");
    var file1=$("input[name='zip_file']").get(0).files[0];
    var files_data = new FormData();
    files_data.append("zip_file",file1);

    $("input[type='text']").each(function(){
        console.log($(this).attr("id"))
        files_data.append($(this).attr("id"),$(this).val());
    });

    $("select").each(function(){
        files_data.append($(this).attr("id"),$(this).val());
    })



	$.ajax({
		type: "POST",
		url: usage_url ,
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
var d_uf="<span class='info'>Please prepare the following files as a \"compressed file\" (.zip) <br><br>And use \"<span class='stress'>same file name</span>\" as following:<br><br><ol><li> <span class='stress'>read.fastq(Required)</span>:<br>FASTQ format,for CLASH read</li><li><span class='stress'>regulator.fasta(Required)</span>:<br>FASTA format,for regulaotry RNA</li><li> <span class='stress'>targetRNA.fasta(Required)</span>: <br>FASTA format ,for target RNA (transcript)</li><li><span class='stress'>gene_file.csv(Optional)</span>:<br>Must have \"transcript_name\" and \"Gene_name\" column name</li></ol></span>";
var d_em="<span class='info'>We use this mail to inform you how to start the analysis and see the result</span>";
addHoverTip("#d_uf",d_uf);
addHoverTip("#d_em",d_em);

// preprocess hint

var d_as="<span class='info'> Remove adapter sequence from CLASH reads.<br><br> Such as:<br>Illumina: AGATCGGAAGAGC<br>Small RNA: TGGAATTCTCGG<br>Nextera: CTGTCTCTTATA</span>";
var d_hl_g="<span class='info'>After trimming adapter,select the CLASH length (greater than) <br><br>You can\'t use 0 !!!</span>";
var d_hl_l="<span class='info'>After trimming adapter,select the CLASH length (less than) <br><br>You can\'t use 0 !!!</span>";
var d_ps="<span class='info'>Trim low-quality ends from reads in addition to adapter removal</span>";
var d_tt="<span class='info'>Select which program to trim adapter </span>";

addHoverTip("#d_as",d_as);
addHoverTip("#d_hl_g",d_hl_g);
addHoverTip("#d_hl_l",d_hl_l);
addHoverTip("#d_ps",d_ps);
addHoverTip("#d_tt",d_tt);

// quality
var d_rc="<span class='info'>Select \"read count\" of CLASH read (greater equal)</span>";
var d_rm="<span class='info'>Use \"RNAfold\" (from ViennaRNA package) to calculate \"minimum free energy\" (mfe) of CLASH reads.<br><br>This option selects the \"RNAfold_MFE\" column (less equal).<br><br>You can use None to not select</span>";

addHoverTip("#d_rc",d_rc);
addHoverTip("#d_rm",d_rm);
// Find Pairs
// -------- pir ----------
var d_atrm_p="<span class='info'>Use \"bowtie\" to align regulatory to CLASH reads.<br><br> You can choose the mismatch count between 0 to 2</span>";
var d_attm_p="<span class='info'>Use \"bowtie\" to align remaining sequence to target RNA.<br><br>You can choose the mismatch count between 0 to 2</span>";
var d_rsl_p="<span class='info'>Select sequence length of remaining sequence which gets from CLASH read (greater than)</span>";
var d_hph_p="<span class='info'>Max hits per CLASH read (not including different of position)</span>";
// -------- hyb ----------
var d_hst_h="<span class='info'>Fragment selection threshold </span>";
var d_obf_h="<span class='info'>Max gap/overlap between fragments </span>";
var d_hph_h="<span class='info'>Max hits per read (including different of position)</span>";
// -------- clan ----------
var d_fl_c="<span class='info'>Minimum length for each fragment </span>";
var d_obf_c="<span class='info'>Maximum overlap allowed between fragments </span>";
var d_hpf_c="<span class='info'>Number of maximum hits for each maximal fragment</span>";

addHoverTip("#d_atrm_p",d_atrm_p);
addHoverTip("#d_attm_p",d_attm_p);
addHoverTip("#d_rsl_p",d_rsl_p);
addHoverTip("#d_hph_p",d_hph_p);
addHoverTip("#d_hst_h",d_hst_h);
addHoverTip("#d_obf_h",d_obf_h);
addHoverTip("#d_hph_h",d_hph_h);
addHoverTip("#d_fl_c",d_fl_c);
addHoverTip("#d_obf_c",d_obf_c);
addHoverTip("#d_hpf_c",d_hpf_c);
// analyse
var d_rs="<span class='info'>Use \"RNAup\" (from ViennaRNA package) to calculate the \"thermodynamics\" of regulatory RNA and target RNA ,then find the binding site.<br><br>This option selects the \"RNAup_score\" column (less equal).<br><br>You can use None to not select</span>";

addHoverTip("#d_rs",d_rs);




//---------------create SVG
//var width = $('.right-opt').width()-40;
//var height = $('.right-opt').height();
//var rectY=30;
//var down_arrow=20;
//var down_arrow_len=down_arrow-5;
//var rectY_all=rectY*9+8*down_arrow
//var svg = d3.select("#flowchart")
  //.append("svg")
  //.attr("width", width)
  //.attr("height", rectY_all)
  //.attr("style","background:#EBECF0;")
  

////---------------create scale
//var xScale = d3.scale.linear()
  //.domain([0,1000])
  //.range([0,width]);

//if(rectY_all >height){
    //$('#flowchart').css("overflow","auto")
    //$('#flowchart').height(height)
//}

//pos_array=[[0,0,1,"Clash Raw Data"],[1,1,1,"Process Hybrid(1)"],[2,2,1,"Process Hybrid(2)"],[3,3,1,"Find Regulator"],[4,4,1,"Find Target"],[5,5,1,"Predit Target Position"],[6,6,1,"Organize Result"],[7,7,1,"Add Gene Info"],[8,8,1,"Web Browse"],[9,3,0,"Regulator File"],[10,4,0,"Transcript File"],[11,7,0,"Gene File(Optional)"]]
////---------------plot rect
//var rectSite = svg.selectAll("rect")
  //.data(pos_array)
  //.enter()
  //.append("rect")
  //.attr("id",function(d,i){
    //return "flow"+d[0]
  //})
  //.attr("fill", "red")
  //.attr("y", function(d){
      //return d[1]*rectY+d[1]*down_arrow;
  //})
  //.attr("x", function(d){
      //return d[2]*xScale(550)
    //})
  //.attr("width", xScale(450))
  //.attr("height", rectY)


//var defs = svg.append('svg:defs')
//var marker=defs.append('svg:marker')
    //.append('svg:marker')
      //.attr('id', "arrow")
      //.attr('markerHeight', 10)
      //.attr('markerWidth', 10)
      //.attr('markerUnits', 'strokeWidth')
      //.attr('orient', 'auto')
      //.attr('refX', "6")
      //.attr('refY', "6")
      //.attr('viewBox', "0 0 12 12")
      //.append('svg:path')
        //.attr('d', "M2,2 L10,6 L2,10 L6,6 L2,2")
        //.attr('fill', "black");
//////------------plot arrow 
//arrow_array=[[1,0],[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[1,7],[0,3],[0,4],[0,7]];
//var line = svg.selectAll("line")
            //.data(arrow_array)
            //.enter()
            //.append("line")
             //.attr("x1",function(d){
                //var value=xScale(780);
                //if(d[0] === 0){
                   //value=xScale(450);
                //}
                //return value
            //})  
             //.attr("y1",function(d){
                //var value=d[1]*(rectY+down_arrow)+rectY;
                //if(d[0] === 0){
                   //value=d[1]*(rectY+down_arrow)+rectY/2;
                //}
                //return value
            //})   
             //.attr("x2",function(d){
                //var value=xScale(780);
                //if(d[0] === 0){
                   //value=xScale(545);
                //}
                //return value
            //})    
             //.attr("y2",function(d){
                //var value=d[1]*(rectY+down_arrow)+rectY+down_arrow_len;
                //if(d[0] === 0){
                   //value=d[1]*(rectY+down_arrow)+rectY/2;
                //}
                //return value
            //})  
             //.attr("stroke","black")  
             //.attr("stroke-width",2)  
             //.attr("marker-end","url(#arrow)")

////------------ add text
//var rectSite = svg.selectAll("text")
  //.data(pos_array)
  //.enter()
  //.append("text")
  //.attr("id",function(d,i){
    //return "text"+d[0]
  //})
  //.attr("fill", "white")
  //.attr("y", function(d){
      //return d[1]*rectY+d[1]*down_arrow+rectY*2/3;
  //})
  //.attr("x", function(d){
      //return d[2]*xScale(550)+xScale(40);
    //})
  //.style('font-size', xScale(40)+'px')
  //.style('font-weight', 'bold')
  //.text(function(d){
      //return d[3]
  //})
    
//function flowHover(object,target){
    //$(object).hover(
        //function() {
            //$(target).addClass("flow_hover");
        //}, function() {
            //$(target).removeClass("flow_hover");
        //}
    //);
//}

//flowHover("#flow0","#d_uf");
//flowHover("#flow1","#d_as");
//flowHover("#flow1","#d_hl");
//flowHover("#flow2","#d_rc");
//flowHover("#flow2","#d_rm");
//flowHover("#flow3","#d_rhm");
//flowHover("#flow3","#d_rsl");
//flowHover("#flow4","#d_rtm");
//flowHover("#flow5","#d_rs");
//flowHover("#flow5","#d_gts");
//flowHover("#flow9","#d_uf");
//flowHover("#flow10","#d_uf");
//flowHover("#flow11","#d_uf");


//flowHover("#text0","#d_uf");
//flowHover("#text1","#d_as");
//flowHover("#text1","#d_hl");
//flowHover("#text2","#d_rc");
//flowHover("#text2","#d_rm");
//flowHover("#text3","#d_rhm");
//flowHover("#text3","#d_rsl");
//flowHover("#text4","#d_rtm");
//flowHover("#text5","#d_rs");
//flowHover("#text5","#d_gts");
//flowHover("#text9","#d_uf");
//flowHover("#text10","#d_uf");
//flowHover("#text11","#d_uf");



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
    if (/^\s*$/.test(filename)){
      $(this).prev('span').text(text)
    }else{
      $(this).prev('span').text(filename.replace("C:\\fakepath\\", ""));
    }

  })
  
}
changefile("zip_file","no file");
