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
GRP = 'DM'
data.loc[(data['BL3118'] < 100) & (data['BL3164'] < 5.7) & (data['TRT_MED_DIABETES'] != '1'), GRP] = '정상'
data.loc[(data['BL3118'] >= 126) | (data['BL3164'] >= 6.5) | (data['TRT_MED_DIABETES'] == '1'), GRP] = '당뇨병'
data['DM'].fillna('전당뇨',inplace=True)

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
dm_cnt_exec = data_exec.pivot_table(
                             index=[GRP,'GRP']
                            ,columns=['AGEGRP']
    ,values=['CDW']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
# each column total value percentile
dm_per_exec = round(dm_cnt_exec.div(dm_cnt_exec.iloc[-1], axis=1).astype(float)*100,1)

# dm_per_m

dm_agegrp_exec = pd.DataFrame()

for i in range(len(dm_cnt_exec.columns)):
    if i == 0:
        dm_agegrp_exec = pd.concat(
                                [
                                 dm_cnt_exec.iloc[:,i]
                                ,dm_per_exec.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        dm_agegrp_exec = pd.concat(
                                [
                                 dm_agegrp_exec
                                ,dm_cnt_exec.iloc[:,i]
                                ,dm_per_exec.iloc[:,i]
                                ]
                            ,axis=1
        )
        
dm_agegrp_exec

#%%
## pivot table create normal
dm_cnt_norm = data_norm.pivot_table(
                             index=[GRP,'GRP']
                            ,columns=['AGEGRP']
    ,values=['CDW']
    ,aggfunc='count'
    ,margins=True
    ,fill_value=0
                            )
# each column total value percentile
dm_per_norm = round(dm_cnt_norm.div(dm_cnt_norm.iloc[-1], axis=1).astype(float)*100,1)

# dm_per_m

dm_agegrp_norm = pd.DataFrame()

for i in range(len(dm_cnt_norm.columns)):
    if i == 0:
        dm_agegrp_norm = pd.concat(
                                [
                                 dm_cnt_norm.iloc[:,i]
                                ,dm_per_norm.iloc[:,i]
                                ]
                            ,axis=1
        )
    else:
        dm_agegrp_norm = pd.concat(
                                [
                                 dm_agegrp_norm
                                ,dm_cnt_norm.iloc[:,i]
                                ,dm_per_norm.iloc[:,i]
                                ]
                            ,axis=1
        )
        
dm_agegrp_norm

#%%
dm_agegrp = pd.concat([dm_agegrp_exec.iloc[:-1,:], dm_agegrp_norm.iloc[:-1,:]],axis=0)

dm_agegrp.columns = pd.MultiIndex.from_tuples(
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
dm_agegrp = dm_agegrp.sort_index()

labels = []
for i in range(len(dm_per_exec.columns)-1):
    labels.append(dm_per_exec.columns[i][1])
    
dm_agegrp

#%%
value01 = dm_per_exec.iloc[0,:-1]
value02 = dm_per_norm.iloc[0,:-1]

x = np.arange(len(labels))  # the label locations # all 값이 list에는 포함되지 않았기 때문임.
width = 0.35  # the width of the bars

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(15, 10),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(x - 0.2, value01, width, label='임원',color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.85,np.array(dm_per_exec.iloc[0,:-1]).shape[0]))[4])
rects2 = ax.bar(x + 0.2, value02, width, label='정규일반',color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.85,np.array(dm_per_exec.iloc[0,:-1]).shape[0]))[1])

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_title('연령별 당뇨병 유병율(22~23년)\n\n',fontsize=30)
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

plt.savefig("{}/02_02당뇨병_01유병율.png".format(workdir)
           , dpi=175)

plt.show()

#%%
with pd.ExcelWriter('{}/health_status_TABLE.xlsx'.format(workdir), mode='a',engine='openpyxl') as writer:
    dm_agegrp.to_excel(writer,sheet_name="02_02당뇨병유병율")

#%%
dm_grp_exec = data_exec.pivot_table(
                          columns=['DM']
                         ,values=['CDW']
                         ,aggfunc='count'
)

# dm_grp

label_pie_exec = dm_grp_exec.columns.to_list()
label_pie_exec

data_pie_exec = dm_grp_exec.iloc[0,:].to_list()
data_pie_exec

data_exec.loc[(data_exec['DM']=='당뇨병') & (data_exec['BL3164'] < 6.5)                          ,'DM_HbA1c'] = '01_~6.4'
data_exec.loc[(data_exec['DM']=='당뇨병') & (data_exec['BL3164'] > 6.4) & (data_exec['BL3164'] <  7.0),'DM_HbA1c'] = '02_6.5~6.9'
data_exec.loc[(data_exec['DM']=='당뇨병') & (data_exec['BL3164'] > 6.9) & (data_exec['BL3164'] <  8.0),'DM_HbA1c'] = '03_7.0~7.9'
data_exec.loc[(data_exec['DM']=='당뇨병') & (data_exec['BL3164'] > 7.9) & (data_exec['BL3164'] <  9.0),'DM_HbA1c'] = '04_8.0~8.9'
data_exec.loc[(data_exec['DM']=='당뇨병') & (data_exec['BL3164'] > 8.9) & (data_exec['BL3164'] < 10.0),'DM_HbA1c'] = '05_9.0~9.9'
data_exec.loc[(data_exec['DM']=='당뇨병') & (data_exec['BL3164'] > 9.9)                          ,'DM_HbA1c'] = '06_10.0~'

# data

DM_HbA1c_cat_exec = data_exec.pivot_table(
                              columns=['DM_HbA1c']
                             ,values=['CDW'] 
                             ,aggfunc='count'
                             )
DM_HbA1c_cat_exec

data_bar_exec = DM_HbA1c_cat_exec.iloc[0,:].to_list()
data_bar_exec

data_bar_per_exec = []

for i in range(len(data_bar_exec)):
    data_bar_per_exec.append(round(data_bar_exec[i]/data_pie_exec[0],3))

data_bar_per_exec

label_bar_exec = ['6.4% 이하'
            ,'6.5%~6.9%'
            ,'7.0%~7.9%'
            ,'8.0%~8.9%'
            ,'9.0%~9.9%'
            ,'10.0% 이상'
            ]

label_bar_exec

dm_grp_norm = data_norm.pivot_table(
                          columns=['DM']
                         ,values=['CDW']
                         ,aggfunc='count'
)

# dm_grp

label_pie_norm = dm_grp_norm.columns.to_list()
label_pie_norm

data_pie_norm = dm_grp_norm.iloc[0,:].to_list()
data_pie_norm

data_norm.loc[(data_norm['DM']=='당뇨병') & (data_norm['BL3164'] < 6.5)                          ,'DM_HbA1c'] = '01_~6.4'
data_norm.loc[(data_norm['DM']=='당뇨병') & (data_norm['BL3164'] > 6.4) & (data_norm['BL3164'] <  7.0),'DM_HbA1c'] = '02_6.5~6.9'
data_norm.loc[(data_norm['DM']=='당뇨병') & (data_norm['BL3164'] > 6.9) & (data_norm['BL3164'] <  8.0),'DM_HbA1c'] = '03_7.0~7.9'
data_norm.loc[(data_norm['DM']=='당뇨병') & (data_norm['BL3164'] > 7.9) & (data_norm['BL3164'] <  9.0),'DM_HbA1c'] = '04_8.0~8.9'
data_norm.loc[(data_norm['DM']=='당뇨병') & (data_norm['BL3164'] > 8.9) & (data_norm['BL3164'] < 10.0),'DM_HbA1c'] = '05_9.0~9.9'
data_norm.loc[(data_norm['DM']=='당뇨병') & (data_norm['BL3164'] > 9.9)                          ,'DM_HbA1c'] = '06_10.0~'

# data

DM_HbA1c_cat_norm = data_norm.pivot_table(
                              columns=['DM_HbA1c']
                             ,values=['CDW'] 
                             ,aggfunc='count'
                             )
DM_HbA1c_cat_norm

data_bar_norm = DM_HbA1c_cat_norm.iloc[0,:].to_list()
data_bar_norm

data_bar_per_norm = []

for i in range(len(data_bar_norm)):
    data_bar_per_norm.append(round(data_bar_norm[i]/data_pie_norm[0],3))

data_bar_per_norm

label_bar_norm = ['6.4% 이하'
            ,'6.5%~6.9%'
            ,'7.0%~7.9%'
            ,'8.0%~8.9%'
            ,'9.0%~9.9%'
            ,'10.0% 이상'
            ]

label_bar_norm

# #%%
# # data_pie_exec
# label_pie_exec

#%%
fig, ax = plt.subplots(linewidth=2)

plt.figure(figsize=(15,10))
# fig, ax = plt.subplots(figsize=(20,10 ), subplot_kw=dict(aspect="equal"),linewidth=2)
fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정

ax.set_title("당뇨병 유병율 비교\n\n",fontsize=50,y=2.2)

out_category = data_pie_exec
in_category = data_pie_norm
out_labels = label_pie_exec
in_labels = label_pie_norm
# explode = [0.1,0.1, 0,0,0,0,0,0,0,0,0]

out_cmap = plt.get_cmap("tab20")
in_cmap = plt.get_cmap("Pastel1")

outer_colors = out_cmap(np.array([2,1,0]))
inner_colors = in_cmap(np.array([0,1,2]))

w, ts, at = ax.pie(out_category, radius=5, colors=outer_colors,labels=out_labels,
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
ax.text(-5, -5.8,  '  ', fontsize=22)
ax.text(-5, -6.1,  '  ', fontsize=22)
ax.text(4.2, -5.5,  '□ 외측: 임원', fontsize=30)
ax.text(4.2, -6,  '□ 내측: 정규일반', fontsize=30)

fig.tight_layout()

plt.savefig("{}/02_02당뇨병_02유병율비교_new.png".format(workdir)
           , dpi=175)

plt.show()

#%%
labels_bar_dm =['임원','정규일반']

# Bar chart create
value01 = [data_bar_per_exec[0]*100,data_bar_per_norm[0]*100]
value02 = [data_bar_per_exec[1]*100,data_bar_per_norm[1]*100]
value03 = [data_bar_per_exec[2]*100,data_bar_per_norm[2]*100]
value04 = [data_bar_per_exec[3]*100,data_bar_per_norm[3]*100]
value05 = [data_bar_per_exec[4]*100,data_bar_per_norm[4]*100]
value06 = [data_bar_per_exec[5]*100,data_bar_per_norm[5]*100]

label01 = '6.4% 이하'
label02 = '6.5%~6.9%'
label03 = '7.0%~7.9%'
label04 = '8.0%~8.9%'
label05 = '9.0%~9.9%'
label06 = '10.0% 이상'

width = 0.5       # the width of the bars: can also be len(x) sequence

# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(15, 10),linewidth=2) # 캔버스 배경 사이즈 설정

fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정
rects1 = ax.bar(labels_bar_dm, value01, width, label=label01,alpha=0.85
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(data_bar_per_exec).shape[0]))[3])
rects2 = ax.bar(labels_bar_dm, value02, width, label=label02,alpha=0.85
                  ,bottom=value01
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(data_bar_per_exec).shape[0]))[5])
rects3 = ax.bar(labels_bar_dm, value03, width, label=label03,alpha=0.85
                  ,bottom=[value01[i]+value02[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(data_bar_per_exec).shape[0]))[4])
rects4 = ax.bar(labels_bar_dm, value04, width, label=label04,alpha=0.85
                  ,bottom=[value01[i]+value02[i]+value03[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(data_bar_per_exec).shape[0]))[2])
rects5 = ax.bar(labels_bar_dm, value05, width, label=label05,alpha=0.85
                  ,bottom=[value01[i]+value02[i]+value03[i]+value04[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(data_bar_per_exec).shape[0]))[1])
rects6 = ax.bar(labels_bar_dm, value06, width, label=label06,alpha=0.85
                  ,bottom=[value01[i]+value02[i]+value03[i]+value04[i]+value05[i] for i in range(len(value01))]
                  ,color=plt.get_cmap('RdYlBu')(np.linspace(0.15, 0.8,np.array(data_bar_per_exec).shape[0]))[0])

ax.set_title('당뇨병 유병자의 당화혈색소 분포\n\n',fontsize=35)
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
ax.bar_label(rects5, label_type='center',fontsize=18)
ax.bar_label(rects6, label_type='center',fontsize=18)

plt.text(1.43, 75,  '당화혈색소 기준', fontsize=25)
lg = ax.legend(bbox_to_anchor=(1.33,0.5),
          ncol=1  ,loc='right' ,fontsize=20
          )
# plt.text(-0.3, -24, '          ', fontsize=17)
# plt.text(-0.3, -27, '          ', fontsize=17)
# plt.text(-0.3, -30, '          ', fontsize=17)

fig.tight_layout()

plt.savefig("{}/02_02당뇨병_03당뇨병유병자당화혈색소.png".format(workdir)
            , dpi=175
            ,bbox_extra_artists=(lg,)
            # ,bbox_inches='tight'
            )

plt.show()

# # %%
# dm_grp_exec = data_exec.pivot_table(
#                           columns=['DM']
#                          ,values=['CDW']
#                          ,aggfunc='count'
# )

# # dm_grp

# label_pie_exec = dm_grp_exec.columns.to_list()
# label_pie_exec

# data_pie_exec = dm_grp_exec.iloc[0,:].to_list()
# data_pie_exec

# data_exec.loc[(data_exec['DM']=='당뇨병') & (data_exec['BL3164'] < 6.5)                          ,'DM_HbA1c'] = '01_~6.4'
# data_exec.loc[(data_exec['DM']=='당뇨병') & (data_exec['BL3164'] > 6.4) & (data_exec['BL3164'] <  7.0),'DM_HbA1c'] = '02_6.5~6.9'
# data_exec.loc[(data_exec['DM']=='당뇨병') & (data_exec['BL3164'] > 6.9) & (data_exec['BL3164'] <  8.0),'DM_HbA1c'] = '03_7.0~7.9'
# data_exec.loc[(data_exec['DM']=='당뇨병') & (data_exec['BL3164'] > 7.9) & (data_exec['BL3164'] <  9.0),'DM_HbA1c'] = '04_8.0~8.9'
# data_exec.loc[(data_exec['DM']=='당뇨병') & (data_exec['BL3164'] > 8.9) & (data_exec['BL3164'] < 10.0),'DM_HbA1c'] = '05_9.0~9.9'
# data_exec.loc[(data_exec['DM']=='당뇨병') & (data_exec['BL3164'] > 9.9)                          ,'DM_HbA1c'] = '06_10.0~'

# # data

# DM_HbA1c_cat_exec = data_exec.pivot_table(
#                               columns=['DM_HbA1c']
#                              ,values=['CDW'] 
#                              ,aggfunc='count'
#                              )
# DM_HbA1c_cat_exec

# data_bar_exec = DM_HbA1c_cat_exec.iloc[0,:].to_list()
# data_bar_exec

# data_bar_per_exec = []

# for i in range(len(data_bar_exec)):
#     data_bar_per_exec.append(round(data_bar_exec[i]/data_pie_exec[0],3))

# data_bar_per_exec

# label_bar_exec = ['6.4% 이하'
#             ,'6.5%~6.9%'
#             ,'7.0%~7.9%'
#             ,'8.0%~8.9%'
#             ,'9.0%~9.9%'
#             ,'10.0% 이상'
#             ]

# label_bar_exec

# # make figure and assign axis objects
# fig = plt.figure(figsize=(12, 12))
# ax1 = fig.add_subplot(121)
# ax2 = fig.add_subplot(122)
# fig.subplots_adjust(wspace=0.1)

# # pie chart parameters
# ratios = data_pie_exec
# pie_labels = label_pie_exec
# explode = [0.07, 0.02, 0.02]
# colors_pie = ['coral', 'wheat', 'lightgreen'] # '#99e472'

# def func(pct, allvals):
#     absolute = int(round(pct/100.*np.sum(allvals)))
# #     return "{:.1f}%\n({:,d})".format(pct, absolute) # %값(수치)로 표현하고 싶을 때, 1000 단위 마다 (,)표시하기
#     return "{:,d}\n({:.1f}%)".format(absolute, pct) # 수치(%값)로 표현하고 싶을 때1000 단위미다 ','표시

# # rotate so that first wedge is split by the x-axis
# ax1.pie(ratios, autopct=lambda pct: func(pct, ratios)
#         , startangle=-15, labels=pie_labels, explode=explode, colors=colors_pie
# ,textprops=dict(color="black",fontsize=22)
# ,shadow=True
# )

# # bar chart parameters
# xpos = 0.05
# bottom = 0
# ratios = data_bar_per_exec #bar chart using category percentile
# width = .2
# colors_bar = [
#        [0.4148009 , 0.54687353, 0.93908753, 1.        ],
#        [0.60854736, 0.73572523, 0.99935383, 1.        ],
#        [0.92811601, 0.82219715, 0.76514135, 1.        ],
#        [0.96771093, 0.66297301, 0.54432319, 1.        ],
#        [0.89213754, 0.42538874, 0.33328927, 1.        ],
#        'red'
#        ]
# # colors_bar = ['cornflowerblue','skyblue','mistyrose','lightpink','salmon','red']
# # colors_bar = ['#4a8ddc','#b5dafe','#ffbbed','#fd6252','#ffa500','#d82c20']
# # colors_bar = plt.get_cmap('coolwarm')(
# # np.linspace(0.15, 0.85, np.array(data_bar_per).shape[0])
# # )

# for j in range(len(ratios)):
#     height = ratios[j]
#     ax2.bar(xpos, height, width, bottom=bottom, color=colors_bar[j],alpha=0.7)
#     ypos = bottom + ax2.patches[j].get_height() / 2
#     bottom += height
#     ax2.text(xpos, ypos, "%1.1f%%" % (ax2.patches[j].get_height() * 100),
#              ha='center',color="black",fontsize=15)

# ax2.set_title('분포(%)', fontsize=17)

# # plt.text(-1.35, -0.005, '   ', fontsize=22)
# plt.text(-1.35, -0.005,  '당화혈색소 분류 기준:', fontsize=22)
# lg = ax2.legend(label_bar_exec
#                ,bbox_to_anchor=(-0.85,-0.105)
#                ,ncol=3
#                ,loc='lower left' ,fontsize=15
#                )
# plt.text(-1.6, -0.15,  '  ', fontsize=22)
# ax2.axis('off')
# ax2.set_xlim(- 2.5 * width, 2.5 * width)

# # use ConnectionPatch to draw lines between the two plots
# # get the wedge data
# theta1, theta2 = ax1.patches[0].theta1, ax1.patches[0].theta2
# center, r = ax1.patches[0].center, ax1.patches[0].r
# bar_height = sum([item.get_height() for item in ax2.patches])

# # draw top connecting line
# x = r * np.cos(np.pi / 180 * theta2) + center[0]
# y = np.sin(np.pi / 180 * theta2) + center[1]
# con = ConnectionPatch(xyA=(- width / 3, bar_height), xyB=(x, y),
# coordsA="data", coordsB="data", axesA=ax2, axesB=ax1)
# con.set_color([0, 0, 0])
# con.set_linewidth(2)
# ax2.add_artist(con)

# # draw bottom connecting line
# x = r * np.cos(np.pi / 180 * theta1) + center[0] 
# y = np.sin(np.pi / 180 * theta1) + center[1]
# con = ConnectionPatch(xyA=(- width / 3, 0), xyB=(x, y), coordsA="data",
# coordsB="data", axesA=ax2, axesB=ax1)
# con.set_color([0, 0, 0])
# ax2.add_artist(con)
# con.set_linewidth(2)
 
# # all subplot's title setting
# plt.suptitle('당뇨병 유병자의 당화혈색소 분포(임원)\n\n',fontsize=30)

# fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정

# # fig.tight_layout()

# plt.savefig("{}/02_02당뇨병_02당뇨병유병자당화혈색소_임원.png".format(workdir)
#             , dpi=175 #72의 배수 ,edgecolor='black'
#            )
 
# plt.show() 
# # %%
# dm_grp_norm = data_norm.pivot_table(
#                           columns=['DM']
#                          ,values=['CDW']
#                          ,aggfunc='count'
# )

# # dm_grp

# label_pie_norm = dm_grp_norm.columns.to_list()
# label_pie_norm

# data_pie_norm = dm_grp_norm.iloc[0,:].to_list()
# data_pie_norm

# data_norm.loc[(data_norm['DM']=='당뇨병') & (data_norm['BL3164'] < 6.5)                          ,'DM_HbA1c'] = '01_~6.4'
# data_norm.loc[(data_norm['DM']=='당뇨병') & (data_norm['BL3164'] > 6.4) & (data_norm['BL3164'] <  7.0),'DM_HbA1c'] = '02_6.5~6.9'
# data_norm.loc[(data_norm['DM']=='당뇨병') & (data_norm['BL3164'] > 6.9) & (data_norm['BL3164'] <  8.0),'DM_HbA1c'] = '03_7.0~7.9'
# data_norm.loc[(data_norm['DM']=='당뇨병') & (data_norm['BL3164'] > 7.9) & (data_norm['BL3164'] <  9.0),'DM_HbA1c'] = '04_8.0~8.9'
# data_norm.loc[(data_norm['DM']=='당뇨병') & (data_norm['BL3164'] > 8.9) & (data_norm['BL3164'] < 10.0),'DM_HbA1c'] = '05_9.0~9.9'
# data_norm.loc[(data_norm['DM']=='당뇨병') & (data_norm['BL3164'] > 9.9)                          ,'DM_HbA1c'] = '06_10.0~'

# # data

# DM_HbA1c_cat_norm = data_norm.pivot_table(
#                               columns=['DM_HbA1c']
#                              ,values=['CDW'] 
#                              ,aggfunc='count'
#                              )
# DM_HbA1c_cat_norm

# data_bar_norm = DM_HbA1c_cat_norm.iloc[0,:].to_list()
# data_bar_norm

# data_bar_per_norm = []

# for i in range(len(data_bar_norm)):
#     data_bar_per_norm.append(round(data_bar_norm[i]/data_pie_norm[0],3))

# data_bar_per_norm

# label_bar_norm = ['6.4% 이하'
#             ,'6.5%~6.9%'
#             ,'7.0%~7.9%'
#             ,'8.0%~8.9%'
#             ,'9.0%~9.9%'
#             ,'10.0% 이상'
#             ]

# label_bar_norm

# # make figure and assign axis objects
# fig = plt.figure(figsize=(12, 12))
# ax1 = fig.add_subplot(121)
# ax2 = fig.add_subplot(122)
# fig.subplots_adjust(wspace=0.1)

# # pie chart parameters
# ratios = data_pie_norm
# pie_labels = label_pie_norm
# explode = [0.07, 0.02, 0.02]
# colors_pie = ['coral', 'wheat', 'lightgreen'] # '#99e472'

# def func(pct, allvals):
#     absolute = int(round(pct/100.*np.sum(allvals)))
# #     return "{:.1f}%\n({:,d})".format(pct, absolute) # %값(수치)로 표현하고 싶을 때, 1000 단위 마다 (,)표시하기
#     return "{:,d}\n({:.1f}%)".format(absolute, pct) # 수치(%값)로 표현하고 싶을 때1000 단위미다 ','표시

# # rotate so that first wedge is split by the x-axis
# ax1.pie(ratios, autopct=lambda pct: func(pct, ratios)
#         , startangle=-15, labels=pie_labels, explode=explode, colors=colors_pie
# ,textprops=dict(color="black",fontsize=22)
# ,shadow=True
# )

# # bar chart parameters
# xpos = 0.05
# bottom = 0
# ratios = data_bar_per_norm #bar chart using category percentile
# width = .2
# colors_bar = [
#        [0.4148009 , 0.54687353, 0.93908753, 1.        ],
#        [0.60854736, 0.73572523, 0.99935383, 1.        ],
#        [0.92811601, 0.82219715, 0.76514135, 1.        ],
#        [0.96771093, 0.66297301, 0.54432319, 1.        ],
#        [0.89213754, 0.42538874, 0.33328927, 1.        ],
#        'red'
#        ]
# # colors_bar = ['cornflowerblue','skyblue','mistyrose','lightpink','salmon','red']
# # colors_bar = ['#4a8ddc','#b5dafe','#ffbbed','#fd6252','#ffa500','#d82c20']
# # colors_bar = plt.get_cmap('coolwarm')(
# # np.linspace(0.15, 0.85, np.array(data_bar_per).shape[0])
# # )

# for j in range(len(ratios)):
#     height = ratios[j]
#     ax2.bar(xpos, height, width, bottom=bottom, color=colors_bar[j],alpha=0.7)
#     ypos = bottom + ax2.patches[j].get_height() / 2
#     bottom += height
#     ax2.text(xpos, ypos, "%1.1f%%" % (ax2.patches[j].get_height() * 100),
#              ha='center',color="black",fontsize=15)

# ax2.set_title('분포(%)', fontsize=17)

# # plt.text(-1.35, -0.005, '   ', fontsize=22)
# plt.text(-1.35, -0.005,  '당화혈색소 분류 기준:', fontsize=22)
# lg = ax2.legend(label_bar_norm
#                ,bbox_to_anchor=(-0.85,-0.105)
#                ,ncol=3
#                ,loc='lower left' ,fontsize=15
#                )
# plt.text(-1.6, -0.15,  '  ', fontsize=22)
# ax2.axis('off')
# ax2.set_xlim(- 2.5 * width, 2.5 * width)

# # use ConnectionPatch to draw lines between the two plots
# # get the wedge data
# theta1, theta2 = ax1.patches[0].theta1, ax1.patches[0].theta2
# center, r = ax1.patches[0].center, ax1.patches[0].r
# bar_height = sum([item.get_height() for item in ax2.patches])

# # draw top connecting line
# x = r * np.cos(np.pi / 180 * theta2) + center[0]
# y = np.sin(np.pi / 180 * theta2) + center[1]
# con = ConnectionPatch(xyA=(- width / 3, bar_height), xyB=(x, y),
# coordsA="data", coordsB="data", axesA=ax2, axesB=ax1)
# con.set_color([0, 0, 0])
# con.set_linewidth(2)
# ax2.add_artist(con)

# # draw bottom connecting line
# x = r * np.cos(np.pi / 180 * theta1) + center[0] 
# y = np.sin(np.pi / 180 * theta1) + center[1]
# con = ConnectionPatch(xyA=(- width / 3, 0), xyB=(x, y), coordsA="data",
# coordsB="data", axesA=ax2, axesB=ax1)
# con.set_color([0, 0, 0])
# ax2.add_artist(con)
# con.set_linewidth(2)
 
# # all subplot's title setting
# plt.suptitle('당뇨병 유병자의 당화혈색소 분포(임원)\n\n',fontsize=30)

# fig.set_facecolor('whitesmoke') ## 캔버스 배경색 설정

# # fig.tight_layout()

# plt.savefig("{}/02_02당뇨병_02당뇨병유병자당화혈색소_임원.png".format(workdir)
#             , dpi=175 #72의 배수 ,edgecolor='black'
#            )
 
# plt.show()

# %%
