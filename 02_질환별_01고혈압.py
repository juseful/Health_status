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
GRP = 'BP'
data.loc[(data['SM0600SBP'] < 120) & (data['SM0600DBP'] < 80) & (data['TRT_MED_HYPERTENSION'] != '1'), GRP] = '03_OPTIMAL'
data.loc[(data['SM0600SBP'] >= 140) | (data['SM0600DBP'] >= 90) | (data['TRT_MED_HYPERTENSION'] == '1'), GRP] = '01_고혈압'
data['BP'].fillna('02_고혈압전단계',inplace=True)

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
bp_cnt_exec = data_exec.pivot_table(
                             index=[GRP,'GRP']
                            ,columns=['AGEGRP']
    ,values=['CDW']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
# each column total value percentile
bp_per_exec = round(bp_cnt_exec.div(bp_cnt_exec.iloc[-1], axis=1).astype(float)*100,1)

# bp_per_m

bp_agegrp_exec = pd.DataFrame()

for i in range(len(bp_cnt_exec.columns)):
    if i == 0:
        bp_agegrp_exec = pd.concat(
                                [
                                 bp_cnt_exec.iloc[:,i]
                                ,bp_per_exec.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        bp_agegrp_exec = pd.concat(
                                [
                                 bp_agegrp_exec
                                ,bp_cnt_exec.iloc[:,i]
                                ,bp_per_exec.iloc[:,i]
                                ]
                            ,axis=1
        )
        
bp_agegrp_exec

#%%
## pivot table create normal
bp_cnt_norm = data_norm.pivot_table(
                             index=[GRP,'GRP']
                            ,columns=['AGEGRP']
    ,values=['CDW']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
# each column total value percentile
bp_per_norm = round(bp_cnt_norm.div(bp_cnt_norm.iloc[-1], axis=1).astype(float)*100,1)

# bp_per_m

bp_agegrp_norm = pd.DataFrame()

for i in range(len(bp_cnt_norm.columns)):
    if i == 0:
        bp_agegrp_norm = pd.concat(
                                [
                                 bp_cnt_norm.iloc[:,i]
                                ,bp_per_norm.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        bp_agegrp_norm = pd.concat(
                                [
                                 bp_agegrp_norm
                                ,bp_cnt_norm.iloc[:,i]
                                ,bp_per_norm.iloc[:,i]
                                ]
                            ,axis=1
        )
        
bp_agegrp_norm

#%%
bp_agegrp = pd.concat([bp_agegrp_exec.iloc[:-1,:], bp_agegrp_norm.iloc[:-1,:]],axis=0)

bp_agegrp.columns = pd.MultiIndex.from_tuples(
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
bp_agegrp = bp_agegrp.sort_index()

labels = []
for i in range(len(bp_per_exec.columns)-1):
    labels.append(bp_per_exec.columns[i][1])
    
bp_agegrp

#%%
value01 = bp_per_exec.iloc[0,:-1]
value02 = bp_per_norm.iloc[0,:-1]

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.35  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(15, 10),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(x - 0.2, value01, width, label='임원',color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.85,np.array(bp_per_exec.iloc[0,:-1]).shape[0]))[4])
rects2 = ax.bar(x + 0.2, value02, width, label='정규일반',color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.85,np.array(bp_per_exec.iloc[0,:-1]).shape[0]))[1])

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('연령별 고혈압 유병율(22~23년)\n\n',fontsize=30)
ax.set_ylabel(
                '(단위: %)' # 표시값
                 ,labelpad=-70 # 여백값 설정
                ,fontsize=20 # 글씨크기 설정
                ,rotation=0 # 회전값 조정
#                 ,ha='center' # 위치조정
                ,loc='top' # 위치조정, ha와 동시에 사용은 불가함.
            )
ax.yaxis.set_tick_params(labelsize=15) # y축 표시값 글씨크기 조정
ax.set_xticks(x)
ax.set_xticklabels(
                   labels[0:len(labels)] # all 값이 list에는 포함되지 않았기 때문임.
                  , fontsize=17
                  )
ax.legend(fontsize=17,loc='best')

# bar위에 값 label 표시
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate(height, 
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 8),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom'
                   ,fontsize=18
                   )

autolabel(rects1)
autolabel(rects2)

fig.tight_layout()

plt.savefig("{}/02_01고혈압_01유병율.png".format(workdir)
           , dpi=175)

plt.show()

#%%
with pd.ExcelWriter('{}/health_status_TABLE.xlsx'.format(workdir), mode='w',engine='openpyxl') as writer:
    bp_agegrp.to_excel(writer,sheet_name="02_01고혈압유병율")
# %%
