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
GRP = 'PHY'
data.loc[(data['OVERALL_PHYSICAL_ACTIVITY'] == '0'), GRP] = '신체활동 없음'
data.loc[(data['OVERALL_PHYSICAL_ACTIVITY'] == '1'), GRP] = '신체활동(강도:3)'
data.loc[(data['OVERALL_PHYSICAL_ACTIVITY'] == '2'), GRP] = '신체활동(강도:2)'
data.loc[(data['OVERALL_PHYSICAL_ACTIVITY'] == '3'), GRP] = '신체활동(강도:1)'

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
PHY_cnt_exec = data_exec.pivot_table(
                             index=[GRP,'GRP']
                            ,columns=['AGEGRP']
    ,values=['CDW']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
# each column total value percentile
PHY_per_exec = round(PHY_cnt_exec.div(PHY_cnt_exec.iloc[-1], axis=1).astype(float)*100,1)

# PHY_per_m

PHY_agegrp_exec = pd.DataFrame()

for i in range(len(PHY_cnt_exec.columns)):
    if i == 0:
        PHY_agegrp_exec = pd.concat(
                                [
                                 PHY_cnt_exec.iloc[:,i]
                                ,PHY_per_exec.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        PHY_agegrp_exec = pd.concat(
                                [
                                 PHY_agegrp_exec
                                ,PHY_cnt_exec.iloc[:,i]
                                ,PHY_per_exec.iloc[:,i]
                                ]
                            ,axis=1
        )
        
PHY_agegrp_exec

#%%
## pivot table create normal
PHY_cnt_norm = data_norm.pivot_table(
                             index=[GRP,'GRP']
                            ,columns=['AGEGRP']
    ,values=['CDW']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
# each column total value percentile
PHY_per_norm = round(PHY_cnt_norm.div(PHY_cnt_norm.iloc[-1], axis=1).astype(float)*100,1)

# PHY_per_m

PHY_agegrp_norm = pd.DataFrame()

for i in range(len(PHY_cnt_norm.columns)):
    if i == 0:
        PHY_agegrp_norm = pd.concat(
                                [
                                 PHY_cnt_norm.iloc[:,i]
                                ,PHY_per_norm.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        PHY_agegrp_norm = pd.concat(
                                [
                                 PHY_agegrp_norm
                                ,PHY_cnt_norm.iloc[:,i]
                                ,PHY_per_norm.iloc[:,i]
                                ]
                            ,axis=1
        )
        
PHY_agegrp_norm

#%%
PHY_agegrp = pd.concat([PHY_agegrp_exec.iloc[:-1,:], PHY_agegrp_norm.iloc[:-1,:]],axis=0)

PHY_agegrp.columns = pd.MultiIndex.from_tuples(
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
PHY_agegrp = PHY_agegrp.sort_index()

labels = []
for i in range(len(PHY_per_exec.columns)-1):
    labels.append(PHY_per_exec.columns[i][1])
    
PHY_agegrp

#%%
PHY_grp_exec = data_exec.pivot_table(
                          columns=['PHY']
                         ,values=['CDW']
                         ,aggfunc='count'
)

# PHY_grp

label_pie_exec = PHY_grp_exec.columns.to_list()
label_pie_exec

data_pie_exec = PHY_grp_exec.iloc[0,:].to_list()
data_pie_exec

PHY_grp_norm = data_norm.pivot_table(
                          columns=['PHY']
                         ,values=['CDW']
                         ,aggfunc='count'
)

# PHY_grp

label_pie_norm = PHY_grp_norm.columns.to_list()
label_pie_norm

data_pie_norm = PHY_grp_norm.iloc[0,:].to_list()
data_pie_norm
#%%
fig, ax = plt.subplots(linewidth=2)

plt.figure(figsize=(15,10))
# fig, ax = plt.subplots(figsize=(20,10 ), subplot_kw=dict(aspect="equal"),linewidth=2)
fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정

ax.set_title("그룹별 신체활동 분포\n\n",fontsize=50,y=2.2)

out_category = data_pie_exec
in_category = data_pie_norm
out_labels = ['활동없음','약강도','중강도','고강도']#label_pie_exec
in_labels = ['활동없음','약강도','중강도','고강도']#label_pie_norm
# explode = [0.1,0.1, 0,0,0,0,0,0,0,0,0]

out_cmap = plt.get_cmap("tab20")
in_cmap = plt.get_cmap("Pastel1")

outer_colors = out_cmap(np.array([1,0,2,3]))
inner_colors = in_cmap(np.array([1,2,0,3]))

w, ts, at = ax.pie(out_category, radius=5, colors=outer_colors,labels=out_labels,
                #    explode = explode,
        rotatelabels =False, startangle=90,counterclock=False,
       pctdistance=0.75, labeldistance=0.87,
       wedgeprops=dict(width=1.5, edgecolor='w'),textprops={'fontsize': 30}, autopct="%1.1f%%")

for t in ts:
    t.set_color('black')
for autotext in at:
    autotext.set_color('black')

w, ts, at = ax.pie(in_category, radius= 3, colors=inner_colors,labels=in_labels,
       rotatelabels =False, startangle=90,counterclock=False,
       pctdistance=0.78, labeldistance=0.3,
     wedgeprops=dict(width=2, edgecolor='w'), textprops={'fontsize': 30}, autopct="%.f%%")

for t in ts:
    t.set_color('black')
for autotext in at:
    autotext.set_color('black')
ax.text(-7.5, -5.5,  '  ', fontsize=22)
ax.text(-6, -5.2,  '* 약강도: 걷기, 골프 등', fontsize=25)
ax.text(-6, -5.5,  '* 중강도: 속보, 테니스, 수영 등', fontsize=25)
ax.text(-6, -5.8,  '* 고강도: 에어로빅, 조깅 등', fontsize=25)
ax.text(4.2, -5.5,  '□ 외측: 임원', fontsize=30)
ax.text(4.2, -6,  '□ 내측: 정규일반', fontsize=30)

fig.tight_layout()
plt.savefig("{}/03_03운동습관_01분포.png".format(workdir)
           , dpi=175)

plt.show()
#%%
data_exec.loc[(data_exec['PHY']!='신체활동 없음') & (data_exec['PHY_FREQ'] == '1'),'PHY_FREQ_GRP'] = '주 1~2일'
data_exec.loc[(data_exec['PHY']!='신체활동 없음') & (data_exec['PHY_FREQ'] == '2'),'PHY_FREQ_GRP'] = '주 3~4일'
data_exec.loc[(data_exec['PHY']!='신체활동 없음') & (data_exec['PHY_FREQ'] == '3'),'PHY_FREQ_GRP'] = '주 5일 이상'

# data

PHY_FREQ_cat_exec = data_exec.pivot_table(
                              columns=['PHY_FREQ_GRP']
                             ,values=['CDW'] 
                             ,aggfunc='count'
                             )
PHY_FREQ_cat_exec

data_bar_exec = PHY_FREQ_cat_exec.iloc[0,:].to_list()
data_bar_exec
data_bar_total_exec = data_bar_exec[0]+data_bar_exec[1]+data_bar_exec[2]
data_bar_total_exec

data_bar_per_exec = []

for i in range(len(data_bar_exec)):
    data_bar_per_exec.append(round(data_bar_exec[i]/data_bar_total_exec,3))

data_bar_per_exec

label_bar_exec = ['주 1~2일'
            ,'주 3~4일'
            ,'주 5일이상'
            ]

label_bar_exec

data_norm.loc[(data_norm['PHY']!='신체활동 없음') & (data_norm['PHY_FREQ'] == '1'),'PHY_FREQ_GRP'] = '주 1~2일'
data_norm.loc[(data_norm['PHY']!='신체활동 없음') & (data_norm['PHY_FREQ'] == '2'),'PHY_FREQ_GRP'] = '주 3~4일'
data_norm.loc[(data_norm['PHY']!='신체활동 없음') & (data_norm['PHY_FREQ'] == '3'),'PHY_FREQ_GRP'] = '주 5일 이상'

# data

PHY_FREQ_cat_norm = data_norm.pivot_table(
                              columns=['PHY_FREQ_GRP']
                             ,values=['CDW'] 
                             ,aggfunc='count'
                             )
PHY_FREQ_cat_norm

data_bar_norm = PHY_FREQ_cat_norm.iloc[0,:].to_list()
data_bar_norm
data_bar_total_norm = data_bar_norm[0]+data_bar_norm[1]+data_bar_norm[2]
data_bar_total_norm

data_bar_per_norm = []

for i in range(len(data_bar_norm)):
    data_bar_per_norm.append(round(data_bar_norm[i]/data_bar_total_norm,3))

data_bar_per_norm

label_bar_norm = ['주 1~2일'
            ,'주 3~4일'
            ,'주 5일이상'
            ]

label_bar_norm

# %%
labels_bar_dm =['임원','정규일반']

# Bar chart create
value01 = [data_bar_per_exec[0]*100,data_bar_per_norm[0]*100]
value02 = [data_bar_per_exec[1]*100,data_bar_per_norm[1]*100]
value03 = [data_bar_per_exec[2]*100,data_bar_per_norm[2]*100]

label01 = label_bar_norm[0]
label02 = label_bar_norm[1]
label03 = label_bar_norm[2]

width = 0.5       # the width of the bars: can also be len(x) sequence

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(15, 10),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(labels_bar_dm, value01, width, label=label01,alpha=0.85
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(data_bar_per_exec).shape[0]))[1])
rects2 = ax.bar(labels_bar_dm, value02, width, label=label02,alpha=0.85
                  ,bottom=value01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(data_bar_per_exec).shape[0]))[2])
rects3 = ax.bar(labels_bar_dm, value03, width, label=label03,alpha=0.85
                  ,bottom=[value01[i]+value02[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(data_bar_per_exec).shape[0]))[0])

ax.set_title('평균 운동횟수 분포\n\n',fontsize=35)
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

plt.text(1.47, 65,  '운동횟수 기준', fontsize=25)
lg = ax.legend(bbox_to_anchor=(1.33,0.5),
          ncol=1  ,loc='right' ,fontsize=20
          )
# plt.text(-0.3, -24, '          ', fontsize=17)
# plt.text(-0.3, -27, '          ', fontsize=17)
# plt.text(-0.3, -30, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/03_03운동습관_02운동횟수.png".format(workdir)
            , dpi=175
            ,bbox_extra_artists=(lg,)
            # ,bbox_inches='tight'
            )

plt.show()
#%%
data_exec.loc[(data_exec['PHY']!='신체활동 없음') & (data_exec['PHY_DURATION'] == '1'),'PHY_HOUR'] = '20분 이하'
# 문진응답내역에서 null 값은 중간값 처리
data_exec.loc[(data_exec['PHY']!='신체활동 없음') & (data_exec['PHY_DURATION'] == '2'),'PHY_HOUR']  = '20~40분'
data_exec.loc[(data_exec['PHY']!='신체활동 없음') & (data_exec['PHY_DURATION'] == '3'),'PHY_HOUR'] = '40~60분'
data_exec.loc[(data_exec['PHY']!='신체활동 없음') & (data_exec['PHY_DURATION'] == '4'),'PHY_HOUR'] = '60분 이상'

# data

PHY_AMT_cat_exec = data_exec.pivot_table(
                              columns=['PHY_HOUR']
                             ,values=['CDW'] 
                             ,aggfunc='count'
                             )
PHY_AMT_cat_exec

PHY_AMT_data_bar_exec = PHY_AMT_cat_exec.iloc[0,:].to_list()
PHY_AMT_data_bar_exec
PHY_AMT_data_bar_total_exec = PHY_AMT_data_bar_exec[0]+PHY_AMT_data_bar_exec[1]+PHY_AMT_data_bar_exec[2]+PHY_AMT_data_bar_exec[3]

PHY_AMT_data_bar_per_exec = []

for i in range(len(PHY_AMT_data_bar_exec)):
    PHY_AMT_data_bar_per_exec.append(round(PHY_AMT_data_bar_exec[i]/PHY_AMT_data_bar_total_exec,3))

PHY_AMT_data_bar_per_exec

PHY_AMT_label_bar_exec = ['20분 이하'
            ,'20~40분'
            ,'40~60분'
            ,'60분 이상'
            ]

PHY_AMT_label_bar_exec

data_norm.loc[(data_norm['PHY']!='신체활동 없음') & (data_norm['PHY_DURATION'] == '1'),'PHY_HOUR'] = '20분 이하'
# 문진응답내역에서 null 값은 중간값 처리
data_norm.loc[(data_norm['PHY']!='신체활동 없음') & (data_norm['PHY_DURATION'] == '2'),'PHY_HOUR']  = '20~40분'
data_norm.loc[(data_norm['PHY']!='신체활동 없음') & (data_norm['PHY_DURATION'] == '3'),'PHY_HOUR'] = '40~60분'
data_norm.loc[(data_norm['PHY']!='신체활동 없음') & (data_norm['PHY_DURATION'] == '4'),'PHY_HOUR'] = '60분 이상'

# data

PHY_AMT_cat_norm = data_norm.pivot_table(
                              columns=['PHY_HOUR']
                             ,values=['CDW'] 
                             ,aggfunc='count'
                             )
PHY_AMT_cat_norm

PHY_AMT_data_bar_norm = PHY_AMT_cat_norm.iloc[0,:].to_list()
PHY_AMT_data_bar_norm
PHY_AMT_data_bar_total_norm = PHY_AMT_data_bar_norm[0]+PHY_AMT_data_bar_norm[1]+PHY_AMT_data_bar_norm[2]+PHY_AMT_data_bar_norm[3]

PHY_AMT_data_bar_per_norm = []

for i in range(len(PHY_AMT_data_bar_norm)):
    PHY_AMT_data_bar_per_norm.append(round(PHY_AMT_data_bar_norm[i]/PHY_AMT_data_bar_total_norm,3))

PHY_AMT_data_bar_per_norm

PHY_AMT_label_bar_norm = ['20분 이하'
            ,'20~40분'
            ,'40~60분'
            ,'60분 이상'
            ]

PHY_AMT_label_bar_norm

# %%
labels_bar_dm =['임원','정규일반']

# Bar chart create
value01 = [PHY_AMT_data_bar_per_exec[0]*100,PHY_AMT_data_bar_per_norm[0]*100]
value02 = [PHY_AMT_data_bar_per_exec[1]*100,PHY_AMT_data_bar_per_norm[1]*100]
value03 = [PHY_AMT_data_bar_per_exec[2]*100,PHY_AMT_data_bar_per_norm[2]*100]
value04 = [PHY_AMT_data_bar_per_exec[3]*100,PHY_AMT_data_bar_per_norm[3]*100]

label01 = PHY_AMT_label_bar_norm[0]
label02 = PHY_AMT_label_bar_norm[1]
label03 = PHY_AMT_label_bar_norm[2]
label04 = PHY_AMT_label_bar_norm[3]

width = 0.5       # the width of the bars: can also be len(x) sequence

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(15, 10),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(labels_bar_dm, value01, width, label=label01,alpha=0.85
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(PHY_AMT_data_bar_per_norm).shape[0]))[2])
rects2 = ax.bar(labels_bar_dm, value02, width, label=label02,alpha=0.85
                  ,bottom=value01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(PHY_AMT_data_bar_per_norm).shape[0]))[3])
rects3 = ax.bar(labels_bar_dm, value03, width, label=label03,alpha=0.85
                  ,bottom=[value01[i]+value02[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(PHY_AMT_data_bar_per_norm).shape[0]))[1])
rects4 = ax.bar(labels_bar_dm, value04, width, label=label04,alpha=0.85
                  ,bottom=[value01[i]+value02[i]+value03[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(PHY_AMT_data_bar_per_norm).shape[0]))[0])

ax.set_title('평균 운동시간 분포\n\n',fontsize=35)
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

plt.text(1.47, 68,  '운동시간 기준', fontsize=25)
lg = ax.legend(bbox_to_anchor=(1.32,0.5),
          ncol=1  ,loc='right' ,fontsize=20
          )
# plt.text(-0.3, -24, '          ', fontsize=17)
# plt.text(-0.3, -27, '          ', fontsize=17)
# plt.text(-0.3, -30, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/03_03운동습관_03운동시간.png".format(workdir)
            , dpi=175
            ,bbox_extra_artists=(lg,)
            # ,bbox_inches='tight'
            )

plt.show()
#%%
with pd.ExcelWriter('{}/health_status_TABLE.xlsx'.format(workdir), mode='a',engine='openpyxl') as writer:
    PHY_agegrp.to_excel(writer,sheet_name="03_03운동습관")

# %%
