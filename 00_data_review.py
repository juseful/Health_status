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
GRP = 'BP'
data.loc[(data['SM0600SBP'] < 120) & (data['SM0600DBP'] < 80) & (data['TRT_MED_HYPERTENSION'] != '1'), GRP] = '03_OPTIMAL'
data.loc[(data['SM0600SBP'] >= 140) | (data['SM0600DBP'] >= 90) | (data['TRT_MED_HYPERTENSION'] == '1'), GRP] = '01_고혈압'
data['BP'].fillna('02_고혈압전단계',inplace=True)

GRP = 'DM'
data.loc[(data['BL3118'] < 100) & (data['BL3164'] < 5.7) & (data['TRT_MED_DIABETES'] != '1'), GRP] = '정상'
data.loc[(data['BL3118'] >= 126) | (data['BL3164'] >= 6.5) | (data['TRT_MED_DIABETES'] == '1'), GRP] = '당뇨병'
data['DM'].fillna('전당뇨',inplace=True)

data.loc[(data['DM']=='당뇨병') & (data['BL3164'] < 6.5)                          ,'DM_HbA1c'] = '01_~6.4'
data.loc[(data['DM']=='당뇨병') & (data['BL3164'] > 6.4) & (data['BL3164'] <  7.0),'DM_HbA1c'] = '02_6.5~6.9'
data.loc[(data['DM']=='당뇨병') & (data['BL3164'] > 6.9) & (data['BL3164'] <  8.0),'DM_HbA1c'] = '03_7.0~7.9'
data.loc[(data['DM']=='당뇨병') & (data['BL3164'] > 7.9) & (data['BL3164'] <  9.0),'DM_HbA1c'] = '04_8.0~8.9'
data.loc[(data['DM']=='당뇨병') & (data['BL3164'] > 8.9) & (data['BL3164'] < 10.0),'DM_HbA1c'] = '05_9.0~9.9'
data.loc[(data['DM']=='당뇨병') & (data['BL3164'] > 9.9)                          ,'DM_HbA1c'] = '06_10.0~'

GRP = 'DYSLIPID'
data.loc[(data['BL3113'] >= 240) | (data['BL314201'] >= 160 ) | (data['BL3141'] >= 200 ) | (data['BL3142'] < 40 ) | (data['TRT_MED_HYPERLIPIDEMIA'] == '1'), GRP] = '이상지질혈증'
data['DYSLIPID'].fillna('정상',inplace=True)

GRP = 'BMI'
data.loc[ data['SM316001'] < 18.5                            ,'BMI'] = '01. 저체중(BMI 0~18.4)'
data.loc[(data['SM316001'] >= 18.5) & (data['SM316001'] < 23),'BMI'] = '02. 정상체중(BMI 18.5~22.9)'
data.loc[(data['SM316001'] >= 23.0) & (data['SM316001'] < 25),'BMI'] = '03. 위험체중(BMI 23~24.9)'
data.loc[(data['SM316001'] >= 25.0) & (data['SM316001'] < 30),'BMI'] = '04. 비만1단계(BMI 25~29.9)'
data.loc[(data['SM316001'] >= 30.0) & (data['SM316001'] < 40),'BMI'] = '05. 비만2단계(BMI 30~39.9)'
data.loc[ data['SM316001'] >= 40.0                           ,'BMI'] = '06. 비만3단계(BMI 40~)'

GRP1 = "Fatty_YN"
GRP2 = "Category"
# data[GRP1] = ""
rsltcd_GRP = ['0007','0056','0003','0057','0002','0058','0054']
rslttext = [
            '01_Minimal'
           ,'02_Minimal to mild'
           ,'03_Mild'
           ,'04_Mild to Moderate'
           ,'05_Moderate'
           ,'06_Moderate to Severe'
           ,'07_Severe'
           ]

for i in range(len(rsltcd_GRP)):
    data['CAT_{}'.format(i)] = (
    (data.loc[:,'ABD_US_RSLT_CD'] == rsltcd_GRP[i])
    ).astype(int)
    data.loc[data['CAT_{}'.format(i)] == 1,GRP1] = "01_Fattyliver"
    data.loc[data['CAT_{}'.format(i)] == 1,GRP2] = rslttext[i]

data[GRP1].fillna('02_Absent',inplace=True)
data[GRP2].fillna('00_Absent',inplace=True)

GRP = 'CACT'

data.loc[ data['CACT_SCORE'] == 0                            ,'CACT'] = '01_No calcification(AJ-130 score = 0)'
data.loc[(data['CACT_SCORE'] > 0)    & (data['CACT_SCORE'] < 10) ,'CACT'] = '02_Minimal calcification(AJ-130 score 1 ~ 9)'
data.loc[(data['CACT_SCORE'] >= 10)  & (data['CACT_SCORE'] < 100),'CACT'] = '03_Mild calcification(AJ-130 score 10~99)'
data.loc[(data['CACT_SCORE'] >= 100) & (data['CACT_SCORE'] < 400),'CACT'] = '04_Moderate calcification(AJ-130 score 100 ~ 399)'
data.loc[ data['CACT_SCORE'] >= 400                          ,'CACT'] = '05_Severe calcification(AJ-130 score 400 ~)'

data.loc[data['CACT_SCORE'] != 0, 'CAL'] = '01_Cal'
data['CAL'].fillna('02_No',inplace=True)# data.loc[data['CACT_SCORE'] == 0, 'CAL'] = '02_No'

GRP = 'SMOKE'
data.loc[(data['SMK'] == '0'), GRP] = '비흡연'
data.loc[(data['SMK'] == '1'), GRP] = '금연중'
data.loc[(data['SMK'] == '2'), GRP] = '흡연중'

data.loc[(data['SMOKE']=='흡연중') & (data['SMK_CURRENT_AMOUNT'] == '0'),'SMOKE_AMT'] = '10개비 이하'
data.loc[(data['SMOKE']=='흡연중') & (data['SMK_CURRENT_AMOUNT'] == '1'),'SMOKE_AMT'] = '11~20개비'
# 문진응답내역에서 null 값은 중간값 처리
data.loc[(data['SMOKE']=='흡연중') & (data['SMK_CURRENT_AMOUNT'] == ""),'SMOKE_AMT']  = '11~20개비'
data.loc[(data['SMOKE']=='흡연중') & (data['SMK_CURRENT_AMOUNT'] == '2'),'SMOKE_AMT'] = '21_30개비'
data.loc[(data['SMOKE']=='흡연중') & (data['SMK_CURRENT_AMOUNT'] == '3'),'SMOKE_AMT'] = '31개비 이상'

GRP = 'ALCOHOL'
data.loc[(data['ALC_YS'] == '0'), GRP] = '금주'
data.loc[(data['ALC_YS'] == '1'), GRP] = '음주'

data.loc[(data['ALCOHOL']=='음주') & (data['ALC_FREQ'] == '0'),'ALCOHOL_FREQ'] = '01_월1회 이하'
data.loc[(data['ALCOHOL']=='음주') & (data['ALC_FREQ'] == '1'),'ALCOHOL_FREQ'] = '02_월2~3회'
data.loc[(data['ALCOHOL']=='음주') & (data['ALC_FREQ'] == '2'),'ALCOHOL_FREQ'] = '03_주1~2회'
# 문진응답내역에서 null 값은 중간값 처리
data.loc[(data['ALCOHOL']=='음주') & (data['ALC_FREQ'] == ''),'ALCOHOL_FREQ']  = '03_주1~2회'
data.loc[(data['ALCOHOL']=='음주') & (data['ALC_FREQ'] == '3'),'ALCOHOL_FREQ'] = '04_주3~4회'
data.loc[(data['ALCOHOL']=='음주') & (data['ALC_FREQ'] == '4'),'ALCOHOL_FREQ'] = '05_주5~6회'
data.loc[(data['ALCOHOL']=='음주') & (data['ALC_FREQ'] == '5'),'ALCOHOL_FREQ'] = '06_매일'

data.loc[(data['ALCOHOL']=='음주') & (data['ALC_AMOUNT_DRINKS'] == '0'),'ALCOHOL_AMT'] = '01_1~2잔'
data.loc[(data['ALCOHOL']=='음주') & (data['ALC_AMOUNT_DRINKS'] == '1'),'ALCOHOL_AMT'] = '02_반병'
# 문진응답내역에서 null 값은 중간값 처리
data.loc[(data['ALCOHOL']=='음주') & (data['ALC_AMOUNT_DRINKS'] == ''),'ALCOHOL_AMT']  = '02_반병'
data.loc[(data['ALCOHOL']=='음주') & (data['ALC_AMOUNT_DRINKS'] == '2'),'ALCOHOL_AMT'] = '03_1병'
data.loc[(data['ALCOHOL']=='음주') & (data['ALC_AMOUNT_DRINKS'] == '3'),'ALCOHOL_AMT'] = '04_2병이상'

GRP = 'PHY'
data.loc[(data['OVERALL_PHYSICAL_ACTIVITY'] == '0'), GRP] = '신체활동 없음'
data.loc[(data['OVERALL_PHYSICAL_ACTIVITY'] == '1'), GRP] = '신체활동(강도:3)'
data.loc[(data['OVERALL_PHYSICAL_ACTIVITY'] == '2'), GRP] = '신체활동(강도:2)'
data.loc[(data['OVERALL_PHYSICAL_ACTIVITY'] == '3'), GRP] = '신체활동(강도:1)'

data.loc[(data['PHY']!='신체활동 없음') & (data['PHY_FREQ'] == '1'),'PHY_FREQ_GRP'] = '주 1~2일'
data.loc[(data['PHY']!='신체활동 없음') & (data['PHY_FREQ'] == '2'),'PHY_FREQ_GRP'] = '주 3~4일'
data.loc[(data['PHY']!='신체활동 없음') & (data['PHY_FREQ'] == '3'),'PHY_FREQ_GRP'] = '주 5일 이상'

data.loc[(data['PHY']!='신체활동 없음') & (data['PHY_DURATION'] == '1'),'PHY_HOUR'] = '20분 이하'
# 문진응답내역에서 null 값은 중간값 처리
data.loc[(data['PHY']!='신체활동 없음') & (data['PHY_DURATION'] == '2'),'PHY_HOUR']  = '20~40분'
data.loc[(data['PHY']!='신체활동 없음') & (data['PHY_DURATION'] == '3'),'PHY_HOUR'] = '40~60분'
data.loc[(data['PHY']!='신체활동 없음') & (data['PHY_DURATION'] == '4'),'PHY_HOUR'] = '60분 이상'

GRP = 'STRESS'
data.loc[(data['STRESS_SCORE'] > 8 ) & (data['STRESS_SCORE'] < 27), GRP] = '잠재적 스트레스군'
data.loc[(data['STRESS_SCORE'] >= 27), GRP] = '고위험 스트레스군'
data['STRESS'].fillna('건강군',inplace=True)

data
#%%
data.to_excel('{}/건강현황분석data_review.xlsx'.format(workdir),index=False)
# %%
