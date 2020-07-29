import pandas as pd
import sys



fi="hyb_file_step5.csv"
id_path=sys.argv[1]
out_file=sys.argv[2]

def readData(way):
    data=pd.read_csv(id_path+"/"+way+"/"+fi,usecols=["regulator_name","transcript_name"])
    data=data.drop_duplicates(subset=None, keep='first', inplace=False)
    data['ID']=data.apply(lambda x: x['regulator_name']+"/"+x["transcript_name"],axis=1)
    data=data.drop(["regulator_name","transcript_name"],axis=1)
    return data



pir_data=readData("pir")
hyb_data=readData("hyb")
clan_data=readData("clan")

# print(pir_data.shape)
# print(hyb_data.shape)
# print(clan_data.shape)

all_data=pd.concat([pir_data,hyb_data,clan_data],axis=0,ignore_index=True)
# print(all_data.shape)
all_data=all_data.drop_duplicates(subset=None, keep='first', inplace=False)
# print(all_data.shape)

clan_data["clan"]=1
pir_data["pir"]=1
hyb_data["hyb"]=1

pir_data=pir_data.set_index(["ID"])
clan_data=clan_data.set_index(["ID"])
hyb_data=hyb_data.set_index(["ID"])
all_data=all_data.set_index(["ID"])

all_data=pd.concat([all_data,pir_data,hyb_data,clan_data],axis=1,join_axes=[all_data.index])
all_data=all_data.fillna(0)

all_data.to_csv(out_file)



