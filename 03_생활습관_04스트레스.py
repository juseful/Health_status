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
GRP = 'STRESS'
data.loc[(data['STRESS_SCORE'] > 8 ) & (data['STRESS_SCORE'] < 27), GRP] = '잠재적 스트레스군'
data.loc[(data['STRESS_SCORE'] >= 27), GRP] = '고위험 스트레스군'
data['STRESS'].fillna('건강군',inplace=True)

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
stress_cnt_exec = data_exec.pivot_table(
                             index=[GRP,'GRP']
                            ,columns=['AGEGRP']
    ,values=['CDW']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
# each column total value percentile
stress_per_exec = round(stress_cnt_exec.div(stress_cnt_exec.iloc[-1], axis=1).astype(float)*100,1)

# stress_per_m

stress_agegrp_exec = pd.DataFrame()

for i in range(len(stress_cnt_exec.columns)):
    if i == 0:
        stress_agegrp_exec = pd.concat(
                                [
                                 stress_cnt_exec.iloc[:,i]
                                ,stress_per_exec.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        stress_agegrp_exec = pd.concat(
                                [
                                 stress_agegrp_exec
                                ,stress_cnt_exec.iloc[:,i]
                                ,stress_per_exec.iloc[:,i]
                                ]
                            ,axis=1
        )
        
stress_agegrp_exec

#%%
## pivot table create normal
stress_cnt_norm = data_norm.pivot_table(
                             index=[GRP,'GRP']
                            ,columns=['AGEGRP']
    ,values=['CDW']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
# each column total value percentile
stress_per_norm = round(stress_cnt_norm.div(stress_cnt_norm.iloc[-1], axis=1).astype(float)*100,1)

# stress_per_m

stress_agegrp_norm = pd.DataFrame()

for i in range(len(stress_cnt_norm.columns)):
    if i == 0:
        stress_agegrp_norm = pd.concat(
                                [
                                 stress_cnt_norm.iloc[:,i]
                                ,stress_per_norm.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        stress_agegrp_norm = pd.concat(
                                [
                                 stress_agegrp_norm
                                ,stress_cnt_norm.iloc[:,i]
                                ,stress_per_norm.iloc[:,i]
                                ]
                            ,axis=1
        )
        
stress_agegrp_norm

#%%
stress_agegrp = pd.concat([stress_agegrp_exec.iloc[:-1,:], stress_agegrp_norm.iloc[:-1,:]],axis=0)

stress_agegrp.columns = pd.MultiIndex.from_tuples(
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
stress_agegrp = stress_agegrp.sort_index()

labels = []
for i in range(len(stress_per_exec.columns)-1):
    labels.append(stress_per_exec.columns[i][1])
    
stress_agegrp

#%%
# with pd.ExcelWriter('{}/health_status_TABLE.xlsx'.format(workdir), mode='a',engine='openpyxl') as writer:
#     stress_agegrp.to_excel(writer,sheet_name="02_02당뇨병유병율")

#%%
stress_grp_exec = data_exec.pivot_table(
                          columns=['STRESS']
                         ,values=['CDW']
                         ,aggfunc='count'
)

# stress_grp

label_pie_exec = stress_grp_exec.columns.to_list()
label_pie_exec

data_pie_exec = stress_grp_exec.iloc[0,:].to_list()
data_pie_exec

stress_grp_norm = data_norm.pivot_table(
                          columns=['STRESS']
                         ,values=['CDW']
                         ,aggfunc='count'
)

# stress_grp

label_pie_norm = stress_grp_norm.columns.to_list()
label_pie_norm

data_pie_norm = stress_grp_norm.iloc[0,:].to_list()
data_pie_norm
# #%%
# # data_pie_exec
# label_pie_exec

#%%
fig, ax = plt.subplots(linewidth=2)

plt.figure(figsize=(15,10))
# fig, ax = plt.subplots(figsize=(20,10 ), subplot_kw=dict(aspect="equal"),linewidth=2)
fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정

ax.set_title("그룹별 스트레스군 비교\n\n",fontsize=50,y=2.2)

out_category = data_pie_exec
in_category = data_pie_norm
out_labels = label_pie_exec
in_labels = label_pie_norm
# explode = [0.1,0.1, 0,0,0,0,0,0,0,0,0]

out_cmap = plt.get_cmap("tab20")
in_cmap = plt.get_cmap("Pastel1")

outer_colors = out_cmap(np.array([2,1,0]))
inner_colors = in_cmap(np.array([0,1,2]))

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
       pctdistance=0.75, labeldistance=0.45,
     wedgeprops=dict(width=2, edgecolor='w'), textprops={'fontsize': 30}, autopct="%.f%%")

for t in ts:
    t.set_color('black')
for autotext in at:
    autotext.set_color('black')
ax.text(-7.5, -5.5,  '  ', fontsize=22)
ax.text(-6, -5.2,  '* 건강군: 스트레스 총점이 8점 이하', fontsize=25)
ax.text(-6, -5.5,  '* 잠재적 스트레스군: 스트레스 총점이 9~26점', fontsize=25)
ax.text(-6, -5.8,  '* 고위험 스트레스군: 스트레스 총점이 27점 이상', fontsize=25)
ax.text(4.2, -5.5,  '□ 외측: 임원', fontsize=30)
ax.text(4.2, -6,  '□ 내측: 정규일반', fontsize=30)

fig.tight_layout()
plt.savefig("{}/03_04스트레스_01분포.png".format(workdir)
           , dpi=175)

plt.show()

#%%
with pd.ExcelWriter('{}/health_status_TABLE.xlsx'.format(workdir), mode='a',engine='openpyxl') as writer:
    stress_agegrp.to_excel(writer,sheet_name="03_04스트레스")
# %%
