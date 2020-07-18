column1=[
        {"title":"Target RNA Name"},
        {"title":"# of CLASH Evidences"},
        {"title":"Target Details"}
    ];

column2=[
        {"title":"Target Gene Name"},
        {"title":"Target RNA Name"},
        {"title":"# of CLASH Evidences"},
        {"title":"Target Details"}
    ];

column=[column1,column2]

$('#example').DataTable({
    "data": tdata,
    "destroy":true,
    "columns":column[gene_exist],
    "aoColumnDefs":[
        {
            "aTargets":[-1],
            "mData": function ( source, type, val  ) {return source},
            "mRender" : function(data,type,full){
                var value;
                if(data[gene_exist+1]+""==="0")
                    value = "show details"
                else
                    value = '<a target="_blank" href="'+site_link+"?name="+data[gene_exist]+"&regulator="+regulator_name+"&userID="+userID+"&way="+way+"&count="+data[gene_exist+1]+'&mtype=transcript&sfile=ori_reg">show details</a>';
                return value
            }
        }
    ],
    "order": [[ gene_exist+1, 'desc'  ]]

});
