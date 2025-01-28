from scipy import stats
import numpy as np

def check_normality(df, column):
    """
    if n<= 50:
        shapiro test
    else:
        D'Agostino's K^2 test
    """
    num_users = df[~df[column].isna()].shape[0] 
    if num_users <= 50:
       normality_test = stats.shapiro(df[column])
    else:
        normality_test = stats.normaltest(df[column])
    if normality_test.pvalue <= 0.05:
        return num_users, True
    else:
        return num_users, False
    
def get_median_iqr(df, column):
    # remove nan numbers first
    data = df[~df[column].isna()][column]
    median = data.median()
    q1 = np.percentile(data, 25, interpolation='midpoint')
    q3 = np.percentile(data, 75, interpolation='midpoint')
    iqr = q3 - q1
    return median.round(1), iqr.round(1)

def get_mean_std(df, column):
    data = df[column]
    return data.mean().round(1), data.std().round(1)

def get_column_stats(df, column):
    n, is_normal = check_normality(df, column)
    if is_normal:
        mean, std = get_mean_std(df, column)
        return n, is_normal, mean, std
    else:
        median, iqr = get_median_iqr(df, column)
        return n, is_normal, median, iqr
    

def rename_evaluation_survey_columns(df, is_initial_session):
    df = df.copy()
    is_responses_to_be_renamed_dict = {
                'Alter': 'age', 
                'Geschlecht': 'gender',
                'Arbeitserfahrung als ErnährungsberaterIn (in Jahren)':'years_of_experience',
                'Ich verwende häufig\xa0Software Applikationen\xa0(z.B. Nährwertdatenbanken, Ernährungs-Apps, usw.) \xa0in meinem Arbeitsalltag.': 'software_usage',
                'Ich halte die DietCoach-Plattform für nützlich.': 'useful',
                'Die Nutzung der DietCoach-Plattform ermöglicht es mir, Aufgaben schneller zu erledigen.': 'fast_to_finish_tasks',
                'Die Nutzung der DietCoach-Plattform steigert meine Produktivität.':'improve_productivity',
                'Das Erlernen der Nutzung der DietCoach-Plattform fällt mir leicht.': 'easy_to_learn',
                'Interaktion mit der DietCoach-Plattform ist klar und verständlich.': 'clear_interaction',
                'Ich finde die DietCoach-Plattform einfach zu nutzen.': 'easy_to_use',
                'Es fällt mir leicht, die DietCoach-Plattform geschickt zu nutzen.': 'easy_to_use_skillfully',
                'Ich verfüge über die notwendigen Ressourcen, um die DietCoach-Plattform zu nutzen.': 'resources_to_use',
                'Ich verfüge über die erforderlichen Kenntnisse zur Nutzung der DietCoach-Plattform.': 'knowledge_to_use',
                'Die DietCoach-Plattform ist mit anderen von mir verwendeten Technologien kompatibel.': 'tech_compatibility',
                'Ich beabsichtige, die DietCoach-Plattform auch in Zukunft zu nutzen, sofern sie verfügbar ist.': 'use_in_future',
                'Ich werde versuchen, die DietCoach-Plattform bei meiner Arbeit zu nutzen, sofern sie verfügbar ist.': 'use_at_work',
                'Ich habe vor, die DietCoach-Plattform weiterhin häufig zu nutzen, sofern sie verfügbar ist.':'use_frequently',
                'DietCoach zu nutzen macht Spaß': 'fun_to_use', 
                'DietCoach zu nutzen ist angenehm': 'comfortable_to_use',
                'DietCoach zu nutzen ist sehr unterhaltsam': 'entertaining_to_use',
                'Ich denke, dass ich die DietCoach-Plattform häufig nutzen möchte.': 'sus_frequent_use',
                'Ich finde die DietCoach-Plattform unnötig komplex.': 'sus_complex',
                'Ich finde die DietCoach-Plattform einfach zu bedienen.': 'sus_easy_to_operate',
                'Ich glaube, dass ich die Unterstützung einer technischen Person benötige, um die DietCoach-Plattform nutzen zu können.': 'sus_technical_support',
                'Ich finde, dass die verschiedenen Funktionen der DietCoach-Plattform gut integriert waren.': 'sus_well_integrated',
                'Ich finde, dass die DietCoach-Plattform zu inkonsistent war.': 'sus_inconsistent',
                'Ich könnte mir vorstellen, dass die meisten Ernährungsberater die DietCoach-Plattform sehr schnell erlernen würden.': 'sus_quick_learning',
                'Ich finde die DietCoach-Plattform sehr umständlich zu bedienen.': 'sus_awkward',
                'Ich fühlte mich bei der Nutzung der DietCoach-Plattform sehr sicher.': 'sus_safe',
                'Ich musste viele Dinge lernen, bevor ich mit der DietCoach-Plattform loslegen konnte.': 'sus_learn_before_start',
        }

    additional_fs_to_be_renamed_ls = {'Die DietCoach-Plattform verbessert mein Verständnis für die Lebensmittelauswahl der Patienten.': 'increase_patient_food_understanding',
                'Die Bereitstellung von Ernährungsempfehlungen unter Einbezug der tatsächlichen Lebensmittel-Einkaufsdaten der Patienten würde die Qualität der Ernährungsversorgung verbessern.': 'improve_nutrition_care_quality',
                'Patienten würden mit einer Ernährungsberatung, die auf ihrem tatsächlichen Kaufverhalten basiert, bessere Gesundheitsergebnisse erzielen.': 'better_achieve_health_outcomes',
                'Welcher Prozentsatz Ihrer Patienten könnte Ihrer Meinung nach davon profitieren, wenn Sie die DietCoach-Plattform nutzen?': 'perc_patients_can_benefit',
                'Mehrpersonenhaushalt': 'multi_person_household', 
                'Die Nutzung der Treuekarte wird vorausgesetzt': 'required_use_of_customer_card',
                'Es werden nur Einkäufe berücksichtigt': 'fpd_only',
                'Nur Einkäufe bei Migros und Coop werden berücksichtigt': 'migros_coop_only',
                'Medizinische Diagnose des Patienten (z.B., Diabetes)': 'medical_diagnosis',
                'Demografie des Kunden (Geschlecht, Alter)': 'client_demographics',
                'Ich würde mich dafür einsetzen, dass das DietCoach-System von Versicherungen abgedeckt wird. ': 'insurance_coverage',
                'Die DietCoach-Plattform ist wertvoll, im Vergleich zu anderen Tools oder Systemen, die ich in meinem Arbeitsablauf verwende.': 'valuable_compared_to_other_tools',
                'Die DietCoach-Plattform könnte zu Kosteneinsparungen in der Patientenversorgung führen.': 'promote_cost_savings',
                'Was halten Sie für einen fairen Preis, den potenzielle Zahler, z.B. Patienten oder deren Krankenversicherungen, für die DietCoach-Plattform zu zahlen bereit wären (pro Patient pro Monat in CHF)?': 'price_per_patient_per_month',
                }
    if is_initial_session:
        to_be_renamed_dict = is_responses_to_be_renamed_dict
    else:
        to_be_renamed_dict = {**is_responses_to_be_renamed_dict, **additional_fs_to_be_renamed_ls}
    df = df.rename(columns=to_be_renamed_dict)
    df = df[list(to_be_renamed_dict.values()) + ['institution', 'email']]
    
    return df



def map_likert_to_numbers(df, is_initial_session):
    df = df.copy()
    #map likert scales to numebrs
    five_likert_mapping = {
        'Stimme überhaupt nicht zu': 1,
        'Stimme nicht zu': 2,
        'Weder noch': 3,
        'Stimme zu': 4,
        'Stimme völlig zu': 5
    }

    seven_likert_mapping = {
        'Stimme überhaupt nicht zu': 1,
        'Stimme nicht zu': 2,
        'Stimme eher nicht zu': 3,
        'Weder noch': 4,
        'Stimme zu': 5,
        'Stimme eher zu': 6,
        'Stimme völlig zu': 7
    }

    patient_perc_mapping = {
        '0-20% ': 1,
        '21-40%': 2,
        '41-60%': 3,
        '61-80%': 4,
        '81-100%': 5
    }

    positive_sus_columns = ['sus_frequent_use', 'sus_easy_to_operate', 
        'sus_well_integrated',  'sus_quick_learning', 'sus_safe']

    negative_sus_columns = ['sus_complex', 'sus_technical_support',
        'sus_inconsistent', 'sus_awkward', 'sus_learn_before_start']

    columns_to_seven_likert_mapping = ['software_usage', 'useful',
        'fast_to_finish_tasks', 'improve_productivity', 'easy_to_learn',
        'clear_interaction', 'easy_to_use', 'easy_to_use_skillfully',
        'resources_to_use', 'knowledge_to_use', 'tech_compatibility',
        'use_in_future', 'use_at_work', 'use_frequently', 'fun_to_use',
        'comfortable_to_use', 'entertaining_to_use']
    
    if is_initial_session:
        for col in positive_sus_columns + negative_sus_columns:
            df[col] = df[col].map(five_likert_mapping)
    else:
        other_columns = ['increase_patient_food_understanding',
                     'improve_nutrition_care_quality',
                     'better_achieve_health_outcomes',
                     'multi_person_household', 
                     'required_use_of_customer_card',
                     'fpd_only',
                     'migros_coop_only',
                     'medical_diagnosis',
                     'client_demographics',
                     'insurance_coverage',
                     'valuable_compared_to_other_tools',
                     'promote_cost_savings',
                     'price_per_patient_per_month']
        #special mapping for perc_patients_can_benefit
        df.perc_patients_can_benefit = df.perc_patients_can_benefit.map(patient_perc_mapping)
        
        for col in positive_sus_columns + negative_sus_columns + other_columns:
            df[col] = df[col].map(five_likert_mapping)

    for col in columns_to_seven_likert_mapping:
        df[col] = df[col].map(seven_likert_mapping)
    return df


def calculate_sus(row):
    positive_sus_columns = ['sus_frequent_use', 'sus_easy_to_operate', 
        'sus_well_integrated',  'sus_quick_learning', 'sus_safe']

    negative_sus_columns = ['sus_complex', 'sus_technical_support',
        'sus_inconsistent', 'sus_awkward', 'sus_learn_before_start']

    positive_sus = row[positive_sus_columns].sum() - 5
    negative_sus = 25 -row[negative_sus_columns].sum()
    return 2.5 * (positive_sus + negative_sus)

def calculate_aggregated_metrics(df):
    df = df.copy()
    df['sus'] = df.apply(calculate_sus, axis=1)
    df['performance_expectancy'] = df[['useful', 'fast_to_finish_tasks', 'improve_productivity']].mean(axis=1)
    df['effort_expectancy'] = df[['easy_to_learn', 'clear_interaction', 'easy_to_use', 'easy_to_use_skillfully']].mean(axis=1)
    df['facilitating_conditions'] = df[['resources_to_use', 'knowledge_to_use', 'tech_compatibility']].mean(axis=1)
    df['behavioral_intention'] = df[['use_in_future', 'use_at_work', 'use_frequently']].mean(axis=1)
    df['hedonic_motivation'] = df[['fun_to_use', 'comfortable_to_use', 'entertaining_to_use']].mean(axis=1)
    return df
