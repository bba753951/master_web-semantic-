from django.shortcuts import render

from django.shortcuts import render_to_response
from django.http import HttpResponse,JsonResponse,FileResponse
from django.views.decorators.csrf import csrf_exempt

import subprocess
import pandas as pd
import random,string
import os

server="cosbi7"
media_path = '/home/bba753951/Django/master_project/media/uploadfile/'
script_folder = '/home/bba753951/Django/master_project/BROWSE/script/'
info_path = '/home/bba753951/Django/master_project/media/info/'
reference_path="/home/bba753951/Django/master_project/media/reference/"
pipeline_env="/home/bba753951/suite/env_path.sh"

def downloadList(request):        
    folder_id=request.GET.get("id","")
    way=request.GET.get("way","")
    id_path=media_path+folder_id+"/"+way+"/"
    
    # output which column 
    original_info=["hybrid0","hybrid_seq","hybrid_len","reg_hyb_target_pos","remain_pos","read_count","RNAfold_MFE","regulator_name","regulator_seq","regulator_len","on_reg_pos","transcript_name","transcript_len","rem_tran_target_pos","RNAup_pos","RNAup_score","RNAup_target_seq","RNAup_input_seq"]

    # change new name
    new_original_info=["CLASH Read ID","CLASH Read","CLASH Read Length","Region on CLASH Read identified as Small RNA","Region on CLASH Read identified as Target RNA","Read Count","RNAfold MFE","Small RNA Name","Small RNA Sequence","Small RNA Length","Small RNA Region Found in CLASH Read","Target RNA Name","Target RNA Length","Target RNA Region Found in CLASH Read","Predicted Target Site","RNAup Score","5\' to 3\' Paired Sequence in Target RNA","5\' to 3\' Paired Sequence in Small RNA"]

    data=pd.read_csv(id_path+"step6.csv",usecols=original_info)
    data=data[original_info]
    data.columns=new_original_info
    data.to_csv(id_path+"result_by_RNA_RNA_interaction.csv",index=0)

    # change column name and output name of three file
    command="sed -e '1c CLASH Read,# Identified Interactions,Identified Interactions' {0}step6_hybrid_transcript.csv > {0}result_by_CLASH_read.csv".format(id_path)
    subprocess.call(command, shell=True)
    command="sed -e '1c Small RNA Name,# Identified Targets,Identified Targets' {0}step6_regulator_transcript.csv > {0}result_by_small_RNA_name.csv".format(id_path)
    subprocess.call(command, shell=True)
    command="sed -e '1c Target RNA Name,# Small RNA Interactors,Small RNA Interactors' {0}step6_transcript_regulator.csv > {0}result_by_target_RNA_name.csv".format(id_path)
    subprocess.call(command, shell=True)

    # zip all file
    command="zip -j {0}download.zip {0}result*.csv".format(id_path)
    subprocess.call(command, shell=True)
    print(id_path+"download.zip")
    # response = FileResponse(open(id_path+"download.zip","rb"))
    # response["Content-Type"]="application/octet-stream"
    # response["Content-Disposition"]="attachment;filename=download.zip"
    # return response
    return JsonResponse({"state":"ok"})





def browse(request):        
    folder_id=request.GET.get("id","")
    RNAup_score=request.GET.get("up","")
    RNAfold_MFE=request.GET.get("fold","")
    readCount=request.GET.get("readCount","")
    return render_to_response('browse.html',locals())

def savefile(file1,name,id_path):
    file_path = id_path+name

    with open(file_path,'wb') as f:
        for temp in file1.chunks():
            f.write(temp)

def getDefault(value,default):
    if not value:
        print("can not get value {} ,use defalut {}".format(value,default))
        return default
    return value


@csrf_exempt
def uploadfile(request):
# for browse

    print("upload---------------\n\n\n")
    if request.method == 'POST':

        RNAfold_MFE = getDefault(request.POST.get("RNAfold_MFE","None"),"None")
        RNAup_score = getDefault(request.POST.get("RNAup_score","None"),"None")
        readCount = getDefault(request.POST.get("readCount","None"),"None")
        # way = getDefault(request.POST.get("way","pir"),"pir")
        mtype = getDefault(request.POST.get("browse","regulator"),"regulator")
        folder_id = request.POST.get("folder_id").strip()
        id_path=media_path+folder_id+"/"
        task_id=folder_id

        if not os.path.isdir(id_path):
            raise ValueError

        if os.path.isfile(id_path+"findway.csv"):
            with open(id_path+"findway.csv","r") as f:
                way = f.read().strip()
        else:
            print("no findway")
            way="clan"

        print("way:",way)

        print("------------------------")
        command="bash {4}step6.sh -i {0}{1}/hyb_file_step5.csv -o {0}{1}/step6.csv -t {0}transcript.csv -r {0}regulator.csv -u {2} -f {3} -c {5}".format(id_path,way,RNAup_score,RNAfold_MFE,script_folder,readCount)
        print(command)
        subprocess.call(command, shell=True)
        subprocess.call("bash {}merge_step6_gene.sh {} {}".format(script_folder,id_path,way), shell=True)
    
        data=pd.read_csv(info_path+"info.csv",header=None,index_col=0)
        jobState=str(data.loc[folder_id,2])




        column_name=[]
        if mtype=="regulator":
            column_name=[{"title":"Small RNA Name"},
                         {"title":"# Identified  Targets"},
                         {"title":"Target RNA Details"}]
        else:

            if os.path.isfile(id_path+"gene_file.csv"):
                print("gene_file exist")
                column_name=[{"title":"Target Gene Name"},
                             {"title":"Target RNA Name"},
                             {"title":"# of Small RNAs"},
                             {"title":"Target Details"}]
            else:
                print("gene_file not exist")
                column_name=[{"title":"Target RNA Name"},
                             {"title":"# Chimera Reads"},
                             {"title":"Target Details"}]

        # calculate output summary
        command = "bash {}calculate_output_summary.sh {} {}".format(script_folder,id_path,way)
        subprocess.call(command, shell=True)

        with open("{}{}/output_summary.csv".format(id_path,way),"r")as f:
            summary = f.read().split(",")

        # infoDiv='<div class="ui left labeled button btn_margin_top mini" tabindex="0">\
                  # <a class="ui right pointing label">\
                    # {}\
                  # </a>\
                  # <div class="ui basic button">\
                    # {}\
                  # </div>\
                # </div>'

        infoDiv="<tr>\
                <td class='positive'>{}</td>\
                <td>{}</td>\
                </tr>"

        infoTxt=infoDiv.format("# reads provided",summary[0])
        infoTxt=infoTxt + infoDiv.format("# reads trimmed",summary[1])
        infoTxt=infoTxt + infoDiv.format("# unique reads trimmed",summary[2])
        infoTxt=infoTxt + infoDiv.format("# reads with identified chimera",summary[3])
        infoTxt=infoTxt + infoDiv.format("# identified RNA-RNA pairs",summary[4])

        with open("{}{}/output_summary.html".format(id_path,way),"w")as f:
            f.write(infoTxt)

        return JsonResponse({"data":column_name,"userID":task_id,"way":way,"jobState":jobState})


def showSeq(seq1,seq2):
    seq1=seq1.replace("T","U")
    seq2=seq2.replace("T","U")

    seq2=seq2[::-1]

    count=0   #pos
    gu_pos=[]
    ngu_pos=[]
    bulge_pos=[]
    seq1_bulge_pos=[]
    for j in zip(seq1,seq2):
        i=set(j)
        if i == {'G','U'} or i == {'G','T'}:
            gu_pos.append(count)
        elif i == {'A','T'} or i == {'C' ,'G'} or i == {'A','U'}:
            pass
        elif "-" in i:
            if j[0] == "-":
                bulge_pos.append(count)
            else:
                seq1_bulge_pos.append(count)
        else:
            ngu_pos.append(count)

        count += 1


    result_seq2=""
    result_seq1=""
    for i in range(len(seq2)):
        if i in gu_pos:
            result_seq2+='<span class="gu">'+seq2[i]+'</span>'
        elif i in ngu_pos:
            result_seq2+='<span class="ngu">'+seq2[i]+'</span>'
        elif i in bulge_pos:
            result_seq2+='<span class="bulge">'+seq2[i]+'</span>'
        else:
            result_seq2+=seq2[i]

    for i in range(len(seq1)):
        if i in seq1_bulge_pos:
            result_seq1+='<span class="bulge">'+seq1[i]+'</span>'
        else:
            result_seq1+=seq1[i]

    result="5'"+result_seq1+"3'<br>3'"+result_seq2+"5'"
    return result
def h_inof_add_color(h_info):
    pos=h_info[2].split("-")
    pos=list(map(int,pos))
    seq=h_info[0]
    h_info[0]=seq[:pos[0]-1] + '<span class="reg_on_hyb">' + seq[pos[0]-1:pos[1]] + '</span>' + seq[pos[1]:]
    h_info[2]='<span class="reg_on_hyb">' + h_info[2] +'</span>'

    return h_info
def search1(outfile,userID,way):
    file_path=media_path+userID+"/"+way+"/"




    hybrid_info=["hybrid_seq","hybrid_len","reg_hyb_target_pos","remain_pos"]
    new_hybrid_info=["CLASH Read","CLASH read Length","Region identified by Regulator","Region identified by Target"]
    # show_info=["hybrid0","read_count","RNAfold_MFE","regulator_name","regulator_seq","regulator_len","on_reg_pos","rem_tran_target_pos","RNAup_pos","RNAup_score","RNAup_target_seq"]
    show_info=["hybrid0","read_count","RNAfold_MFE","regulator_name","regulator_len","rem_tran_target_pos","RNAup_pos","RNAup_score","RNAup_target_seq"]
    new_show_info=["CLASH Read ID","Read Count","RNAfold MFE","Small RNA Name","Small RNA Length","CLASH Identified Region","Predicted Target Stie","RNAup Score","Pairing (Top:Target,Bottom:Regulator)"]
    tran_info=["transcript_name","transcript_len"]
    new_tran_info=["Target RNA Name","Target RNA Length"]


    tdata=[]
    tcolumn=[]
    h_info=[new_hybrid_info]
    pre_pos_array=[]
    pos_array=[]
    pos_info=[new_show_info]

    data = pd.read_csv(file_path+outfile,usecols=show_info+hybrid_info+["RNAup_input_seq"])
    print(data.head())
    print(data.columns)

    # calculate color of seq
    data["RNAup_target_seq"]=data.apply(lambda x :showSeq(x["RNAup_target_seq"],x["RNAup_input_seq"]),axis=1)
    data=data.fillna("")


    # get transcript info
    tran_data=pd.read_csv(file_path+outfile,usecols=tran_info,chunksize=1)
    tran=list(tran_data.get_chunk(1).values[0])
    transcript_info=[new_tran_info,tran]
    transcript_len=int(tran[1])


    for i in data.index:
        show_list=list(data.loc[i,show_info])
#
        pos_info.append(show_list.copy())
        show_list.insert(0,i)
        tdata.append(show_list)

        #h_info
        h_info.append(h_inof_add_color(list(data.loc[i,hybrid_info])))

# hybrid_info for hybrid id
    tcolumn.append({"title":"hybrid_info"})
    for i in new_show_info:
        tcolumn.append({"title":i})

#-------------- pos array ----------------
    pre_pos_array=data["RNAup_pos"]
# pre_pos_array=["1-10","2-5","1-4","5-6"]
    for i in range(len(pre_pos_array)):
        #because pos may be negative
        aaa=pre_pos_array[i].split("-")
        if len(aaa) == 2:
            pos_split = list(map(int,aaa))
        elif len(aaa) == 3:
            print("====negative pos====")
            pos_split = [1,int(aaa[2])]
        else:
            raise ValueError

        if pos_split[1] > transcript_len:
            print("====longer then transcript_len====")
            pos_split[1]=transcript_len
        pos_split.insert(0,i)
        pos_array.append(pos_split)

    pos_array.sort(key=lambda x: [x[1],x[2]])

# caculate level layer

    level = 0
    max_level = 0
    level_lastPos = [0]

    for i in pos_array:
        # index 2 mean ending pos
        level=0
        while(True):
            if i[1] >= level_lastPos[level]:   
                level_lastPos[level]=i[2]
                i.append(level+1)
                if level > max_level:
                    max_level = level
                break
            else:
                level+=1
                if(len(level_lastPos)==level):
                    level_lastPos.append(i[2])
                    i.append(level+1)
                    if level > max_level:
                        max_level = level
                    break

#-------------- result -------------------
    result={}
    result["column"]=tcolumn
    result["data"]=tdata
    result["col_num"]=data.shape[0]
    result["hybrid_info"]=h_info
    result["transcript_len"]=transcript_len
    result["transcript_info"]=transcript_info
    result["pos_info"]=pos_info
    result["pos_array"]=pos_array
    result["max_level"]=max_level+1
    return result


def search2(name,userID,way):
    file_path=media_path+userID+"/"+way+"/"
    gene_file=media_path+userID+"/gene_file.csv"
    outfile="ori_reg.csv"
    command='bash {}search_name.sh "{}" {} step6.csv {}'.format(script_folder,name,file_path,outfile)
    subprocess.call(command,shell=True)


    table=[]
    if os.path.exists(gene_file): 
        gene_exist=1
        command='bash {}reg_merge_gene.sh {} {} {}'.format(script_folder,file_path+outfile,gene_file,file_path+"merge_gene.csv")
        subprocess.call(command,shell=True)
        print(command)

        data = pd.read_csv(file_path+"merge_gene.csv")
        groups = data.groupby(data["transcript_name"])

        for name,group in groups:
            table.append([group.iloc[0,0],name,len(group),0])
    else:
        gene_exist=0

        data = pd.read_csv(file_path+outfile,usecols=["transcript_name"])
        groups = data.groupby(data["transcript_name"])

        for name,group in groups:
            table.append([name,len(group),0])

    return table,gene_exist

def copy_example(request):
    media_path = '/home/bba753951/Django/master_project/media/uploadfile/example'
    subprocess.call("mkdir "+media_path, shell=True)
    example_path = '/home/bba753951/Django/master_project/media/example_data/'
    command='cp {}* {}'.format(example_path,media_path)
    subprocess.call(command,shell=True)
    return JsonResponse({"data":"ok"})


def site_link(request):
    name=request.GET.get("name")
    mtype=request.GET.get("mtype")
    reg_name=request.GET.get("regulator")
    userID=request.GET.get("userID")
    way=request.GET.get("way","clan")
    count=request.GET.get("count","0")
    search_file=request.GET.get("sfile","step6")+".csv"
    tTitle=""
    file_path=media_path+userID+"/"+way+"/"

    print(mtype)
    if mtype=="transcript":
        print("======search1:",search_file)
        outfile="table.csv"
        command='bash {}search_name.sh "{}" {} {} {}'.format(script_folder,name,file_path,search_file,outfile)
        print("======search1:",command)
        subprocess.call(command,shell=True)
        result=search1(outfile,userID,way)
    elif mtype=="regulator":
        print("----------------------")
        print(name)
        result,gene_exist=search2(name,userID,way)
        tTitle="The small RNA <span class='reg_text'>{}</span> has {} target RNAs".format(name,count)
        return render_to_response('reg_tran.html',locals())

    if reg_name:
        tTitle="For the target RNA <span class='tran_text'>{}</span> <br> # of the small RNA <span class='reg_text'>{}</span> target evidences = {}".format(name,reg_name,count)
    else:
        tTitle="For the target RNA <span class='tran_text'>{}</span> <br> # of small RNAs target = {}".format(name,count)

    return render_to_response('site_table.html',locals())



def usage(request):
    return render_to_response('usage.html',locals())

def analyse(request):
    return render_to_response('analyse.html',locals())

def contact(request):
    return render_to_response('contact.html',locals())

@csrf_exempt
def usage_upload(request):
    suite_bin = "/home/bba753951/suite/bin/"

    # task_id="".join(random.choice(string.ascii_letters+string.digits) for x in range(10))
    # id_path=media_path+task_id+"/"
    # print(request.method)
    # print("task_id=======",task_id)


    # print("upload---------------\n\n\n")
    # if request.method == 'POST':
        # hyb_file = request.FILES.get('zip_file')
        # mail = request.POST.get("mail")

        # adaptor = getDefault(request.POST.get("adaptor","None"),"None")
        # hyb_len_g = getDefault(request.POST.get("hyb_len_g",17),17)
        # hyb_len_l = getDefault(request.POST.get("hyb_len_l",70),70)
        # phred_score = getDefault(request.POST.get("phred_score",30),30)
        # trimmed_tool = getDefault(request.POST.get("trimmed_tool","flexbar"),"flexbar")

        # readCount = getDefault(request.POST.get("readCount","None"),"None")
        # RNAfold_MFE = getDefault(request.POST.get("RNAfold_MFE","None"),"None")

        # reg_mis = getDefault(request.POST.get("reg_mis",0),0)
        # tran_mis = getDefault(request.POST.get("tran_mis",0),0)
        # rem_len = getDefault(request.POST.get("rem_len",17),17)
        # hyb_hit_p = getDefault(request.POST.get("hyb_hit_p",10),10)
        # hyb_thres_h = getDefault(request.POST.get("hyb_thres_h",0.1),0.1)
        # hyb_overlap_h = getDefault(request.POST.get("hyb_overlap_h",4),4)
        # hyb_hit_h = getDefault(request.POST.get("hyb_hit_h",10),10)
        # frag_len_c = getDefault(request.POST.get("frag_len_c",17),17)
        # hyb_overlap_c = getDefault(request.POST.get("hyb_overlap_c",4),4)
        # hyb_hit_c = getDefault(request.POST.get("hyb_hit_c",10),10)

        # RNAup_score = getDefault(request.POST.get("RNAup_score","None"),"None")



        # subprocess.call("mkdir "+id_path, shell=True)
        # print("mkdir")
        # savefile(hyb_file,"upload.zip",id_path)
        # print("save3")

        # cal_time="/usr/bin/time -f \"\t%E real,\t%U user,\t%S sys\" -a -o {}time_log".format(id_path)
        # command=". {}env_path.sh".format(script_folder)
        # command1="bash {}changeState.sh {} {} {}".format(script_folder,task_id,1,2) 
        # command2="bash {}un_zip.sh {}upload.zip".format(script_folder,id_path)
        # run1="cd {}".format(id_path)

        # run2="{} make -f {}makefile preprocess qc={} trim={} link={} len={} slen={} rc={} fd={} in=hyb_file.fastq".format(cal_time,suite_bin,trimmed_tool,phred_score,adaptor,hyb_len_g,hyb_len_l,readCount,RNAfold_MFE)
        # run3="{} make -f {}makefile build reg=reg_file.fasta tran=tran_file.fasta in=hyb_file.fastq".format(cal_time,suite_bin)

        # run4="mkdir pir hyb clan"


        # run5="{} make -f {}makefile detect way=pir llen={} reg_mis={} tran_mis={} hmax={} reg=reg_file.fasta tran=tran_file.fasta in=hyb_file.fastq".format(cal_time,suite_bin,rem_len,reg_mis,tran_mis,hyb_hit_p)
        # run5_1="{} make -f {}makefile analyse reg=reg_file.fasta tran=tran_file.fasta in=hyb_file.fastq way=pir".format(cal_time,suite_bin,RNAup_score)
        # run5_2="mv hyb_file_step5.csv pir/"
        # run5_3="rm hyb_file_step4.csv"


        # run6="{} make -f {}makefile detect way=hyb hval={} hmax={} gmax={} reg=reg_file.fasta tran=tran_file.fasta in=hyb_file.fastq".format(cal_time,suite_bin,hyb_thres_h,hyb_hit_h,hyb_overlap_h)
        # run6_1="{} make -f {}makefile analyse reg=reg_file.fasta tran=tran_file.fasta in=hyb_file.fastq way=hyb".format(cal_time,suite_bin,RNAup_score)
        # run6_2="mv hyb_file_step5.csv hyb/"
        # run6_3="rm hyb_file_step4.csv"



        # run7="{} make -f {}makefile detect way=clan llen={} hmax={} gmax={} reg=reg_file.fasta tran=tran_file.fasta in=hyb_file.fastq".format(cal_time,suite_bin,frag_len_c,hyb_hit_c,hyb_overlap_c)
        # run7_1="{} make -f {}makefile analyse reg=reg_file.fasta tran=tran_file.fasta in=hyb_file.fastq way=clan".format(cal_time,suite_bin,RNAup_score)
        # run7_2="mv hyb_file_step5.csv clan/"
        # run7_3="rm hyb_file_step4.csv"

        # command3="bash {}changeState.sh {} {} {}".format(script_folder,task_id,2,3) 
        # command4='echo "Your analysis is completed,and your Job ID is {0}.\n Or you can click this link to see result http://{2}.ee.ncku.edu.tw/master_project/browse?id={0}&up={3}&fold={4}&readCount={5}" | mail -s "Analysis completed from {2}" -a "From: CosbiLab <bba753951@{2}.ee.ncku.edu.tw>" {1}'.format(task_id,mail,server,RNAup_score,RNAfold_MFE,readCount)
        # command5="bash {}schedule.sh".format(script_folder) 

        # with open(id_path+"run.sh","w") as fp:
            # fp.write(command+"\n\n")
            # fp.write(command1+"\n\n")
            # fp.write(command2+"\n\n")
            # fp.write(run1+"\n\n")
            # fp.write(run2+"\n\n")
            # fp.write(run3+"\n\n")
            # fp.write(run4+"\n\n")
            # fp.write(run5+"\n\n")
            # fp.write(run5_1+"\n\n")
            # fp.write(run5_2+"\n\n")
            # fp.write(run5_3+"\n\n")
            # fp.write(run6+"\n\n")
            # fp.write(run6_1+"\n\n")
            # fp.write(run6_2+"\n\n")
            # fp.write(run6_3+"\n\n")
            # fp.write(run7+"\n\n")
            # fp.write(run7_1+"\n\n")
            # fp.write(run7_2+"\n\n")
            # fp.write(run7_3+"\n\n")
            # fp.write(command3+"\n\n")
            # fp.write(command4+"\n\n")
            # fp.write(command5+"\n\n")

        # with open(info_path+"info.csv","a+") as fp:
            # fp.write(task_id+","+mail+",0\n")


        # infoTxt="<span class='info'>Adaptor Sequence: {}<br><br> CLASH read Length &ge;{} <br><br> CLASH read Length &le;{} <br><br> Phred Score &ge;{} <br><br> Trimmed Tool:{} <br><br> Read Count &ge;{} <br><br> RNAfold_MFE &le; {}<br><br>Way:PIR <br><br>Align to Regulator Mismatch &le; {}<br><br>Align to Transcript Mismatch &le; {} <br><br>Remaining Sequence Length &ge;{} <br><br> Hits per read &le; {}<br><br>Way:HYB<br><br>Fragement Selection Threshold &le;{} <br><br>Overlap between Fragments &le;{} <br><br>Hits per read &le;{}<br><br>Way:CLAN<br><br>Fragments Length &ge;{}<br><br>Overlap between Fragments &le;{}<br><br>Hits per Fragment &le;{} <br><br> RNAup_score &le; {} <br></span>".format(adaptor,hyb_len_g,hyb_len_l,phred_score,trimmed_tool,readCount,RNAfold_MFE,reg_mis,tran_mis,rem_len,hyb_hit_p,hyb_thres_h,hyb_overlap_h,hyb_hit_h,frag_len_c,hyb_overlap_c,hyb_hit_c,RNAup_score)
        # with open(id_path+"info_para.txt","w") as fp:
            # fp.write(infoTxt)
            
        # confirm_command='echo "We already recived your analysis request. If your analysis is done,we will sent another mail to inform you." | mail -s "Response mail from {2}" -a "From: CosbiLab <bba753951@{2}.ee.ncku.edu.tw>" {1}'.format(task_id,mail,server)
        # subprocess.call(confirm_command, shell=True)

    return JsonResponse({"data":"ok","userID":task_id})

@csrf_exempt
def analyse_upload(request):
    suite_bin = "/home/bba753951/suite/bin/"

    task_id="".join(random.choice(string.ascii_letters+string.digits) for x in range(10))
    id_path=media_path+task_id+"/"
    print(request.method)
    print("task_id=======",task_id)


    print("upload---------------\n\n\n")
    if request.method == 'POST':
        # upload file
        use_old_id = getDefault(request.POST.get("use_old_id","None"),"None").strip()
        old_id_path=media_path+use_old_id+"/"
        reg_select = getDefault(request.POST.get("reg_select","-1"),"-1")
        target_select = getDefault(request.POST.get("target_select","-1"),"-1")

        if use_old_id == "None":
            if reg_select == "0":
                regulator_file = request.FILES.get('zip_regulator')
            if target_select == "0":
                target_file = request.FILES.get('zip_target')

            read_file = request.FILES.get('zip_read')


        mail = request.POST.get("mail")


        barcode = getDefault(request.POST.get("barcode","None"),"None")
        # preporcess
        prep_check = getDefault(request.POST.get("prep_check","1"),"1")
        adaptor = getDefault(request.POST.get("adaptor","None"),"None")
        hyb_len_g = getDefault(request.POST.get("hyb_len_g",17),17)
        hyb_len_l = getDefault(request.POST.get("hyb_len_l",70),70)
        phred_score = getDefault(request.POST.get("phred_score",30),30)
        trimmed_tool = getDefault(request.POST.get("trimmed_tool","trim_galore"),"trim_galore")

        # quality
        readCount = getDefault(request.POST.get("readCount","None"),"None")
        RNAfold_MFE = getDefault(request.POST.get("RNAfold_MFE","None"),"None")

        # find pairs 
        find_way = getDefault(request.POST.get("findway","clan"),"clan")
        ## pir
        reg_mis = getDefault(request.POST.get("reg_mis",0),0)
        tran_mis = getDefault(request.POST.get("tran_mis",0),0)
        rem_len = getDefault(request.POST.get("rem_len",17),17)
        hyb_hit_p = getDefault(request.POST.get("hyb_hit_p",10),10)
        ## hyb
        hyb_thres_h = getDefault(request.POST.get("hyb_thres_h",0.1),0.1)
        hyb_overlap_h = getDefault(request.POST.get("hyb_overlap_h",4),4)
        hyb_hit_h = getDefault(request.POST.get("hyb_hit_h",10),10)
        ## clan
        frag_len_c = getDefault(request.POST.get("frag_len_c",17),17)
        hyb_overlap_c = getDefault(request.POST.get("hyb_overlap_c",4),4)
        hyb_hit_c = getDefault(request.POST.get("hyb_hit_c",10),10)

        # analyse
        RNAup_score = getDefault(request.POST.get("RNAup_score","None"),"None")

        if adaptor=="None" and trimmed_tool != "trim_galore":
            print("error adapter")
            raise ValueError


        subprocess.call("mkdir "+id_path, shell=True)
        print("mkdir")
        print("==========================================")
        print("use_old_id",use_old_id)

        if use_old_id == "None":

            print("reg_select",reg_select)
            print("target_select",target_select)

            savefile(read_file,"read.zip",id_path)
            if reg_select == "0":
                savefile(regulator_file,"regulator.zip",id_path)
            else:
                print("cp {}{}.zip {}regulator.zip".format(reference_path,reg_select,id_path))
                subprocess.call("cp {}{}.zip {}regulator.zip".format(reference_path,reg_select,id_path), shell=True)
            if target_select == "0":
                savefile(target_file,"target.zip",id_path)
            else:
                print("cp {}{}.zip {}target.zip".format(reference_path,target_select,id_path))
                subprocess.call("cp {}{}.zip {}target.zip".format(reference_path,target_select,id_path), shell=True)
        else:
            if not os.path.isdir(id_path):
                print("old id not exist: ",use_old_id)
                raise ValueError
            subprocess.call("cp {}*.zip {}".format(old_id_path,id_path), shell=True)



        print("barcode:",barcode)

        b1="echo no barcode"
        b2=""
        b3=""
        if barcode != "None":
            b1="/home/bba753951/suite/hyb-master/bin/hyb demultiplex in=hyb_file.fastq code=barcode.txt"

            b2="mv hyb_file.fastq ori_hyb_file.fastq"
            b3="mv {}_bar.txt hyb_file.fastq".format(barcode)
            with open(id_path+"barcode.txt","w") as fp:
                fp.write(barcode+"\tbar")


        cal_time="/usr/bin/time -f \"\t%E real,\t%U user,\t%S sys\" -a -o {}time_log".format(id_path)
        command=". {}".format(pipeline_env)
        command1="bash {}changeState.sh {} {} {}".format(script_folder,task_id,1,2) 
        command2="bash {}un_zip.sh {}".format(script_folder,id_path)
        run1="cd {}".format(id_path)

        run2="{} make -f {}makefile preprocess qc={} trim={} link={} len={} slen={} rc={} fd={} in=hyb_file.fastq".format(cal_time,suite_bin,trimmed_tool,phred_score,adaptor,hyb_len_g,hyb_len_l,readCount,RNAfold_MFE)
        if prep_check == "0":
            run2="{} make -f {}makefile preprocess qc={} trim={} link={} len={} slen={} rc={} fd={} use_trim={} in=hyb_file.fastq".format(cal_time,suite_bin,"trim_galore",phred_score,adaptor,hyb_len_g,hyb_len_l,readCount,RNAfold_MFE,prep_check)

        print(run2)
        run3="{} make -f {}makefile build reg=reg_file.fasta tran=tran_file.fasta in=hyb_file.fastq".format(cal_time,suite_bin)

        run4="mkdir pir hyb clan"
        ## pir   
        run5="{} make -f {}makefile detect way=pir llen={} reg_mis={} tran_mis={} hmax={} reg=reg_file.fasta tran=tran_file.fasta in=hyb_file.fastq".format(cal_time,suite_bin,rem_len,reg_mis,tran_mis,hyb_hit_p)
        run5_1="{} make -f {}makefile analyse reg=reg_file.fasta tran=tran_file.fasta in=hyb_file.fastq way=pir".format(cal_time,suite_bin,RNAup_score)
        run5_2="mv hyb_file_step5.csv pir/"
        run5_3="rm hyb_file_step4.csv"
        ## hyb   
        run6="{} make -f {}makefile detect way=hyb hval={} hmax={} gmax={} reg=reg_file.fasta tran=tran_file.fasta in=hyb_file.fastq".format(cal_time,suite_bin,hyb_thres_h,hyb_hit_h,hyb_overlap_h)
        run6_1="{} make -f {}makefile analyse reg=reg_file.fasta tran=tran_file.fasta in=hyb_file.fastq way=hyb".format(cal_time,suite_bin,RNAup_score)
        run6_2="mv hyb_file_step5.csv hyb/"
        run6_3="rm hyb_file_step4.csv"
        ## clan   
        run7="{} make -f {}makefile detect way=clan llen={} hmax={} gmax={} reg=reg_file.fasta tran=tran_file.fasta in=hyb_file.fastq".format(cal_time,suite_bin,frag_len_c,hyb_hit_c,hyb_overlap_c)
        run7_1="{} make -f {}makefile analyse reg=reg_file.fasta tran=tran_file.fasta in=hyb_file.fastq way=clan".format(cal_time,suite_bin,RNAup_score)
        run7_2="mv hyb_file_step5.csv clan/"
        run7_3="rm hyb_file_step4.csv"

        command3="bash {}changeState.sh {} {} {}".format(script_folder,task_id,2,3) 
        command4='echo "Your analysis is completed,and your Job ID is {0}.\n Or you can click this link to see result http://{2}.ee.ncku.edu.tw/master_project/browse?id={0}" | mail -s "Analysis completed from {2}" -a "From: CosbiLab <bba753951@{2}.ee.ncku.edu.tw>" {1}'.format(task_id,mail,server)
        command5="bash {}schedule.sh".format(script_folder) 

        with open(id_path+"run.sh","w") as fp:
            fp.write(command+"\n\n")
            fp.write(command1+"\n\n")
            fp.write(command2+"\n\n")
            fp.write(run1+"\n\n")
            fp.write(b1+"\n\n")
            fp.write(b2+"\n\n")
            fp.write(b3+"\n\n")
            fp.write(run2+"\n\n")
            fp.write(run3+"\n\n")
            fp.write(run4+"\n\n")
            fp.write(run5+"\n\n")
            fp.write(run5_1+"\n\n")
            fp.write(run5_2+"\n\n")
            fp.write(run5_3+"\n\n")
            fp.write(run6+"\n\n")
            fp.write(run6_1+"\n\n")
            fp.write(run6_2+"\n\n")
            fp.write(run6_3+"\n\n")
            fp.write(run7+"\n\n")
            fp.write(run7_1+"\n\n")
            fp.write(run7_2+"\n\n")
            fp.write(run7_3+"\n\n")
            fp.write(command3+"\n\n")
            fp.write(command4+"\n\n")
            fp.write(command5+"\n\n")

        with open(info_path+"info.csv","a+") as fp:
            fp.write(task_id+","+mail+",0\n")

        with open(id_path+"findway.csv","w") as fp:
            fp.write(find_way)

        # infoDiv='<div class="ui left labeled button btn_margin_top mini" tabindex="0">\
                  # <a class="ui right pointing label">\
                    # {}\
                  # </a>\
                  # <div class="ui basic button">\
                    # {}\
                  # </div>\
                # </div>'
        infoDiv="<tr>\
                <td class='positive'>{}</td>\
                <td>{}</td>\
                </tr>"

        infoTxt=infoDiv.format("Barcode Sequence",barcode)
        infoTxt=infoTxt + infoDiv.format("Trimmed Tool",trimmed_tool)
        infoTxt=infoTxt + infoDiv.format("Adapter Sequence",adaptor)
        infoTxt=infoTxt + infoDiv.format("CLASH Read Length &ge;",hyb_len_g)
        infoTxt=infoTxt + infoDiv.format("CLASH Read Length &le;",hyb_len_l)
        infoTxt=infoTxt + infoDiv.format("Phred Score &ge;",phred_score)


        if find_way=="pir":
            infoTxt=infoTxt + infoDiv.format("Algorithm","piRTarBase")
            infoTxt=infoTxt + infoDiv.format("Mismatch of Aligning to Regulator &le;",reg_mis)
            infoTxt=infoTxt + infoDiv.format("Mismatch of Aligning to Target &le;",tran_mis)
            infoTxt=infoTxt + infoDiv.format("Remaining Sequence Length &ge;",rem_len)
            infoTxt=infoTxt + infoDiv.format("Hits per Read &le;",hyb_hit_c)

        elif find_way=="hyb":
            infoTxt=infoTxt + infoDiv.format("Algorithm","Hyb")
            infoTxt=infoTxt + infoDiv.format("Fragment Selection Threshold &le;",hyb_thres_h)
            infoTxt=infoTxt + infoDiv.format("Overlap/Gap between Fragments &le;",hyb_overlap_h)
            infoTxt=infoTxt + infoDiv.format("Hits per Read &le;",hyb_hit_h)

        elif find_way=="clan":
            infoTxt=infoTxt + infoDiv.format("Algorithm","CLAN")
            infoTxt=infoTxt + infoDiv.format("Fragments Length &ge;",frag_len_c)
            infoTxt=infoTxt + infoDiv.format("Overlap between Fragments &le;",hyb_overlap_c)
            infoTxt=infoTxt + infoDiv.format("Hits per Fragment &le;",hyb_hit_c)

        else:
            infoTxt="find way error"
            raise ValueError

        with open(id_path+"info_para.txt","w") as fp:
            fp.write(infoTxt)
            
        # confirm_command='echo "if you want to start your analysis,please click this link http://{2}.ee.ncku.edu.tw/master_project/browse/confirmMail?id={0}" | mail -s "Confirm mail from {2}" -a "From: CosbiLab <bba753951@{2}.ee.ncku.edu.tw>" {1}'.format(task_id,mail,server)
        confirm_command='echo "We already recived your analysis request. If your analysis is done,we will sent another mail to inform you." | mail -s "Response mail from {2}" -a "From: CosbiLab <bba753951@{2}.ee.ncku.edu.tw>" {1}'.format(task_id,mail,server)
        subprocess.call(confirm_command, shell=True)

    return JsonResponse({"data":"ok","userID":task_id})


# when user confirm mail,change info.csv from 0 to 1
def confirmMail(request):
    folder_id=request.GET.get("id")
    print("========confirm===========",folder_id)

    data=pd.read_csv(info_path+"info.csv",header=None,index_col=0)
    if data.loc[folder_id,2] == 0:
        data.loc[folder_id,2]=1
        data.to_csv(info_path+"info.csv",header=0)
        command="bash {}schedule.sh".format(script_folder)
        subprocess.call(command, shell=True)
    # return render_to_response('confirm.html',locals())
    return JsonResponse({"data":"ok","userID":folder_id})


