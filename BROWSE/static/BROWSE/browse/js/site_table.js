// ---------------- function -------------------
//function addtable(array_info,i){
function addtable(array_info,i){
    i = parseInt(i);

    var info = '<div><table class="qtable"><tr>'
    for(j = 0;j < array_info[0].length;j++){
        info += '<th>'+array_info[0][j]+'</th>'
    }

    info += '</tr><tr>'
    for(j = 0;j < array_info[0].length;j++){
        info += '<td>'+array_info[i+1][j]+'</td>'
    }
    info += '</tr></table></div>'
    return info   
}
function addClickTip(array_info,id_name,i,my_pos,at_pos){
	var info = addtable(array_info,i);

    $("#"+id_name+i).qtip({
        content: {
            text:info},
            //button: "close me",},
        show: {
            event: 'click',
            effect: function(offset) {
                $(this).slideDown(100); // "this" refers to the tooltip
                var id_text = $("#"+id_name+i).text();
                $("#"+id_name+i).text("close");
                $("#"+id_name+i).addClass(id_text);
            }},
		position: {
            my:my_pos,
            at:at_pos
		},
        hide: {
            //target: $('#'+id_name+i,'*:not("[type=button]")'),
            target: $('#'+id_name+i),
            effect: function(offset) {
                var id_text = $("#"+id_name+i).attr("class").split(" ")[1]
                $("#"+id_name+i).text(id_text);
                $("#"+id_name+i).removeClass(id_text);
            },
            event: 'click'},
        style: {
                    classes: 'qtip-dark'
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
			target: $('#show_site'),
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

//------------------ D3 --------------------------------
//---------------D3 varable
function drawSite(){

var seq_len = transcript_len;
//var pos_array = [[1,10,30,2],[2,5,15,1],[0,160,180,1],[4,175,185,2],[3,205,250,1]];
//var info = [["title1","title2"],["0","b"],["1","d"],["2","c"],["3","f"],["4","g"]]
//
var padding = 20; 
var rectY = 25;
var width = $('#show_site').width()-2*padding;// svg

var height = (max_level+4)*rectY // svg

var axisYpos = height - 2*rectY;
var rect_seqY = axisYpos - rectY;


if(height>400){
    $('#show_site').css("overflow","auto")
    $('#show_site').height(400)
    $('#show_site').animate({ scrollTop: height  }, 1000);
}


//---------------create SVG
var svg = d3.select("#show_site")
  .append("svg")
  .attr("width", width)
  .attr("height", height)
  .attr("style","background:#ecf0f3;")
  //.attr("viewbox","0,0,"+10000+","+10000)
  //.attr("preserveAspectRatio","xMidYMax slice");
  

//---------------create scale
var xScale = d3.scale.linear()
  .domain([0,seq_len+1])
  .range([0,width-2*padding]);


//---------------create axis
var axis = d3.svg.axis()
  .scale(xScale)
  .orient("bottom");
  
var gAxis = svg.append("g")
.attr("transform","translate("+padding+","+axisYpos+")")
  .classed("axis",true)
  .call(axis);


//---------------plot site rect
var rectSite = svg.selectAll("rect")
  .data(pos_array)
  .enter()
  .append("rect")
  .attr("id",function(d){
    return "site"+d[0]
  })
  .attr("fill", "red")
  .attr("x", function(d,i){
      return padding + xScale(d[1]);
  })
  .attr("y", function(d){
    return rect_seqY - d[3]*rectY
  })
  .attr("width", function(d){
    return  xScale(d[2]-d[1]);
  })
  .attr("height", rectY*0.8)

for(i=0;i<pos_array.length;i++){
  var info_table = addtable(pos_info,i);
  addHoverTip("#site"+i,info_table);
}


//---------------plot transcript rect
var rectSeq = svg.append("rect")
  .attr("fill", "blue")
  .attr("x", padding+xScale(1))
  .attr("y", rect_seqY)
  .attr("width" , xScale(seq_len))
  .attr("height", rectY*0.8)
  .attr("id","transcript_rect")
  

var tran_table = addtable(transcript_info,0);
addHoverTip("#transcript_rect",tran_table);


}

drawSite();
$(window).resize(function(){
    var svg = d3.select("#show_site");
    svg.selectAll("*").remove();
    drawSite();
});
//------------------DataTable --------------------------------
$('#example').DataTable({
    "data": tdata,
    "destroy":true,
    "columns":tcolumn,
    //"autoWidth": true,
    "aoColumnDefs":[
        {
            "aTargets":[1],
            "mData": function ( source, type, val  ) {return source},
            "mRender" : function(data,type,full){
                value = '<button type="button" class="hyb_btn" id="hybrid'+data[0]+'">'+data[1]+'</button>';
                //value = '<button type="button" class="hyb_btn" id="'+data[0]+'">'+data[1]+'</button>';
                return value
            }
        },
        { "bVisible": false, "aTargets": [0]},
    ]
});

// bcuz hybrid_info have column_name at index 0
//function renderTip(){

    //for(i = 0;i < tcol_num;i++){
        //addClickTip(hybrid_info,"hybrid",i,'top left','bottom right')
    //}
//}
//renderTip();
//$('#example').on('draw.dt',renderTip);

function renderTip(){
    $(".hyb_btn").each(function(){
        var id = $(this).attr("id").slice(6);
        console.log(id);
        addClickTip(hybrid_info,"hybrid",id,'top left','bottom right');
    })
}
renderTip();
$('#example').on('draw.dt',renderTip);

