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

def downloadList(request):        
    folder_id=request.GET.get("id","")
    way=request.GET.get("way","")
    id_path=media_path+folder_id+"/"+way+"/"
    command="zip -j {0}download.zip {0}step6*.csv".format(id_path)
    subprocess.call(command, shell=True)
    print(id_path+"download.zip")
    response = FileResponse(open(id_path+"download.zip","rb"))
    response["Content-Type"]="application/octet-stream"
    response["Content-Disposition"]="attachment;filename=download.zip"
    return response





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
        return default
    return value

@csrf_exempt
def uploadfile(request):
# for browse
    print(request)



    print("upload---------------\n\n\n")
    if request.method == 'POST':

        RNAfold_MFE = getDefault(request.POST.get("RNAfold_MFE","None"),"None")
        RNAup_score = getDefault(request.POST.get("RNAup_score","None"),"None")
        readCount = getDefault(request.POST.get("readCount","None"),"None")
        # way = getDefault(request.POST.get("way","pir"),"pir")
        mtype = getDefault(request.POST.get("browse","regulator"),"regulator")
        folder_id = request.POST.get("folder_id")
        id_path=media_path+folder_id+"/"
        task_id=folder_id


        if os.path.isfile("findway.csv"):
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




        column_name=[]
        if mtype=="regulator":
            column_name=[{"title":"Regulatory RNA Name"},
                         {"title":"# of Target RNAs"},
                         {"title":"Target RNA Details"}]
        else:

            if os.path.isfile(id_path+"gene_file.csv"):
                print("gene_file exist")
                column_name=[{"title":"Target Gene Name"},
                             {"title":"Target RNA Name"},
                             {"title":"# of Regulatory RNAs"},
                             {"title":"Target Details"}]
            else:
                print("gene_file not exist")
                column_name=[{"title":"Target RNA Name"},
                             {"title":"# of Regulatory RNAs"},
                             {"title":"Target Details"}]
        return JsonResponse({"data":column_name,"userID":task_id,"way":way})


def showSeq(seq1,seq2):
    seq1=seq1.replace("T","U")
    seq2=seq2.replace("T","U")

    seq2=seq2[::-1]

    count=0
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
    new_show_info=["CLASH Read ID","Read Count","RNAfold MFE","Regulatory RNA Name","Regulatory RNA Length","CLASH Identified Region","Predicted Target Stie","RNAup Score","Pairing (Top:Target,Bottom:Regulator)"]
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
        tTitle="The regulatory RNA <span class='reg_text'>{}</span> has {} target RNAs".format(name,count)
        return render_to_response('reg_tran.html',locals())

    if reg_name:
        tTitle="For the target RNA <span class='tran_text'>{}</span> <br> # of the regulatory RNA <span class='reg_text'>{}</span> target evidences = {}".format(name,reg_name,count)
    else:
        tTitle="For the target RNA <span class='tran_text'>{}</span> <br> # of regulatory RNAs target = {}".format(name,count)

    return render_to_response('site_table.html',locals())



def usage(request):
    return render_to_response('usage.html',locals())

def analyse(request):
    return render_to_response('analyse.html',locals())

@csrf_exempt
def usage_upload(request):
    suite_bin = "/home/bba753951/suite/bin/"

    task_id="".join(random.choice(string.ascii_letters+string.digits) for x in range(10))
    id_path=media_path+task_id+"/"
    print(request.method)
    print("task_id=======",task_id)


    print("upload---------------\n\n\n")
    if request.method == 'POST':
        # upload file
        hyb_file = request.FILES.get('zip_file')
        mail = request.POST.get("mail")

        # preporcess
        adaptor = getDefault(request.POST.get("adaptor","None"),"None")
        hyb_len_g = getDefault(request.POST.get("hyb_len_g",17),17)
        hyb_len_l = getDefault(request.POST.get("hyb_len_l",70),70)
        phred_score = getDefault(request.POST.get("phred_score",30),30)
        trimmed_tool = getDefault(request.POST.get("trimmed_tool","flexbar"),"flexbar")

        # quality
        readCount = getDefault(request.POST.get("readCount","None"),"None")
        RNAfold_MFE = getDefault(request.POST.get("RNAfold_MFE","None"),"None")

        # find pairs 
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



        subprocess.call("mkdir "+id_path, shell=True)
        print("mkdir")
        savefile(hyb_file,"upload.zip",id_path)
        print("save3")

        cal_time="/usr/bin/time -f \"\t%E real,\t%U user,\t%S sys\" -a -o {}time_log".format(id_path)
        command=". {}env_path.sh".format(script_folder)
        command1="bash {}changeState.sh {} {} {}".format(script_folder,task_id,1,2) 
        command2="bash {}un_zip.sh {}upload.zip".format(script_folder,id_path)
        run1="cd {}".format(id_path)

        run2="{} make -f {}makefile preprocess qc={} trim={} link={} len={} slen={} rc={} fd={} in=hyb_file.fastq".format(cal_time,suite_bin,trimmed_tool,phred_score,adaptor,hyb_len_g,hyb_len_l,readCount,RNAfold_MFE)
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
        command4='echo "Your analysis is completed,and your Job ID is {0}.\n Or you can click this link to see result http://{2}.ee.ncku.edu.tw/master_project/browse?id={0}&up={3}&fold={4}&readCount={5}" | mail -s "Analysis completed from {2}" -a "From: CosbiLab <bba753951@{2}.ee.ncku.edu.tw>" {1}'.format(task_id,mail,server,RNAup_score,RNAfold_MFE,readCount)
        command5="bash {}schedule.sh".format(script_folder) 

        with open(id_path+"run.sh","w") as fp:
            fp.write(command+"\n\n")
            fp.write(command1+"\n\n")
            fp.write(command2+"\n\n")
            fp.write(run1+"\n\n")
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


        infoTxt="<span class='info'>Adaptor Sequence: {}<br><br> CLASH read Length &ge;{} <br><br> CLASH read Length &le;{} <br><br> Phred Score &ge;{} <br><br> Trimmed Tool:{} <br><br> Read Count &ge;{} <br><br> RNAfold_MFE &le; {}<br><br>Way:PIR <br><br>Align to Regulator Mismatch &le; {}<br><br>Align to Transcript Mismatch &le; {} <br><br>Remaining Sequence Length &ge;{} <br><br> Hits per read &le; {}<br><br>Way:HYB<br><br>Fragement Selection Threshold &le;{} <br><br>Overlap between Fragments &le;{} <br><br>Hits per read &le;{}<br><br>Way:CLAN<br><br>Fragments Length &ge;{}<br><br>Overlap between Fragments &le;{}<br><br>Hits per Fragment &le;{} <br><br> RNAup_score &le; {} <br></span>".format(adaptor,hyb_len_g,hyb_len_l,phred_score,trimmed_tool,readCount,RNAfold_MFE,reg_mis,tran_mis,rem_len,hyb_hit_p,hyb_thres_h,hyb_overlap_h,hyb_hit_h,frag_len_c,hyb_overlap_c,hyb_hit_c,RNAup_score)
        with open(id_path+"info_para.txt","w") as fp:
            fp.write(infoTxt)
            
        confirm_command='echo "if you want to start your analysis,please click this link http://{2}.ee.ncku.edu.tw/master_project/browse/confirmMail?id={0}" | mail -s "Confirm mail from {2}" -a "From: CosbiLab <bba753951@{2}.ee.ncku.edu.tw>" {1}'.format(task_id,mail,server)
        subprocess.call(confirm_command, shell=True)

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
        read_file = request.FILES.get('zip_read')
        regulator_file = request.FILES.get('zip_regulator')
        target_file = request.FILES.get('zip_target')

        mail = request.POST.get("mail")


        barcode = getDefault(request.POST.get("barcode","None"),"None")
        # preporcess
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

        savefile(read_file,"read.zip",id_path)
        savefile(regulator_file,"regulator.zip",id_path)
        savefile(target_file,"target.zip",id_path)
        print("save3")

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
        command=". {}env_path.sh".format(script_folder)
        command1="bash {}changeState.sh {} {} {}".format(script_folder,task_id,1,2) 
        command2="bash {}un_zip.sh {}".format(script_folder,id_path)
        run1="cd {}".format(id_path)

        run2="{} make -f {}makefile preprocess qc={} trim={} link={} len={} slen={} rc={} fd={} in=hyb_file.fastq".format(cal_time,suite_bin,trimmed_tool,phred_score,adaptor,hyb_len_g,hyb_len_l,readCount,RNAfold_MFE)
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
        command4='echo "Your analysis is completed,and your Job ID is {0}.\n Or you can click this link to see result http://{2}.ee.ncku.edu.tw/master_project/browse?id={0}&way={3}" | mail -s "Analysis completed from {2}" -a "From: CosbiLab <bba753951@{2}.ee.ncku.edu.tw>" {1}'.format(task_id,mail,server,find_way)
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


        if find_way=="pir":
            infoTxt="<span class='info'>Adapter Sequence: {}<br><br> CLASH read Length &ge;{} <br><br> CLASH read Length &le;{} <br><br> Phred Score &ge;{} <br><br> Trimmed Tool:{} <br><br> Algorithm:piRTarBase <br><br>Align to Regulatory RNA Mismatch &le; {}<br><br>Align to Target RNA Mismatch &le; {} <br><br>Remaining Sequence Length &ge;{} <br><br> Hits per read &le;<br> </span>".format(adaptor,hyb_len_g,hyb_len_l,phred_score,trimmed_tool,reg_mis,tran_mis,rem_len,hyb_hit_p)
        elif find_way=="hyb":
            infoTxt="<span class='info'>Adapter Sequence: {}<br><br> CLASH read Length &ge;{} <br><br> CLASH read Length &le;{} <br><br> Phred Score &ge;{} <br><br> Trimmed Tool:{} <br><br> Algorithm:Hyb<br><br>Fragement Selection Threshold &le;{} <br><br>Overlap between Fragments &le;{} <br><br>Hits per read &le;{} <br></span>".format(adaptor,hyb_len_g,hyb_len_l,phred_score,trimmed_tool,hyb_thres_h,hyb_overlap_h,hyb_hit_h)
        elif find_way=="clan":
            infoTxt="<span class='info'>Adapter Sequence: {}<br><br> CLASH read Length &ge;{} <br><br> CLASH read Length &le;{} <br><br> Phred Score &ge;{} <br><br> Trimmed Tool:{} <br><br> Way:CLAN<br><br>Fragments Length &ge;{}<br><br>Overlap between Fragments &le;{}<br><br>Hits per Fragment &le;{} <br></span>".format(adaptor,hyb_len_g,hyb_len_l,phred_score,trimmed_tool,frag_len_c,hyb_overlap_c,hyb_hit_c)
        else:
            infoTxt="find way error"
            raise ValueError

        with open(id_path+"info_para.txt","w") as fp:
            fp.write(infoTxt)
            
        confirm_command='echo "if you want to start your analysis,please click this link http://{2}.ee.ncku.edu.tw/master_project/browse/confirmMail?id={0}" | mail -s "Confirm mail from {2}" -a "From: CosbiLab <bba753951@{2}.ee.ncku.edu.tw>" {1}'.format(task_id,mail,server)
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
    return render_to_response('confirm.html',locals())


