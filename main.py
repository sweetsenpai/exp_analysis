import pandas as pd
import numpy as np




# Процент пользователей купивших премиум после триала
def trial_prem_proc(payments, portrait):
    # группируем записи по id пользователе
    pay_gr = payments.groupby('user_id')
    count_user_list = []
    # выбираем только те записи,где пользователь получал как триал,так и премиуим
    for key, item in pay_gr:
        if not item[item.product_type == 'prem'].empty:
            if not item[item.product_type == 'trial'].empty:
                count_user_list.append(key)
            else: continue

    return len(count_user_list)/(len(portrait)*0.01)


# процент пользователей купившых премимум
def all_prem(portrait):
    tmp_ds = portrait.loc[portrait['is_special'] == 1]
    return len(tmp_ds)/(len(portrait) * 0.01)



# проценты купивших подписку по странам
def country_group(portrait):
    # группируем записи по странам
    country_gr = portrait.groupby('country')
    country_list = []
    # формируем список с названиями стран
    for keys, items in country_gr:
        country_list.append(keys)
    proc_list =[]
    # далее формируем словарь где ключ это страна,а значение процент премиум пользователей
    # предварительно отфильтровав страны с малым количеством пользователей
    for country in country_list:
        tmp = country_gr.get_group(country)
        all = tmp.count()['user_id']
        if  all >= 20:
            prem = tmp[(tmp.is_special == 1)].count()['user_id']
            proc_list.append(prem / (all * 0.01))

    country_dict = dict(zip(country_list, proc_list))
    return country_dict


# создание возрастных групп
# 16 - 17,18-24,25-44,45-64,65-74,75+
def age_group(portrait):
    # переформатируем столбец,чтобы он мог принемать значения типа string
    portrait['age'] = portrait['age'].apply(str)
    age_list = ['16-17', '18-24', '25-44', '45-64', '65+']
    # вместо возраста присваиваем пользователю возрастную группу
    for index, row in portrait.iterrows():
        if 16 <= int(row['age']) <= 17:
            portrait._set_value(index, 'age', age_list[0])
        elif 18 <= int(row['age']) <= 24:
            portrait._set_value(index, 'age', age_list[1])
        elif 25 <= int(row['age']) <= 44:
            portrait._set_value(index, 'age', age_list[2])
        elif 45 <= int(row['age']) <= 64:
            portrait._set_value(index, 'age', age_list[3])
        elif 65 <= int(row['age']) :
            portrait._set_value(index, 'age', age_list[4])
    # группируем записи по возрастным группам
    age_gr = portrait.groupby('age')
    # далее формируем словарь где ключ это возрастная группа ,а значение процент премиум пользователей
    proc_list = []
    for age in age_list:
        tmp = age_gr.get_group(age)
        all = tmp.count()['user_id']
        prem = tmp[(tmp.is_special == 1)].count()['user_id']
        proc_list.append(prem/(all*0.01))
    age_dict = dict(zip(age_list, proc_list))
    return age_dict


# группы по полу
def sex_group(portrait):
    # переформатируем столбец,чтобы он мог принемать значения типа string
    portrait['sex'] = portrait['sex'].apply(str)
    sex_list = ['male', 'female']
    # заменяем 0 и 1 на значения male и female
    for index, row in portrait.iterrows():
        if row['sex'] == '0':
            portrait._set_value(index, 'sex', sex_list[1])
        else:
            portrait._set_value(index, 'sex', sex_list[0])
    # далее делаем тоже,что и в предидущих функциях
    sex_gr  = portrait.groupby('sex')
    proc_list = []
    for sex in sex_list:
        tmp = sex_gr.get_group(sex)
        all = tmp.count()['user_id']
        prem = tmp[(tmp.is_special == 1)].count()['user_id']
        proc_list.append(prem / (all * 0.01))

    sex_dict = dict(zip(sex_list, proc_list))
    return sex_dict


#группы  по активности

def activity_group(portrait):
    # переформатируем столбец,чтобы он мог принемать значения типа string
    portrait['retention_days'] = portrait['retention_days'].apply(str)
    # заменяем nan значения на группу zero activity
    portrait['retention_days'] = portrait_tg['retention_days'].fillna('zero activity')
    activity_list = ['zero activity', 'low activity', 'medium activity', 'high activity', 'very high activity']
    # распределяем по группам
    for index, row in portrait.iterrows():
        if row['retention_days'] == 'zero activity':
            continue
        elif 1 <= len(row['retention_days'].split(',')) <= 5:
            portrait._set_value(index, 'retention_days', activity_list[1])
        elif 6 <= len(row['retention_days'].split(',')) <= 12:
            portrait._set_value(index, 'retention_days', activity_list[2])
        elif 13 <= len(row['retention_days'].split(',')) <= 20:
            portrait._set_value(index, 'retention_days', activity_list[3])
        elif len(row['retention_days'].split(',')) > 20:
            portrait._set_value(index, 'retention_days', activity_list[4])
    # далее делаем тоже,что и в предидущих функциях
    activity_gr = portrait.groupby('retention_days')
    proc_list = []
    for activity in activity_list:
        tmp = activity_gr.get_group(activity)
        all = tmp.count()['user_id']
        prem = tmp[(tmp.is_special == 1)].count()['user_id']
        proc_list.append(prem / (all * 0.01))
    activity_dict = dict(zip(activity_list, proc_list))
    return activity_dict


# функция для пересчета превликательности
def rating_recalculation(view, rating):
    if 1 <= view <= 5:
        rating = rating * 0.1
    elif 6 <= view <= 10:
        rating = rating * 0.2
    elif 11 <= view <= 16:
        rating = rating * 0.3
    elif 17 <= view <= 23:
        rating = rating * 0.4
    elif 24 <= view <= 29:
        rating = rating * 0.5
    elif 30 <= view <= 35:
        rating = rating * 0.6
    elif 36 <= view <= 41:
        rating = rating * 0.7
    elif 42 <= view <= 47:
        rating = rating * 0.8
    elif 48 <= view <= 49:
        rating = rating * 0.9
    elif view <= 50:
        pass
    return rating


# группы по популярности
def attraction_group(portrait):
    portrait['attraction_distribution'] = portrait['attraction_distribution'].apply(str)
    att_list = ['very low attraction', 'low attraction', 'medium attraction', 'high attraction', 'very high attraction']
    for index, row in portrait.iterrows():
        if 0<= rating_recalculation(row['view_count'], int(row['attraction_distribution'])) <= 200:
            portrait._set_value(index, 'attraction_distribution', att_list[0])
        elif 200 < rating_recalculation(row['view_count'], int(row['attraction_distribution'])) <= 400:
            portrait._set_value(index, 'attraction_distribution', att_list[1])
        elif 400 < rating_recalculation(row['view_count'], int(row['attraction_distribution'])) <= 600:
            portrait._set_value(index, 'attraction_distribution', att_list[2])
        elif 600 < rating_recalculation(row['view_count'], int(row['attraction_distribution'])) <= 800:
            portrait._set_value(index, 'attraction_distribution', att_list[3])
        elif rating_recalculation(row['view_count'], int(row['attraction_distribution'])) > 800:
            portrait._set_value(index, 'attraction_distribution', att_list[4])
    att_gr = portrait.groupby('attraction_distribution')
    proc_list = []
    for age in att_list:
        tmp = att_gr.get_group(age)
        all = tmp.count()['user_id']
        prem = tmp[(tmp.is_special == 1)].count()['user_id']
        proc_list.append(prem / (all * 0.01))
    age_dict = dict(zip(att_list, proc_list))
    return age_dict


def attraction_group_true(portrait):
    portrait['attraction_distribution'] = portrait['attraction_distribution'].apply(str)
    att_list = ['very low attraction', 'low attraction', 'medium attraction', 'high attraction', 'very high attraction']
    for index, row in portrait.iterrows():
        if 0<= int(row['attraction_distribution']) <= 200:
            portrait._set_value(index, 'attraction_distribution', att_list[0])
        elif 200 < int(row['attraction_distribution']) <= 400:
            portrait._set_value(index, 'attraction_distribution', att_list[1])
        elif 400 < int(row['attraction_distribution']) <= 600:
            portrait._set_value(index, 'attraction_distribution', att_list[2])
        elif 600 < int(row['attraction_distribution']) <= 800:
            portrait._set_value(index, 'attraction_distribution', att_list[3])
        elif int(row['attraction_distribution']) > 800:
            portrait._set_value(index, 'attraction_distribution', att_list[4])
    att_gr = portrait.groupby('attraction_distribution')
    proc_list = []
    for age in att_list:
        tmp = att_gr.get_group(age)
        all = tmp.count()['user_id']
        prem = tmp[(tmp.is_special == 1)].count()['user_id']
        proc_list.append(prem / (all * 0.01))
    age_dict = dict(zip(att_list, proc_list))
    return age_dict


# убираем статус премиум у пользователей у которых активированна только пробная подписка
def remove_trial(payments, portrait):
    # группируем записи о платежах по id пользователей
    group_tg = payments.groupby('user_id')
    trial = []
    # копируем id пользователей которые используют пробную подписку
    for key, items in group_tg:
        if not items[items.product_type == "trial"].empty and items[items.product_type == "prem"].empty:
            trial.append(key)
    # чтобы в дальнейшем работать с правильными данными обнуляем поля was_special и is_special у пользователей
    # которые используют  пробную подписку
    for user in trial:
        id = portrait_tg.index[portrait_tg['user_id'] == user]
        portrait.at[id, 'was_special'] = np.NAN
        portrait.at[id, 'is_special'] = np.NAN

    return portrait


if __name__ == '__main__':

    payments_cg1 = pd.read_csv(r'Data/payments_CG1.csv', sep=';').dropna()
    payments_cg2 = pd.read_csv(r'Data/payments_CG2.csv', sep=';').dropna()
    payments_tg = pd.read_csv(r'Data/payments_TG.csv', sep=';').dropna()

    portrait_cg1 = pd.read_csv(r'Data/portrait_CG1.csv', sep=';')
    portrait_cg2 = pd.read_csv(r'Data/portrait_CG2.csv', sep=';')
    portrait_tg = pd.read_csv(r'Data/portrait_TG.csv', sep=';')

    pd.set_option("display.max_rows", None, "display.max_columns", None)

    portrait_cg1 = remove_trial(payments_cg1, portrait_cg1)
    portrait_cg2 = remove_trial(payments_cg2, portrait_cg2)
    portrait_tg = remove_trial(payments_tg, portrait_tg)

    #print(activity_group(portrait_cg1))
    #print(activity_group(portrait_cg2))
    #print(activity_group(portrait_tg))

    #print(sex_group(portrait_cg1))
    #print(sex_group(portrait_cg2))
    #print(sex_group(portrait_tg))

    #print(activity_group(portrait_cg1))
    #print(activity_group(portrait_cg2))
    #print(activity_group(portrait_tg))

    #print(attraction_group_true(portrait_tg))
    #print(attraction_group_true(portrait_cg1))
    #print(attraction_group(portrait_cg2))
    #print(attraction_group(portrait_tg))
    """
    plt.bar([0], [2.197], width=0.1, label='CG1', color='b')
    plt.bar([0.1], [3.07], width=0.1, label='CG2', color='g')
    plt.bar([0.2], [1.98], width=0.1, label='TG', color='r')

    plt.legend()

    plt.xlabel('')
    plt.ylabel('Процент')
    plt.title('Женщины')

    plt.show()

    
    labels = ['CG1', 'CG2', 'TG']
    prem_means = [192, 191, 97]
    pleb_means = [4148, 4073, 4211]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, prem_means, width, label='Премимум пользователи')
    rects2 = ax.bar(x + width/2, pleb_means, width, label='Обычные пользователи')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Scores')
    ax.set_title('Отношение пользователейс подпиской и без,в разных  группах')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()


    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')


    autolabel(rects1)
    autolabel(rects2)

    fig.tight_layout()

    plt.show()

      # Pie chart, where the slices will be ordered and plotted counter-clockwise:
       labels = 'С подпиской', 'Без подписки'
       sizes = [all_prem(portrait_tg), 100  - all_prem(portrait_tg)]
       explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

       fig1, ax1 = plt.subplots()
       ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
               shadow=True, startangle=90)
       ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

       plt.show()"""