#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib import font_manager,rc  #한글 폰트 입력을 위한 라이브러리
from matplotlib.patches import ConnectionPatch

#폰트 경로 가져오기
font_path = 'C:\\Windows\\Fonts\\SGL.ttf' #삼성고딕체
 
# 폰트 이름 얻어오기
font_name = font_manager.FontProperties(fname=font_path).get_name()
 
#폰트 설정하기
mpl.rc('font',family=font_name)

#%%
workdir = "C:/Users/smcljy/data/20231124_건강현황"
file_path = '{}/건강현황분석data.dta'.format(workdir)

data = pd.read_stata(file_path)

data
#%%
# 조건별 그룹 설정
### 정상, 기타 결과 그룹 분리
GRP = 'SMOKE'
data.loc[(data['SMK'] == '0'), GRP] = '비흡연'
data.loc[(data['SMK'] == '1'), GRP] = '금연중'
data.loc[(data['SMK'] == '2'), GRP] = '흡연중'

# data.loc[data['GEND_CD'] == 'M', 'GENDER'] = '남'
# data.loc[data['GEND_CD'] == 'F', 'GENDER'] = '여'

data.loc[ data['AGE'] < 45                      ,'AGEGRP'] = '40~44세'
data.loc[(data['AGE'] > 44) & (data['AGE'] < 50),'AGEGRP'] = '45~49세'
data.loc[(data['AGE'] > 49) & (data['AGE'] < 55),'AGEGRP'] = '50~54세'
data.loc[(data['AGE'] > 54) & (data['AGE'] < 60),'AGEGRP'] = '55~59세'
data.loc[ data['AGE'] > 59                      ,'AGEGRP'] = '60세 이상'
# data.head(100)
data
#%%
data_exec = data.drop(data.loc[data['GRP']=='정규일반'].index)
data_norm = data.drop(data.loc[data['GRP']=='임원'].index)

#%%
## pivot table create executive
smoke_cnt_exec = data_exec.pivot_table(
                             index=[GRP,'GRP']
                            ,columns=['AGEGRP']
    ,values=['CDW']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
# each column total value percentile
smoke_per_exec = round(smoke_cnt_exec.div(smoke_cnt_exec.iloc[-1], axis=1).astype(float)*100,1)

# smoke_per_m

smoke_agegrp_exec = pd.DataFrame()

for i in range(len(smoke_cnt_exec.columns)):
    if i == 0:
        smoke_agegrp_exec = pd.concat(
                                [
                                 smoke_cnt_exec.iloc[:,i]
                                ,smoke_per_exec.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        smoke_agegrp_exec = pd.concat(
                                [
                                 smoke_agegrp_exec
                                ,smoke_cnt_exec.iloc[:,i]
                                ,smoke_per_exec.iloc[:,i]
                                ]
                            ,axis=1
        )
        
smoke_agegrp_exec

#%%
## pivot table create normal
smoke_cnt_norm = data_norm.pivot_table(
                             index=[GRP,'GRP']
                            ,columns=['AGEGRP']
    ,values=['CDW']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
# each column total value percentile
smoke_per_norm = round(smoke_cnt_norm.div(smoke_cnt_norm.iloc[-1], axis=1).astype(float)*100,1)

# smoke_per_m

smoke_agegrp_norm = pd.DataFrame()

for i in range(len(smoke_cnt_norm.columns)):
    if i == 0:
        smoke_agegrp_norm = pd.concat(
                                [
                                 smoke_cnt_norm.iloc[:,i]
                                ,smoke_per_norm.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        smoke_agegrp_norm = pd.concat(
                                [
                                 smoke_agegrp_norm
                                ,smoke_cnt_norm.iloc[:,i]
                                ,smoke_per_norm.iloc[:,i]
                                ]
                            ,axis=1
        )
        
smoke_agegrp_norm

#%%
smoke_agegrp = pd.concat([smoke_agegrp_exec.iloc[:-1,:], smoke_agegrp_norm.iloc[:-1,:]],axis=0)

smoke_agegrp.columns = pd.MultiIndex.from_tuples(
        (
         ('40~44세', 'N')
        ,('40~44세', '%')
        ,('45~49세', 'N')
        ,('45~49세', '%')
        ,('50~54세', 'N')
        ,('50~54세', '%')
        ,('55~59세', 'N')
        ,('55~59세', '%')
        ,('60세 이상', 'N')
        ,('60세 이상', '%')
        ,('전체', 'N')
        ,('전체', '%')
        )
    )
smoke_agegrp = smoke_agegrp.sort_index()

labels = []
for i in range(len(smoke_per_exec.columns)-1):
    labels.append(smoke_per_exec.columns[i][1])
    
smoke_agegrp

#%%
smoke_grp_exec = data_exec.pivot_table(
                          columns=['SMOKE']
                         ,values=['CDW']
                         ,aggfunc='count'
)

# smoke_grp

label_pie_exec = smoke_grp_exec.columns.to_list()
label_pie_exec

data_pie_exec = smoke_grp_exec.iloc[0,:].to_list()
data_pie_exec

smoke_grp_norm = data_norm.pivot_table(
                          columns=['SMOKE']
                         ,values=['CDW']
                         ,aggfunc='count'
)

# smoke_grp

label_pie_norm = smoke_grp_norm.columns.to_list()
label_pie_norm

data_pie_norm = smoke_grp_norm.iloc[0,:].to_list()
data_pie_norm

#%%
data_exec.loc[(data_exec['SMOKE']=='흡연중') & (data_exec['SMK_CURRENT_AMOUNT'] == '0'),'SMOKE_AMT'] = '10개비 이하'
data_exec.loc[(data_exec['SMOKE']=='흡연중') & (data_exec['SMK_CURRENT_AMOUNT'] == '1'),'SMOKE_AMT'] = '11~20개비'
# 문진응답내역에서 null 값은 중간값 처리
data_exec.loc[(data_exec['SMOKE']=='흡연중') & (data_exec['SMK_CURRENT_AMOUNT'] == ""),'SMOKE_AMT']  = '11~20개비'
data_exec.loc[(data_exec['SMOKE']=='흡연중') & (data_exec['SMK_CURRENT_AMOUNT'] == '2'),'SMOKE_AMT'] = '21_30개비'
data_exec.loc[(data_exec['SMOKE']=='흡연중') & (data_exec['SMK_CURRENT_AMOUNT'] == '3'),'SMOKE_AMT'] = '31개비 이상'

# data

SMOKE_AMT_cat_exec = data_exec.pivot_table(
                              columns=['SMOKE_AMT']
                             ,values=['CDW'] 
                             ,aggfunc='count'
                             )
SMOKE_AMT_cat_exec

data_bar_exec = SMOKE_AMT_cat_exec.iloc[0,:].to_list()
data_bar_exec

data_bar_per_exec = []

for i in range(len(data_bar_exec)):
    data_bar_per_exec.append(round(data_bar_exec[i]/data_pie_exec[2],3))

data_bar_per_exec

label_bar_exec = ['10개비 이하'
            ,'11~20개비'
            ,'21~30개비'
            ,'31개비 이상'
            ]

label_bar_exec

data_norm.loc[(data_norm['SMOKE']=='흡연중') & (data_norm['SMK_CURRENT_AMOUNT'] == '0'),'SMOKE_AMT'] = '10개비 이하'
data_norm.loc[(data_norm['SMOKE']=='흡연중') & (data_norm['SMK_CURRENT_AMOUNT'] == '1'),'SMOKE_AMT'] = '11~20개비'
# 문진응답내역에서 null 값은 중간값 처리
data_norm.loc[(data_norm['SMOKE']=='흡연중') & (data_norm['SMK_CURRENT_AMOUNT'] == ""),'SMOKE_AMT']  = '11~20개비'
data_norm.loc[(data_norm['SMOKE']=='흡연중') & (data_norm['SMK_CURRENT_AMOUNT'] == '2'),'SMOKE_AMT'] = '21_30개비'
data_norm.loc[(data_norm['SMOKE']=='흡연중') & (data_norm['SMK_CURRENT_AMOUNT'] == '3'),'SMOKE_AMT'] = '31개비 이상'

# data

SMOKE_AMT_cat_norm = data_norm.pivot_table(
                              columns=['SMOKE_AMT']
                             ,values=['CDW'] 
                             ,aggfunc='count'
                             )
SMOKE_AMT_cat_norm

data_bar_norm = SMOKE_AMT_cat_norm.iloc[0,:].to_list()
data_bar_norm

data_bar_per_norm = []

for i in range(len(data_bar_norm)):
    data_bar_per_norm.append(round(data_bar_norm[i]/data_pie_norm[2],3))

data_bar_per_norm

label_bar_norm = ['10개비 이하'
            ,'11~20개비'
            ,'21~30개비'
            ,'31개비 이상'
            ]

label_bar_norm

#%%
fig, ax = plt.subplots(linewidth=2)

plt.figure(figsize=(15,10))
# fig, ax = plt.subplots(figsize=(20,10 ), subplot_kw=dict(aspect="equal"),linewidth=2)
fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정

ax.set_title("그룹별 흡연력 분포\n\n",fontsize=50,y=2.2)

out_category = data_pie_exec
in_category = data_pie_norm
out_labels = label_pie_exec
in_labels = label_pie_norm
# explode = [0.1,0.1, 0,0,0,0,0,0,0,0,0]

out_cmap = plt.get_cmap("tab20")
in_cmap = plt.get_cmap("Pastel1")

outer_colors = out_cmap(np.array([1,0,2]))
inner_colors = in_cmap(np.array([1,2,0]))

w, ts, at = ax.pie(out_category, radius=5, colors=outer_colors,labels=in_labels,
                #    explode = explode,
        rotatelabels =False, startangle=90,counterclock=False,
       pctdistance=0.75, labeldistance=0.85,
       wedgeprops=dict(width=1.5, edgecolor='w'),textprops={'fontsize': 30}, autopct="%1.1f%%")

for t in ts:
    t.set_color('black')
for autotext in at:
    autotext.set_color('black')

w, ts, at = ax.pie(in_category, radius= 3, colors=inner_colors,labels=in_labels,
       rotatelabels =False, startangle=90,counterclock=False,
       pctdistance=0.87, labeldistance=0.37,
     wedgeprops=dict(width=2, edgecolor='w'), textprops={'fontsize': 30}, autopct="%.f%%")

for t in ts:
    t.set_color('black')
for autotext in at:
    autotext.set_color('black')
ax.text(-7.5, -5.5,  '  ', fontsize=22)
ax.text(-5, -5.8,  '  ', fontsize=22)
ax.text(-5, -6.1,  '  ', fontsize=22)
ax.text(4.2, -5.5,  '□ 외측: 임원', fontsize=30)
ax.text(4.2, -6,  '□ 내측: 정규일반', fontsize=30)


fig.tight_layout()
plt.savefig("{}/03_01흡연력_01분포.png".format(workdir)
           , dpi=175)

plt.show()

# %%
labels_bar_dm =['임원','정규일반']

# Bar chart create
value01 = [data_bar_per_exec[0]*100,data_bar_per_norm[0]*100]
value02 = [data_bar_per_exec[1]*100,data_bar_per_norm[1]*100]
value03 = [data_bar_per_exec[2]*100,data_bar_per_norm[2]*100]
value04 = [data_bar_per_exec[3]*100,data_bar_per_norm[3]*100]

label01 = label_bar_norm[0]
label02 = label_bar_norm[1]
label03 = label_bar_norm[2]
label04 = label_bar_norm[3]

width = 0.5       # the width of the bars: can also be len(x) sequence

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(15, 10),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(labels_bar_dm, value01, width, label=label01,alpha=0.85
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(data_bar_per_exec).shape[0]))[2])
rects2 = ax.bar(labels_bar_dm, value02, width, label=label02,alpha=0.85
                  ,bottom=value01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(data_bar_per_exec).shape[0]))[3])
rects3 = ax.bar(labels_bar_dm, value03, width, label=label03,alpha=0.85
                  ,bottom=[value01[i]+value02[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(data_bar_per_exec).shape[0]))[1])
rects4 = ax.bar(labels_bar_dm, value04, width, label=label04,alpha=0.85
                  ,bottom=[value01[i]+value02[i]+value03[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(data_bar_per_exec).shape[0]))[0])

ax.set_title('흡연자의 하루 평균 흡연량 분포\n\n',fontsize=35)
ax.set_ylabel(
                '(단위: %)' # 표시값
                 ,labelpad=-70 # 여백값 설정
                ,fontsize=20 # 글씨크기 설정
                ,rotation=0 # 회전값 조정
#                 ,ha='center' # 위치조정
                ,loc='top' # 위치조정, ha와 동시에 사용은 불가함.
            )
ax.yaxis.set_tick_params(labelsize=15) # y축 표시값 글씨크기 조정

ax.set_xticklabels(
                   labels_bar_dm
                  , fontsize=20
                  )

# Label with label_type 'center' instead of the default 'edge'
ax.bar_label(rects1, label_type='center',fontsize=18)
ax.bar_label(rects2, label_type='center',fontsize=18)
ax.bar_label(rects3, label_type='center',fontsize=18)
ax.bar_label(rects4, label_type='center',fontsize=18)

plt.text(1.5, 68,  '흡연량 기준', fontsize=25)
lg = ax.legend(bbox_to_anchor=(1.33,0.5),
          ncol=1  ,loc='right' ,fontsize=20
          )
# plt.text(-0.3, -24, '          ', fontsize=17)
# plt.text(-0.3, -27, '          ', fontsize=17)
# plt.text(-0.3, -30, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/03_01흡연력_02흡연자의흡연량분포.png".format(workdir)
            , dpi=175
            ,bbox_extra_artists=(lg,)
            # ,bbox_inches='tight'
            )

plt.show()

#%%
with pd.ExcelWriter('{}/health_status_TABLE.xlsx'.format(workdir), mode='a',engine='openpyxl') as writer:
    smoke_agegrp.to_excel(writer,sheet_name="03_01흡연력")
# %%
