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
GRP = 'BMI'
data.loc[ data['SM316001'] < 18.5                            ,'BMI'] = '01. 저체중(BMI 0~18.4)'
data.loc[(data['SM316001'] >= 18.5) & (data['SM316001'] < 23),'BMI'] = '02. 정상체중(BMI 18.5~22.9)'
data.loc[(data['SM316001'] >= 23.0) & (data['SM316001'] < 25),'BMI'] = '03. 위험체중(BMI 23~24.9)'
data.loc[(data['SM316001'] >= 25.0) & (data['SM316001'] < 30),'BMI'] = '04. 비만1단계(BMI 25~29.9)'
data.loc[(data['SM316001'] >= 30.0) & (data['SM316001'] < 40),'BMI'] = '05. 비만2단계(BMI 30~39.9)'
data.loc[ data['SM316001'] >= 40.0                           ,'BMI'] = '06. 비만3단계(BMI 40~)'

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
obd_cnt_exec = data_exec.pivot_table(
                             index=[GRP,'GRP']
                            ,columns=['AGEGRP']
    ,values=['CDW']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
# each column total value percentile
obd_per_exec = round(obd_cnt_exec.div(obd_cnt_exec.iloc[-1], axis=1).astype(float)*100,1)

# obd_per_m

obd_agegrp_exec = pd.DataFrame()

for i in range(len(obd_cnt_exec.columns)):
    if i == 0:
        obd_agegrp_exec = pd.concat(
                                [
                                 obd_cnt_exec.iloc[:,i]
                                ,obd_per_exec.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        obd_agegrp_exec = pd.concat(
                                [
                                 obd_agegrp_exec
                                ,obd_cnt_exec.iloc[:,i]
                                ,obd_per_exec.iloc[:,i]
                                ]
                            ,axis=1
        )
        
obd_agegrp_exec

#%%
## pivot table create normal
obd_cnt_norm = data_norm.pivot_table(
                             index=[GRP,'GRP']
                            ,columns=['AGEGRP']
    ,values=['CDW']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
# each column total value percentile
obd_per_norm = round(obd_cnt_norm.div(obd_cnt_norm.iloc[-1], axis=1).astype(float)*100,1)

# obd_per_m

obd_agegrp_norm = pd.DataFrame()

for i in range(len(obd_cnt_norm.columns)):
    if i == 0:
        obd_agegrp_norm = pd.concat(
                                [
                                 obd_cnt_norm.iloc[:,i]
                                ,obd_per_norm.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        obd_agegrp_norm = pd.concat(
                                [
                                 obd_agegrp_norm
                                ,obd_cnt_norm.iloc[:,i]
                                ,obd_per_norm.iloc[:,i]
                                ]
                            ,axis=1
        )
        
obd_agegrp_norm

#%%
obd_agegrp = pd.concat([obd_agegrp_exec.iloc[:-1,:], obd_agegrp_norm.iloc[:-1,:]],axis=0)

obd_agegrp.columns = pd.MultiIndex.from_tuples(
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
obd_agegrp = obd_agegrp.sort_index()

labels = []
for i in range(len(obd_per_exec.columns)-1):
    labels.append(obd_per_exec.columns[i][1])
    
obd_agegrp

# %%
labels_bar_dm =['임원','정규일반']

# Bar chart create
value01 = [obd_per_exec.iloc[0,-1],obd_per_norm.iloc[0,-1]]
value02 = [obd_per_exec.iloc[1,-1],obd_per_norm.iloc[1,-1]]
value03 = [obd_per_exec.iloc[2,-1],obd_per_norm.iloc[2,-1]]
value04 = [obd_per_exec.iloc[3,-1],obd_per_norm.iloc[3,-1]]
value05 = [obd_per_exec.iloc[4,-1],obd_per_norm.iloc[4,-1]]
value06 = [0                      ,obd_per_norm.iloc[5,-1]]

label01 = '저체중:     BMI 0~18.4'
label02 = '정상체중:  BMI 18.5~22.9'
label03 = '위험체중:   BMI 23~24.9'
label04 = '비만1단계: BMI 25~29.9'
label05 = '비만2단계: BMI 30~39.9'
label06 = '비만3단계: BMI 40~'

width = 0.5       # the width of the bars: can also be len(x) sequence

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(15, 10),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(labels_bar_dm, value01, width, label=label01,alpha=0.85
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(obd_agegrp_exec).shape[0]))[3])
rects2 = ax.bar(labels_bar_dm, value02, width, label=label02,alpha=0.85
                  ,bottom=value01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(obd_agegrp_exec).shape[0]))[5])
rects3 = ax.bar(labels_bar_dm, value03, width, label=label03,alpha=0.85
                  ,bottom=[value01[i]+value02[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(obd_agegrp_exec).shape[0]))[4])
rects4 = ax.bar(labels_bar_dm, value04, width, label=label04,alpha=0.85
                  ,bottom=[value01[i]+value02[i]+value03[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(obd_agegrp_exec).shape[0]))[2])
rects5 = ax.bar(labels_bar_dm, value05, width, label=label05,alpha=0.85
                  ,bottom=[value01[i]+value02[i]+value03[i]+value04[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(obd_agegrp_exec).shape[0]))[1])
rects6 = ax.bar(labels_bar_dm, value06, width, label=label06,alpha=0.85
                  ,bottom=[value01[i]+value02[i]+value03[i]+value04[i]+value05[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(obd_agegrp_exec).shape[0]))[0])

ax.set_title('그룹별 비만도 분포\n\n',fontsize=30)
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
ax.bar_label(rects6, label_type='center',fontsize=16)

plt.text(1.5, 83,  '비만도 분류 기준', fontsize=22)
lg = ax.legend(bbox_to_anchor=(1.05,0.5)
          ,ncol=1  ,loc='lower left' ,fontsize=15
          )
# plt.text(-0.3, -24, '          ', fontsize=17)
# plt.text(-0.3, -27, '          ', fontsize=17)
# plt.text(-0.3, -30, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/02_04비만도_01그룹별비만도분포.png".format(workdir)
            , dpi=175
            ,bbox_extra_artists=(lg,)
            # ,bbox_inches='tight'
            )

plt.show()
# %%
with pd.ExcelWriter('{}/health_status_TABLE.xlsx'.format(workdir), mode='a',engine='openpyxl') as writer:
    obd_agegrp.to_excel(writer,sheet_name="02_04비만도")
# %%
