#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib import font_manager,rc  #한글 폰트 입력을 위한 라이브러리

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
GRP = 'CACT'

data.loc[ data['CACT_SCORE'] == 0                            ,'CACT'] = '01_No calcification(AJ-130 score = 0)'
data.loc[(data['CACT_SCORE'] > 0)    & (data['CACT_SCORE'] < 10) ,'CACT'] = '02_Minimal calcification(AJ-130 score 1 ~ 9)'
data.loc[(data['CACT_SCORE'] >= 10)  & (data['CACT_SCORE'] < 100),'CACT'] = '03_Mild calcification(AJ-130 score 10~99)'
data.loc[(data['CACT_SCORE'] >= 100) & (data['CACT_SCORE'] < 400),'CACT'] = '04_Moderate calcification(AJ-130 score 100 ~ 399)'
data.loc[ data['CACT_SCORE'] >= 400                          ,'CACT'] = '05_Severe calcification(AJ-130 score 400 ~)'

data.loc[data['CACT_SCORE'] != 0, 'CAL'] = '01_Cal'
data['CAL'].fillna('02_No',inplace=True)# data.loc[data['CACT_SCORE'] == 0, 'CAL'] = '02_No'

data.loc[ data['AGE'] < 45                      ,'AGEGRP'] = '40~44세'
data.loc[(data['AGE'] > 44) & (data['AGE'] < 50),'AGEGRP'] = '45~49세'
data.loc[(data['AGE'] > 49) & (data['AGE'] < 55),'AGEGRP'] = '50~54세'
data.loc[(data['AGE'] > 54) & (data['AGE'] < 60),'AGEGRP'] = '55~59세'
data.loc[ data['AGE'] > 59                      ,'AGEGRP'] = '60세 이상'
# # data.head(100)
data

# #%%
# data.to_excel("{}/cact.xlsx".format(workdir))
#%%
data_exec = data.drop(data.loc[data['GRP']=='정규일반'].index)
data_norm = data.drop(data.loc[data['GRP']=='임원'].index)

#%%
## pivot table create executive
cact_cnt_exec = data_exec.pivot_table(
                             index=[GRP,'GRP']
                            ,columns=['AGEGRP']
    ,values=['CDW']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
# each column total value percentile
cact_per_exec = round(cact_cnt_exec.div(cact_cnt_exec.iloc[-1], axis=1).astype(float)*100,1)

# cact_per_m

cact_agegrp_exec = pd.DataFrame()

for i in range(len(cact_cnt_exec.columns)):
    if i == 0:
        cact_agegrp_exec = pd.concat(
                                [
                                 cact_cnt_exec.iloc[:,i]
                                ,cact_per_exec.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        cact_agegrp_exec = pd.concat(
                                [
                                 cact_agegrp_exec
                                ,cact_cnt_exec.iloc[:,i]
                                ,cact_per_exec.iloc[:,i]
                                ]
                            ,axis=1
        )
        
cact_agegrp_exec

#%%
## pivot table create normal
cact_cnt_norm = data_norm.pivot_table(
                             index=[GRP,'GRP']
                            ,columns=['AGEGRP']
    ,values=['CDW']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
# each column total value percentile
cact_per_norm = round(cact_cnt_norm.div(cact_cnt_norm.iloc[-1], axis=1).astype(float)*100,1)

# cact_per_m

cact_agegrp_norm = pd.DataFrame()

for i in range(len(cact_cnt_norm.columns)):
    if i == 0:
        cact_agegrp_norm = pd.concat(
                                [
                                 cact_cnt_norm.iloc[:,i]
                                ,cact_per_norm.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        cact_agegrp_norm = pd.concat(
                                [
                                 cact_agegrp_norm
                                ,cact_cnt_norm.iloc[:,i]
                                ,cact_per_norm.iloc[:,i]
                                ]
                            ,axis=1
        )
        
cact_agegrp_norm

#%%
cact_agegrp = pd.concat([cact_agegrp_exec.iloc[:-1,:], cact_agegrp_norm.iloc[:-1,:]],axis=0)

cact_agegrp.columns = pd.MultiIndex.from_tuples(
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
cact_agegrp = cact_agegrp.sort_index()

labels = []
for i in range(len(cact_per_exec.columns)-1):
    labels.append(cact_per_exec.columns[i][1])
    
cact_agegrp
# %%
labels_bar_dm =['임원','정규일반']

# Bar chart create
value01 = [cact_per_exec.iloc[0,-1],cact_per_norm.iloc[0,-1]]
value02 = [cact_per_exec.iloc[1,-1],cact_per_norm.iloc[1,-1]]
value03 = [cact_per_exec.iloc[2,-1],cact_per_norm.iloc[2,-1]]
value04 = [cact_per_exec.iloc[3,-1],cact_per_norm.iloc[3,-1]]
value05 = [cact_per_exec.iloc[4,-1],cact_per_norm.iloc[4,-1]]

label01 = 'No: AJ-130 = 0'
label02 = 'Minimal: AJ-130 1 ~ 9'
label03 = 'Mild: AJ-130 10 ~ 99'
label04 = 'Moderate: AJ-130 100 ~ 399'
label05 = 'Severe: AJ-130 400 ~'

width = 0.5       # the width of the bars: can also be len(x) sequence

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(15, 10),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(labels_bar_dm, value01, width, label=label01,alpha=0.85
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(cact_agegrp_exec).shape[0]))[5])
rects2 = ax.bar(labels_bar_dm, value02, width, label=label02,alpha=0.85
                  ,bottom=value01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(cact_agegrp_exec).shape[0]))[4])
rects3 = ax.bar(labels_bar_dm, value03, width, label=label03,alpha=0.85
                  ,bottom=[value01[i]+value02[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(cact_agegrp_exec).shape[0]))[2])
rects4 = ax.bar(labels_bar_dm, value04, width, label=label04,alpha=0.85
                  ,bottom=[value01[i]+value02[i]+value03[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(cact_agegrp_exec).shape[0]))[1])
rects5 = ax.bar(labels_bar_dm, value05, width, label=label05,alpha=0.85
                  ,bottom=[value01[i]+value02[i]+value03[i]+value04[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(cact_agegrp_exec).shape[0]))[0])

ax.set_title('그룹별 관상동맥 칼슘화 분포\n\n',fontsize=30)
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
                  , fontsize=17
                  )

# Label with label_type 'center' instead of the default 'edge'
ax.bar_label(rects1, label_type='center',fontsize=16)
ax.bar_label(rects2, label_type='center',fontsize=16)
ax.bar_label(rects3, label_type='center',fontsize=16)
ax.bar_label(rects4, label_type='center',fontsize=16)
ax.bar_label(rects5, label_type='center',fontsize=16)

plt.text(1.43, 75,  '관상동맥 칼슘화 분류 기준', fontsize=22)
lg = ax.legend(bbox_to_anchor=(1.06,0.45)
          ,ncol=1  ,loc='lower left' ,fontsize=15
          )
# plt.text(-0.3, -24, '          ', fontsize=17)
# plt.text(-0.3, -27, '          ', fontsize=17)
# plt.text(-0.3, -30, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/02_06CaCT_01그룹별CaCT분포.png".format(workdir)
            , dpi=175
            ,bbox_extra_artists=(lg,)
            # ,bbox_inches='tight'
            )

plt.show()
# %%
with pd.ExcelWriter('{}/health_status_TABLE.xlsx'.format(workdir), mode='a',engine='openpyxl') as writer:
    cact_agegrp.to_excel(writer,sheet_name="02_06관상동맥칼슘화")
# %%
